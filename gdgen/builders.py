import re
import os
from pathlib import Path

import gdgen
from gdgen import common
from gdgen import methods
from gdgen import gdtypes


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


def configure(module):
	gdtypes.update(module)


def make_config(module):
	config_dest = os.path.join(module.path, "config.py")
	config = FileWriter(config_dest)
	
	config.write_line()
	
	ver = module.get_engine_version(False)
	if ver['major'] >= 3:
		# 3.0 vs 3.1: https://github.com/godotengine/godot/pull/19275
		if ver['minor'] >= 1:
			config.write_line("def can_build(env, platform):")
		else:
			config.write_line("def can_build(env):")
	
		config.write_line("return True", 1)
		config.write_line()

	config.write_line("def configure(env):")
	config.write_line("pass", 1)
	config.write_line()
	
	if module.get_docs_path():
		config.write_line("def get_doc_path():")
		config.write_line("return \"" + module.get_docs_path() + "\"", 1)
		config.write_line()
		
		config.write_line("def get_doc_classes():")
		config.write_line("return [", 1)
		
		for c in module.get_classes():
			name = c['name']
			if not name:
				name = module.get_default_class_name()
			config.write_line('\"' + name + '\"' + ',', 2)
			
		config.write_line("]", 1)
		config.write_line()
		
	if module.get_icons_path():
		config.write_line("def get_icons_path():")
		config.write_line("return \"" + module.get_icons_path() + "\"", 1)
		config.write_line()
		
	config.close()

	
def make_readme(module):
	readme_dest = os.path.join(module.path, "README.md")
	readme = FileWriter(readme_dest)
	
	readme.write_line("#" + " " + module.get_name())
	readme.write_line()
	
	ver = module.get_engine_version()
	if ver == common.engine_latest_version:
		ver = "latest"
	
	readme.write_line("## Installation")
	readme.write_line()
	readme.write_line("Before installing, you must be able to")
	readme.write_line("[compile Godot Engine](https://docs.godotengine.org/en/" + ver + "/development/compiling/)")
	readme.write_line("from source.")
	readme.write_line()
	
	readme.write_line("```bash")
	readme.write_line("# Copy the module under directory named " + module.get_internal_name() + " (must be exactly that)")
	readme.write_line("cp " + module.get_internal_name() + " <godot_path>/modules/" + module.get_internal_name() + " && cd <godot_path>")
	readme.write_line("# Compile the engine manually, for instance:")
	readme.write_line("scons platform=linux target=release_debug bits=64")
	readme.write_line("```")
	
	readme.close()
	
	
def make_license(module, author):
	license_src = os.path.join(gdgen.get_path(), common.licenses_path, module.get_license()) + ".txt"
	license_dest = os.path.join(module.path, "LICENSE.txt")
	
	import datetime
	license_template = {
		"__YEAR__" : str(datetime.datetime.now().year),
		"__AUTHOR__" : author,
	}
	license_text = TemplateWriter(license_src, license_dest)
	license_text.write_out(license_template)
	
	
def make_register_types(module):
	
	# Header
	reg_types_header_dest = os.path.join(module.path, "register_types.h")
	header = FileWriter(reg_types_header_dest)
	
	header.write_line("void register_" + module.get_internal_name() + "_types();")
	header.write_line("void unregister_" + module.get_internal_name() + "_types();")
	header.close()
	
	# Source
	reg_types_source_dest = os.path.join(module.path, "register_types.cpp")
	source = FileWriter(reg_types_source_dest)
	
	source.write_line("#include \"register_types.h\"")
	source.write_line()
	
	for c in module.get_classes():
		name = methods.to_snake_case(c['name'])
		if not name:
			name = module.get_default_class_underscore_name()
		source.write_line("#include " + '\"' + name + ".h" + '\"')
		
	source.write_line()
	
	source.write_line("void register_" + module.get_internal_name() + "_types() {")
	source.write_line()
	
	for c in module.get_classes():
		name = c['name']
		if not name:
			name = module.get_default_class_name()
		source.write_line("ClassDB::register_class<" + name + ">();", 1)
		
	source.write_line("}")
	source.write_line()
	
	source.write_line("void unregister_" + module.get_internal_name() + "_types() {")
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

	env_module = "env_" + module.get_internal_name()
	
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
	
	scsub.write_line("source_dirs = [")
	
	for path in module.get_source_dirs():
		if not path:
			continue
		scsub.write_line("\"" + path + "/" + "\"" + ",", 1)
		
	scsub.write_line("]")
	
	scsub.write_line(env_module + ".Prepend(CPPPATH=source_dirs)")
	scsub.write_line("sources = [Glob(d + \"*.cpp\") for d in source_dirs]")
	scsub.write_line()
		
	scsub.write_line(env_module + ".add_source_files(env.modules_sources, sources)")
	
	scsub.close()
	
	
def make_classes(module):
	
	already_got_default = False
	
	for c_data in module.get_classes():
		name = c_data['name']
		
		if not name: # get default
			if already_got_default:
				continue
			class_name = module.get_default_class_name()
			underscore_name = module.get_internal_name()
			
			already_got_default = True
		else:
			class_name = name
			underscore_name = methods.to_snake_case(class_name)
			
		inherits = c_data['inherits']
		class_dir = os.path.join(module.path, c_data['path'])
		
		if not os.path.exists(class_dir):
			os.makedirs(class_dir)
			
		# Header
		header_dest = os.path.join(class_dir, underscore_name + '.h')
		write_class_header(header_dest, class_name, underscore_name, inherits)
		
		# Source
		source_dest = os.path.join(class_dir, underscore_name + '.cpp')
		write_class_source(source_dest, class_name, underscore_name, inherits)
		
		
def write_class_header(header_dest, name, underscore_name, inherits):
	
	header = FileWriter(header_dest)
	
	HEADER_GUARD = underscore_name.upper()
	
	header.write_line("#ifndef " + HEADER_GUARD + "_H")
	header.write_line("#define " + HEADER_GUARD + "_H")
	header.write_line()
	
	header.write_line(gdtypes.get_include(inherits))
	header.write_line()
	
	header.write_line("class " + name + " : " + "public " + inherits + " {")
	header.write_line("GDCLASS(" + name + ", " + inherits + ");", 1)
	header.write_line()
	
	header.write_line("protected:")
	header.write_line("static void _bind_methods();", 1)
	
	header.write_line("};")
	header.write_line()
	
	header.write_line("#endif " + "// " + HEADER_GUARD + "_H")
	
	header.close()
	
	
def write_class_source(source_dest, name, underscore_name, inherits):
	
	source = FileWriter(source_dest)
	
	source.write_line("#include " + '\"' + underscore_name + ".h" + '\"')
	source.write_line()
	
	source.write_line("void " + name + "::_bind_methods() {")
	source.write_line()
	source.write_line("}")
	
	source.close()
	
	
def make_gdignore(module):
	gdignore_dest = os.path.join(module.path, ".gdignore")
	Path(gdignore_dest).touch()
