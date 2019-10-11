import re
import os

import config


class TemplateWriter:
	src = ''
	dest = ''
	
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		
	def write_out(self, template={}):
		with open(self.src, 'r') as src_template:
			text = src_template.read()

		for placeholder, value in template.items():
			text = text.replace(placeholder, value)
		
		with open(self.dest, 'w') as dest_file:
			dest_file.write(text)
	

class FileWriter:
	dest = ''
	
	def __init__(self, dest, enc="utf-8"):
		self.dest = dest
		self.f = open(dest, "w", encoding=enc)
		
	def write_line(self, line="", ident_count=0):
		self.f.write("\t" * ident_count + line + "\n")
		
	def close(self):
		self.f.close()
		
		
def get_default_class_name(module):
	return ''.join(x for x in module['short_name'].title() if not x.isspace())
	
	
def get_include_by_type(class_type):
    return {
        'Reference': "#include \"core/reference.h\"",
    }[class_type]


def make_config(module, module_path):
	config_dest = os.path.join(module_path, "config.py")
	
	fw = FileWriter(config_dest)
	
	fw.write_line()
	
	v = module['engine_version']
	if v == 'latest':
		fw.write_line("def can_build(env, platform):")
	elif v == '3.0':
		fw.write_line("def can_build(env):")
	
	fw.write_line("return True", 1)
	fw.write_line()

	fw.write_line("def configure(env):")
	fw.write_line("pass", 1)
	fw.write_line()
	
	if module["docs_path"]:
		fw.write_line("def get_doc_path():")
		fw.write_line("return \"" + module["docs_path"] + "\"", 1)
		fw.write_line()
		
	if module["icons_path"]:
		fw.write_line("def get_icons_path():")
		fw.write_line("return \"" + module["icons_path"] + "\"", 1)
		fw.write_line()
		
	fw.close()

	
def make_readme(module, module_path):
	readme_dest = os.path.join(module_path, "README.md")
	
	fw = FileWriter(readme_dest)
	
	fw.write_line("#" + " " + module['name'])
	fw.write_line()
	
	if module['readme']['include_installation_instructions']:
		
		fw.write_line("## Installation")
		fw.write_line()
		fw.write_line("Before installing, you must be able to")
		fw.write_line("[compile Godot Engine](https://docs.godotengine.org/en/" \
				+ module["engine_version"] + "/development/compiling/) from source.")
				
		fw.write_line()
		
		fw.write_line("```bash")
		fw.write_line("# Copy the module under directory named " + module['short_name'] + " (must be exactly that)")
		fw.write_line("cp " + module['short_name'] + " <godot_path>/modules/" + module['short_name'] + " && cd <godot_path>")
		fw.write_line("# Compile the engine manually, for instance:")
		fw.write_line("scons platform=linux target=release_debug bits=64")
		fw.write_line("```")
	
	fw.close()
	
	
def make_license(module, module_path):
	license_src = os.path.join(config.licenses_path, module['license']) + ".txt"
	license_dest = os.path.join(module_path, "LICENSE.txt")
	
	import datetime
	license_template = {
		"__YEAR__" : str(datetime.datetime.now().year),
		"__AUTHOR__" : module['author'],
	}
	tw = TemplateWriter(license_src, license_dest)
	tw.write_out(license_template)
	
	
def make_register_types(module, module_path):
	
	# Header
	reg_types_header_dest = os.path.join(module_path, "register_types.h")
	header = FileWriter(reg_types_header_dest)
	
	header.write_line("void register_" + module['short_name'] + "_types();")
	header.write_line("void unregister_" + module['short_name'] + "_types();")
	header.close()
	
	# Source
	reg_types_source_dest = os.path.join(module_path, "register_types.cpp")
	source = FileWriter(reg_types_source_dest)
	
	source.write_line("#include \"register_types.h\"")
	source.write_line()
	
	for c in module['classes']:
		name = c['name']
		if not name:
			name = get_default_class_name(module)
		source.write_line("#include " + '\"' + name.lower() + ".h" + '\"')
		
	source.write_line()
	
	source.write_line("void register_" + module['short_name'] + "_types() {")
	source.write_line()
	
	for c in module['classes']:
		name = c['name']
		if not name:
			name = get_default_class_name(module)
		source.write_line("ClassDB::register_class<" + name + ">();", 1)
		
	source.write_line("}")
	source.write_line()
	
	source.write_line("void unregister_" + module['short_name'] + "_types() {")
	source.write_line()
	source.write_line("// nothing to do here", 1)
	source.write_line("}")
	
	source.close()


def make_scsub(module, module_path):
	scsub_dest = os.path.join(module_path, "SCsub")
	
	scsub = FileWriter(scsub_dest)
	
	scsub.write_line("#!/usr/bin/env python")
	scsub.write_line()
	scsub.write_line("Import('env')")
	scsub.write_line("Import('env_modules')")
	scsub.write_line()

	env_module = "env_" + module['short_name']
	
	scsub.write_line(env_module + " = env.Clone()")
	scsub.write_line()
	
	if module['thirdparty_path']:
		scsub.write_line("# Thirdparty source files")
		scsub.write_line("thirdparty_dir = '" + module['thirdparty_path'] + "/'")
		scsub.write_line("thirdparty_sources = []")
		scsub.write_line("thirdparty_sources += Glob(thirdparty_dir + '**/*.cpp')")
		scsub.write_line("thirdparty_sources += Glob(thirdparty_dir + '**/*.c')")
		scsub.write_line()

		scsub.write_line(env_module + ".Prepend(CPPPATH=[thirdparty_dir])")
		scsub.write_line()
		
		scsub.write_line("env_thirdparty = " + env_module + ".Clone()")
		scsub.write_line("env_thirdparty.add_source_files(env.modules_sources, thirdparty_sources)")
		scsub.write_line("env_thirdparty.disable_warnings()")
		scsub.write_line()

	scsub.write_line("# Module source files")
	scsub.write_line(env_module + ".add_source_files(env.modules_sources, '*.cpp')")
	
	scsub.close()
	
	
def make_classes(module, module_path):
	
	already_got_default = False
	
	for c_data in module['classes']:
		name = c_data['name']
		if not name:
			if already_got_default:
				continue
			name = get_default_class_name(module)
			already_got_default = True
			
		inherits = c_data['inherits']
		
		# Header
		header_dest = os.path.join(module_path, name.lower() + '.h')
		write_class_header(header_dest, name, inherits)
		
		# Source
		source_dest = os.path.join(module_path, name.lower() + '.cpp')
		write_class_source(source_dest, name, inherits)
		
		
def write_class_header(header_dest, name, inherits):
	
	header = FileWriter(header_dest)
	
	header.write_line("#ifndef " + name.upper() + "_H")
	header.write_line("#define " + name.upper() + "_H")
	header.write_line()
	
	header.write_line(get_include_by_type(inherits))
	header.write_line()
	
	header.write_line("class " + name + " : " + "public " + inherits + " {")
	header.write_line("GDCLASS(" + name + ", " + inherits + ");", 1)
	header.write_line()
	
	header.write_line("protected:")
	header.write_line("static void _bind_methods();", 1)
	
	header.write_line("};")
	header.write_line()
	
	header.write_line("#endif " + "// " + name.upper() + "_H")
	
	header.close()
	
	
def write_class_source(source_dest, name, inherits):
	
	source = FileWriter(source_dest)
	
	source.write_line("#include " + '\"' + name.lower() + ".h" + '\"')
	source.write_line()
	
	source.write_line("void " + name + "::_bind_methods() {")
	source.write_line()
	source.write_line("}")
	
	source.close()
	