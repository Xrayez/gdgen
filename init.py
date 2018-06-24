#!/usr/bin/env python3

'''
Initialize the module with a name
'''

import re
import os

TEMPLATE_REGISTER_TYPES = "TEMPLATE_REGISTER_TYPES"
TEMPLATE_CLASS = "TEMPLATE_CLASS"
TEMPLATE_HEADER = "TEMPLATE_HEADER"
TEMPLATE_SAFE_GUARD = "TEMPLATE_SAFE_GUARD"

def init(module_name):
	# Read register_types
	with open('register_types.h', 'r') as header:
		h = header.read()
	with open('register_types.cpp', 'r') as source:
		cpp = source.read()

	# Replace template stamps with the module's name

	lower_name = to_snake_case(module_name)
	upper_name = lower_name.upper()
	class_name = module_name[0].capitalize() + module_name[1:]

	h = h.replace(TEMPLATE_REGISTER_TYPES, lower_name)
	cpp = cpp.replace(TEMPLATE_REGISTER_TYPES, lower_name)
	cpp = cpp.replace(TEMPLATE_CLASS, class_name)
	cpp = cpp.replace(TEMPLATE_HEADER, lower_name + ".h")

	# Write register_types
	with open('register_types.h', 'w') as header:
		header.write(h)
	with open('register_types.cpp', 'w') as source:
		source.write(cpp)

	# Source files
	os.rename("class.cpp", lower_name + ".cpp")
	os.rename("class.h", lower_name + ".h")

	# Read source
	with open(lower_name + ".h", 'r') as header:
		h = header.read()
	with open(lower_name + ".cpp", 'r') as source:
		cpp = source.read()

	h = h.replace(TEMPLATE_SAFE_GUARD, upper_name)
	h = h.replace(TEMPLATE_CLASS, class_name)
	cpp = cpp.replace(TEMPLATE_HEADER, lower_name + ".h")
	cpp = cpp.replace(TEMPLATE_CLASS, class_name)

	# Write source
	with open(lower_name + ".h", 'w') as header:
		header.write(h)
	with open(lower_name + ".cpp", 'w') as source:
		source.write(cpp)

def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		name = sys.argv[1]
		init(name)
