from gdgen import methods

includes = {}
types = {}


def update(module):
	# In that order
	update_types(module)
	make_includes(module)


def update_types(module):
	global types
	types.clear()
	
	ver = module.get_engine_version(False)
	
	basedir = ""
	
	if ver['major'] >= 3:
		if ver['minor'] >= 1:
			# https://github.com/godotengine/godot/pull/21978
			basedir = "core/"
			
		types['Object'] = basedir
		types['Reference'] = basedir
		types['Resource'] = basedir
		
		basedir = "scene/main/"
		types['Node'] = basedir
		
		basedir = "scene/2d/"
		types['Node2D'] = basedir


def make_includes(module):
	global includes 
	includes.clear()
	
	include_str = "#include \"%s%s.h\""
	
	for t, basedir in types.items():
		class_type = methods.to_snake_case(t)
		includes[t] = include_str % (basedir, class_type)


def get_include(class_type):
	if class_type in includes:
		return includes[class_type]
	else: # fallback
		include_str = "#include \"%s.h\""
		return include_str % methods.to_snake_case(class_type)
