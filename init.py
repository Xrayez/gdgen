#!/usr/bin/env python3

import os
import json
import argparse
import datetime

from builders import TemplateWriter
from builders import FileWriter

from vcs import get_providers as get_vcs_providers

import config


def init(name, output_path, config_path):
	root_dir = os.getcwd()
	
	# Load config
	try:
		with open(config_path) as config_data:
			module = json.load(config_data)
	except Exception as e:
		print_info('config: ' + str(e))
		return
		
	# Create folder
	if output_path:
		module_path = os.path.join(output_path, module['short_name'])
	else:
		module_path = os.path.join(root_dir, module['short_name'])
	
	try:
		os.makedirs(module_path)
	except FileExistsError:
		print_info("Module already exists at specified path.")
		pass

	# Generate
	if module['readme']['initialize']:
		make_readme(module, module_path)
		
	if module['license']:
		make_license(module, module_path)
		
	if module['version_control']:
		initialize_repository(module_path, module['version_control'])
	
	
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
	
	license_template = {
		"__YEAR__" : str(datetime.datetime.now().year),
		"__AUTHOR__" : module['author'],
	}
	tw = TemplateWriter(license_src, license_dest)
	tw.write_out(license_template)
	
	
def initialize_repository(module_path, vcs_name):
	
	for vcs in get_vcs_providers():
		if not vcs.can_handle(vcs_name):
			continue
		vcs.initialize(module_path)
	
		
def open_utf8(filename, mode):
	return open(filename, mode, encoding="utf-8")
		
	
def print_info(msg):
	print(__file__ + ': ' + msg)
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	
	parser.add_argument('-n', '--name', default="")
	parser.add_argument('-o', '--output-path', default="")
	parser.add_argument('-c', '--config-path', default="configs/default.json")
	
	module = parser.parse_args()
	init(module.name, module.output_path, module.config_path)
