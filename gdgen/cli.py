#!/usr/bin/env python3

import os
import argparse

import gdgen

from gdgen import common
from gdgen import gdmodule
from gdgen.module import Module


def main():
	# Parse command line arguments
	parser = argparse.ArgumentParser()

	parser.add_argument('-n', '--name', default="")
	parser.add_argument('-s', '--internal-name', default="")

	parser.add_argument('-c', '--config-path', default=common.config_default_path)
	parser.add_argument('-o', '--output-path', default="")

	parser.add_argument('-f', '--force', action="store_true")

	args = parser.parse_args()
	
	# Load config
	config = gdmodule.load_config(args.config_path)
	
	if args.name and args.internal_name:
		# Override
		config['name'] = args.name
		config['internal_name'] = args.internal_name
	else:
		try:
			# Run wizard
			while config.get('name') == None or config.get('name') == "":
				config['name'] = read_input("Module name")
				
			while config.get('internal_name') == None or config.get('internal_name') == "":
				config['internal_name'] = read_input("Internal module name (snake_case)")
			
			config['author'] = read_input("Author name", Module.get_default_author())
			config['engine_version'] = read_input("Engine version", Module.get_default_engine_version())
			config['cpp_version'] = read_input("C++ version", Module.get_default_cpp_version())
			
			num_classes = read_input("Number of classes to generate", 0)
			if not num_classes:
				num_classes = 0
			
			classes = []
			for n in range(int(num_classes)):
				class_name = read_input("(%s) Class name" % n)
				class_inherits = read_input("(%s) Class inherits" % n)
				class_path = read_input("(%s) Class path" % n, "")
				
				classes.append( {
						"name": class_name,
						"inherits": class_inherits,
						"path": class_path
					}
				)
			config['classes'] = classes
			
			config['docs_path'] = read_input("Documentation path", Module.get_default_docs_path())
			config['icons_path'] = read_input("Icons path", Module.get_default_icons_path())
			config['thirdparty_path'] = read_input("Thirdparty path", Module.get_default_thirdparty_path())
			
			config['readme'] = read_input("Initialize README?", True)
			config['license'] = read_input("License", Module.get_default_license())
			config['version_control'] = read_input("Version control system", Module.get_default_vcs())
			config['to_be_included_inside_project'] = read_input("Will be included inside project?", False)
			
		except KeyboardInterrupt:
			print_info("\nSkipping the wizard.")
	
	# Validate config
	try:
		validate_config(config)
	except ValueError as e:
		print_info(str(e).lower())
		return
	
	# Generate
	gdmodule.init(config, args.output_path, args.force)
	
	
def read_input(prompt, default_value=None):
	if default_value != None:
		msg = "%s (default - %s): " % (prompt, str(default_value))
	else:
		msg = "%s: " % (prompt)
		
	value = input(msg)
	if not value:
		value = default_value
		
	return value
	
	
def validate_config(config):
	required = [
		'name', 
		'internal_name'
	]
	validated = []
	
	for param in config:
		if param in required:
			validated.append(param)
	
	if len(validated) != len(required):
		missing = set(required) - set(validated)
		raise ValueError("Missing required fields in config: %s" % missing)
	
	for param in required:
		if not config[param]:
			raise ValueError("Required config parameter not set: %s" % param)


def print_info(msg):
	print(__file__ + ': ' + msg)
