# GDGen

[![Build Status](https://travis-ci.com/Xrayez/gdgen.svg?branch=master)](https://travis-ci.com/Xrayez/gdgen)

*Version: 1.0-alpha*

An advanced, configurable code generator which aims to automate some aspects of
[Godot Engine](https://github.com/godotengine/godot) development, namely:

- [x] creating C++ modules;
- [ ] creating GDNative plugins.

Currently only C++ module generation is supported, so most of the functionallity 
is revolving around modules.

## Requirements

* Python 3.6+
* Git (optional)

## Compatibility

* Godot Engine 3.0+ (C++ modules generation)

## Installation

```bash
pip install git+https://github.com/Xrayez/gdgen
```

## Usage

```bash
gdgen [-n NAME] [-s INTERNAL_NAME] [-c CONFIG_PATH] [-o OUTPUT_PATH]
```

## Examples
For most use cases, you can use a simple wizard. Here's an example output:
```
$ ~/src/godot/modules> gdgen

Module name: My awesome module
Internal module name (snake_case): my_module
Author name (default - You): Me
Engine version (default - latest): 3.1
C++ version (default - c++11): c++20
Number of classes to generate (default - 0): 1
(0) Class name: NewNode
(0) Class inherits: Node
(0) Class path (default - ):
Documentation path (default - docs): doc_classes
Icons path (default - editor/icons): icons
Thirdparty path (default - thirdparty):
Initialize README? (default - True):
License (default - MIT):
Version control system (default - git):
Will be included inside project? (default - False): True
Initialized empty Git repository in ~/src/godot/modules/my_module/.git/
```

You can also create your own configuration file:
```bash
gdgen -c tests/configs/sample.json -o ~/src/godot/modules/
```

Use default config file, but fill the required fields manually:
```bash
gdgen -n MyModule -s my_module
```

# Config

Name|Description
-----|-----
`name`|(Required) Descriptive name of the module.
`internal_name`|(Required) The name used by the engine for the module to compile. This name is used by default for any unnamed `classes` to be generated later (see below).
`author`|The name that will be used to place inside license text. If not set explicitly, the generator is going to attempt to retrieve one with the help of supported version control provider. In case of `git`, it will use `git config user.name` value.
`engine_version`|The engine target version used to generate compatible module.
`cpp_version`|The C++ version to compile module-specific source files.
`classes`|An optional array to generate Godot classes. Available fields: `name` - the class name; `inherits` - one of the base (Godot) core classes; `path` - relative base directory to generate classes in.
`docs_path`|If set, configures the module to use module-specific documentation for `classes`.
`icons_path`|If set, configures the module to use module-specific editor icons for `classes`.
`thirdparty_path`|If set, configures the module to apply common operations on third-party code (disabling warnings etc).
`readme`|If `true`, initializes a barebones README file with module installation instructions.
`license`|If set, creates LICENSE file with current year and author substituted from available license templates.
`version_control`|If set, attempts to initialize the module with version control provider of choice.
`to_be_included_inside_project`|If `true`, creates `.gdignore` file so that the module can be included inside regular Godot project (for instance, prevents `*.obj` build files to be wrongly recognized and imported as 3D models).
