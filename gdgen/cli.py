import os
import argparse

import gdgen

from gdgen import common
from gdgen import gdmodule


def main():
	# Parse
	parser = argparse.ArgumentParser()

	parser.add_argument('-n', '--name', default="")
	parser.add_argument('-s', '--internal-name', default="")

	parser.add_argument('-c', '--config-path', default=common.config_default_path)
	parser.add_argument('-o', '--output-path', default="")

	parser.add_argument('-f', '--force', action="store_true")

	args = parser.parse_args()
	
	# Load module config
	config = gdmodule.load_config(args.config_path)
	
	if args.name and args.internal_name:
		# Override
		config['name'] = args.name
		config['internal_name'] = args.internal_name
	else:
		# Wizard
		config['name'] = input("Module name: ")
		config['internal_name'] = input("Internal module name (snake_case): ")
		config['author'] = input("Author name: ")
		config['engine_version'] = input("Engine version (latest, 3.0, 3.1 ...): ")
		config['cpp_version'] = input("C++ version (c++11): ")
		config['num_classes'] = int(input("Number of classes to generate: "))
		
		classes = []
		for n in range(config['num_classes']):
			class_name = input("(%s) Class name: " % n)
			class_inherits = input("(%s) Class inherits: " % n)
			class_path = input("(%s) Class path: " % n)
			
			classes.append( {
					"name": class_name,
					"inherits": class_inherits,
					"path": class_path
				}
			)
		config['classes'] = classes
			
		config['docs_path'] = input("Documentation path: ")
		config['icons_path'] = input("Icons path: ")
		config['thirdparty_path'] = input("Thirdparty path: ")
		
		config['readme'] = input("Initialize README?: ")
		config['license'] = input("License: ")
		config['version_control'] = input("Version control system: ")
		config['to_be_included_inside_project'] = input("Will be included inside project?: ")
		
	# Validate config
	try:
		validate_config(config)
	except ValueError as e:
		print_info('config: ' + str(e))
		return
	
	# Generate
	gdmodule.init(config, args.output_path, args.force)
	
	
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
