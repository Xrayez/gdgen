#!/usr/bin/env python3

import os
import json
import argparse

import common
from messages import *
from module import Module


def init(name, output_path, config_path, force=False):
	root_dir = os.getcwd()
	
	# Load module config
	try:
		with open(config_path) as config_data:
			config = json.load(config_data)
	except Exception as e:
		print_info('config: ' + str(e))
		return
		
	if output_path:
		module_path = os.path.join(output_path, config['short_name'])
	else:
		module_path = os.path.join(root_dir, config['short_name'])
	
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
		
		
def deinit(path):
	import shutil
	shutil.rmtree(path)


def print_info(msg):
	print(__file__ + ': ' + msg)
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	
	parser.add_argument('-n', '--name', default="")
	parser.add_argument('-o', '--output-path', default="")
	parser.add_argument('-c', '--config-path', default="configs/default.json")
	
	parser.add_argument('-f', '--force', action="store_true")
	
	module = parser.parse_args()
	init(module.name, module.output_path, module.config_path, module.force)
