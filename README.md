# Godot module template

A simple template that can be used as a starting point for module development.

Supported versions: 
* Godot 3.0 and higher

## Usage

1. Clone the template into `module_name` directory:

    `git clone https://github.com/Xrayez/godot-module-template.git [module_name]`

2. Run `init.py` to initialize the template with a module's name. This will 
replace placeholders in register_types.h/cpp source files with a chosen name:

    `python init.py <module_name>`

    You can run this command multiple times if you decided to change the name.

3. Remove .git folder from the root of the module and:

    `git init`

4. Adapt README.md and LICENSE.md to your needs.
