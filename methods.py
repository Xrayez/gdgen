import re

def to_snake_case(camel):
	# https://stackoverflow.com/a/33516645/
    return re.sub(r'([A-Z]*)([A-Z][a-z]+)', lambda x: (x.group(1) + '_' if x.group(1) else '') + x.group(2) + '_', camel).rstrip('_').lower()
	
	
def to_pascal_case(snake):
	# https://stackoverflow.com/a/19053800/
    comp = snake.split('_')
    return comp[0].title() + ''.join(x.title() for x in comp[1:])
