# Godot module template

A simple template that can be used as a starting point for module development.

Supported versions:
* Godot 3.0 and higher

## Usage

1. Clone the template into `my_class` directory:

    `git clone https://github.com/Xrayez/godot-module-template.git [my_class]`

2. Run `init.py` to initialize the template with a module's name. This will
replace placeholders in register_types.h/cpp source files with a chosen name and
will create simple class that extends `Reference`:

    `python init.py MyClass`

    Module name `MyClass` must be camel-case, with first letter capitalized.

3. Remove .git folder in case you want to apply version control to your module.

4. Adapt README.md and LICENSE.md to your needs.
