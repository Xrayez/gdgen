import re
import os

class TemplateWriter:
	src = ''
	dest = ''
	
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		
	def write_out(self, template):
		with open(self.src, 'r') as src_template:
			text = src_template.read()

		for placeholder, value in template.items():
			text = text.replace(placeholder, value)
		
		with open(self.dest, 'w') as dest_file:
			dest_file.write(text)
	