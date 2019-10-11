#!/usr/bin/env python3

import os
import json
import argparse

import config
import builders
from vcs import get_providers as get_vcs_providers


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
	builders.make_config(module, module_path)
	
	if module['readme']['initialize']:
		builders.make_readme(module, module_path)
		
	if module['license']:
		builders.make_license(module, module_path)
		
	if module['version_control']:
		initialize_repository(module_path, module['version_control'])
		
		
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
