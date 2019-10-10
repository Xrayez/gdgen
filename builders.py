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
	

class FileWriter:
	dest = ''
	
	def __init__(self, dest, enc="utf-8"):
		self.dest = dest
		self.f = open(dest, "w", encoding=enc)
		
	def write_line(self, line=""):
		self.f.write(line + "\n")
		
	def close(self):
		self.f.close()
