import re
import os
from pathlib import Path

import common


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
	
	
def get_include_by_type(class_type):
    return {
        'Reference': "#include \"core/reference.h\"",
    }[class_type]


def make_config(module):
	config_dest = os.path.join(module.path, "config.py")
	
	fw = FileWriter(config_dest)
	
	fw.write_line()
	
	ver = module.get_engine_version(False)
	if ver['major'] >= 3:
		# 3.0 vs 3.1: https://github.com/godotengine/godot/pull/19275
		if ver['minor'] >= 1:
			fw.write_line("def can_build(env, platform):")
		else:
			fw.write_line("def can_build(env):")
	
		fw.write_line("return True", 1)
		fw.write_line()

	fw.write_line("def configure(env):")
	fw.write_line("pass", 1)
	fw.write_line()
	
	if module.get_docs_path():
		fw.write_line("def get_doc_path():")
		fw.write_line("return \"" + module.get_docs_path() + "\"", 1)
		fw.write_line()
		
		fw.write_line("def get_doc_classes():")
		fw.write_line("return [", 1)
		
		for c in module.get_classes():
			name = c['name']
			if not name:
				name = module.get_default_class_name()
			fw.write_line('\"' + name + '\"' + ',', 2)
			
		fw.write_line("]", 1)
		fw.write_line()
		
	if module.get_icons_path():
		fw.write_line("def get_icons_path():")
		fw.write_line("return \"" + module.get_icons_path() + "\"", 1)
		fw.write_line()
		
	fw.close()

	
def make_readme(module):
	readme_dest = os.path.join(module.path, "README.md")
	
	fw = FileWriter(readme_dest)
	
	fw.write_line("#" + " " + module.get_name())
	fw.write_line()
	
	if module.should_include_installation_instructions():
		
		ver = module.get_engine_version()
		if ver == common.engine_latest_version:
			ver = "latest"
		
		fw.write_line("## Installation")
		fw.write_line()
		fw.write_line("Before installing, you must be able to")
		fw.write_line("[compile Godot Engine](https://docs.godotengine.org/en/" + ver + "/development/compiling/)")
		fw.write_line("from source.")
		fw.write_line()
		
		fw.write_line("```bash")
		fw.write_line("# Copy the module under directory named " + module.get_short_name() + " (must be exactly that)")
		fw.write_line("cp " + module.get_short_name() + " <godot_path>/modules/" + module.get_short_name() + " && cd <godot_path>")
		fw.write_line("# Compile the engine manually, for instance:")
		fw.write_line("scons platform=linux target=release_debug bits=64")
		fw.write_line("```")
	
	fw.close()
	
	
def make_license(module):
	license_src = os.path.join(common.licenses_path, module.get_license()) + ".txt"
	license_dest = os.path.join(module.path, "LICENSE.txt")
	
	import datetime
	license_template = {
		"__YEAR__" : str(datetime.datetime.now().year),
		"__AUTHOR__" : module.get_author(),
	}
	tw = TemplateWriter(license_src, license_dest)
	tw.write_out(license_template)
	
	
def make_register_types(module):
	
	# Header
	reg_types_header_dest = os.path.join(module.path, "register_types.h")
	header = FileWriter(reg_types_header_dest)
	
	header.write_line("void register_" + module.get_short_name() + "_types();")
	header.write_line("void unregister_" + module.get_short_name() + "_types();")
	header.close()
	
	# Source
	reg_types_source_dest = os.path.join(module.path, "register_types.cpp")
	source = FileWriter(reg_types_source_dest)
	
	source.write_line("#include \"register_types.h\"")
	source.write_line()
	
	for c in module.get_classes():
		name = c['name']
		if not name:
			name = module.get_default_class_name()
		source.write_line("#include " + '\"' + name.lower() + ".h" + '\"')
		
	source.write_line()
	
	source.write_line("void register_" + module.get_short_name() + "_types() {")
	source.write_line()
	
	for c in module.get_classes():
		name = c['name']
		if not name:
			name = module.get_default_class_name()
		source.write_line("ClassDB::register_class<" + name + ">();", 1)
		
	source.write_line("}")
	source.write_line()
	
	source.write_line("void unregister_" + module.get_short_name() + "_types() {")
	source.write_line()
	source.write_line("// nothing to do here", 1)
	source.write_line("}")
	
	source.close()


def make_scsub(module):
	scsub_dest = os.path.join(module.path, "SCsub")
	
	scsub = FileWriter(scsub_dest)
	
	scsub.write_line("#!/usr/bin/env python")
	scsub.write_line()
	scsub.write_line("Import('env')")
	scsub.write_line("Import('env_modules')")
	scsub.write_line()

	env_module = "env_" + module.get_short_name()
	
	scsub.write_line(env_module + " = env_modules.Clone()")
	scsub.write_line()
	
	if module.get_thirdparty_path():
		scsub.write_line("# Thirdparty source files")
		scsub.write_line("thirdparty_dir = '" + module.get_thirdparty_path() + "/'")
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
		
	ver = module.get_engine_version(False)
	cpp_ver = module.get_cpp_version()
	
	if ver['major'] >= 3:
		if ver['minor'] >= 2 and cpp_ver == "c++11":
			pass # 3.2+ enables C++11 on the whole codebase by default
			# https://github.com/godotengine/godot/commit/5dae2ea777da5395cf1b1e9a8bc6abc93f6ae6bb
		else:
			scsub.write_line("if (not env.msvc):")
			scsub.write_line(env_module + ".Prepend(CXXFLAGS=['-std=" + cpp_ver + "'])", 1)
			scsub.write_line()
	
	scsub.write_line("# Module source files")
	scsub.write_line(env_module + ".add_source_files(env.modules_sources, '*.cpp')")
	
	scsub.close()
	
	
def make_classes(module):
	
	already_got_default = False
	
	for c_data in module.get_classes():
		name = c_data['name']
		if not name:
			if already_got_default:
				continue
			name = module.get_default_class_name()
			already_got_default = True
			
		inherits = c_data['inherits']
		
		# Header
		header_dest = os.path.join(module.path, name.lower() + '.h')
		write_class_header(header_dest, name, inherits)
		
		# Source
		source_dest = os.path.join(module.path, name.lower() + '.cpp')
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
	
	
def make_gdignore(module):
	gdignore_dest = os.path.join(module.path, ".gdignore")
	Path(gdignore_dest).touch()
