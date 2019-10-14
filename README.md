# Godot Module

*Version: 2.0-alpha*

An advanced, easy-to-use, configurable C++ module generator which can create 
necessary files to get started with module development for 
[Godot Engine 3.0+](https://github.com/godotengine/godot).

### Requirements

* Python 3.5+
* Git (optional)

### Usage

```bash
gdmodule.py [-n NAME] [-s INTERNAL_NAME] [-c CONFIG_PATH] [-o OUTPUT_PATH]
```

### Step-by-step

1. Fill out [configs/default.json](configs/default.json) to suite your needs.

2. Run `gdmodule.py`:

    ```bash
    python gdmodule.py
    ```
    
    Alternatively, pass additional arguments to output the generated module at 
    specified location, or use different configuration file:
    
    ```bash
    python gdmodule.py -o "~/src/godot/modules/" -c "~/my_config.json"
    ```

### Examples

```bash
# Use created config file and generate the module directly to Godot modules
gdmodule.py -c configs/test.json -o ~/src/godot/modules/

# Use default config file, but fill the required fields manually
gdmodule.py -n MyModule -s my_module
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
