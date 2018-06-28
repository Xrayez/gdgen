# Godot module template

A simple template that can generate necessary files to get started with module
development for Godot Engine by running `init.py MyModule`

Supported versions:
* Godot 3.0 and higher

## Usage

1. Decide on the module's name. We'll be using `MyModule` as an example.

2. Change directory to godot's modules folder:

```bash
cd godot/modules/
```

3. Clone the template into `my_module` directory (notice snake_case):

```bash
git clone https://github.com/Xrayez/godot-module-template.git my_module
```

4. Run `init.py` to initialize the template with a module's name. This will
replace placeholders in register_types.h/cpp source files with a chosen name and
will create simple class that extends `Reference`:

    `python init.py MyModule`

    Module name `MyModule` must be camel-case, with first letter capitalized.

Remove .git folder in case you want to apply version control to your module
and adapt README.md and LICENSE.md to your needs.

## When things go wrong

If you've immediately decided to change the module's name (class), run these git
commands to reset the template to its original state:

```bash
git reset --hard HEAD # or git stash
git clean -f # deletes generated header and source files
```