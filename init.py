#!/usr/bin/env python3

import os
import json
import argparse

import common
from messages import *
from module import Module


def init(name, internal_name, config_path, output_path, force=False):
	# Load module config
	try:
		with open(config_path) as config_data:
			config = json.load(config_data)
	except Exception as e:
		print_info('config: ' + str(e))
		return
		
	# Override some required config values if set via command line
	if name:
		config['name'] = name
	if internal_name:
		config['internal_name'] = internal_name
	
	# Validate config
	try:
		validate_config(config)
	except ValueError as e:
		print_info('config: ' + str(e))
		return
		
	if output_path:
		module_path = os.path.join(output_path, config['internal_name'])
	else:
		module_path = os.path.join(os.getcwd(), config['internal_name'])
	
	# Generate module
	m = Module(config, module_path)
	try:
		if os.path.exists(module_path) and force:
			deinit(module_path)
		m.generate()
		
	except Exception as e:
		print_info(str(e))
		if not force:
			print_info(INFO_PASS_FORCE_CMD)
		return


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
	
		
def deinit(path):
	import shutil
	shutil.rmtree(path)


def print_info(msg):
	print(__file__ + ': ' + msg)
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	
	parser.add_argument('-n', '--name', default="")
	parser.add_argument('-s', '--internal-name', default="")
	
	parser.add_argument('-c', '--config-path', default="configs/default.json")
	parser.add_argument('-o', '--output-path', default="")
	
	parser.add_argument('-f', '--force', action="store_true")
	
	module = parser.parse_args()
	
	init(module.name, module.internal_name, 
			module.config_path, module.output_path, module.force)
