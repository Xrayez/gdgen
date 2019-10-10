#!/usr/bin/env python3

import os
import json
import argparse
import datetime

from builders import TemplateWriter

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

	write_license(module, module_path)
	
	
def write_license(module, module_path):
	license_src = os.path.join(config.licenses_path, module['license']) + ".txt"
	license_dest = os.path.join(module_path, "LICENSE.txt")
	
	license_template = {
		"__YEAR__" : str(datetime.datetime.now().year),
		"__AUTHOR__" : module['author'],
	}
	tw = TemplateWriter(license_src, license_dest)
	tw.write_out(license_template)
	
		
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
