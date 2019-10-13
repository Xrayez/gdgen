# Include type information

includes = {}

def update_includes(module):
	global includes 
	includes.clear()
	
	ver = module.get_engine_version(False)
	
	include_str = "#include \"%s.h\""
	basedir = ""
	
	if ver['major'] >= 3:
		# Core
		if ver['minor'] >= 1:
			# https://github.com/godotengine/godot/pull/21978
			basedir = "core/"
			
		includes['Object'] = include_str % "%sobject" % basedir
		includes['Reference'] = include_str % "%sreference" % basedir
		includes['Resource'] = include_str % "%sresource" % basedir
		
		# Scene
		includes['Node'] = include_str % "scene/main/node"
		includes['Node2D'] = include_str % "scene/2d/node_2d"


def get_include(class_type):
	if class_type in includes:
		return includes[class_type]
	else: # fallback
		return "#include " + "\"" + to_snake_case(class_type) + ".h\""
