import argparse

from gdgen import common
from gdgen import gdmodule

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('-n', '--name', default="")
	parser.add_argument('-s', '--internal-name', default="")

	parser.add_argument('-c', '--config-path', default=common.config_default_path)
	parser.add_argument('-o', '--output-path', default="")

	parser.add_argument('-f', '--force', action="store_true")

	module = parser.parse_args()

	gdmodule.init(module.name, module.internal_name, 
		module.config_path, module.output_path, module.force)
