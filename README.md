# [WIP] Godot module generator

*Version:* 2.0-dev

## Notice

For previous stable version please checkout the 
[1.0 branch](https://github.com/Xrayez/godot-module/tree/1.0). This version aims
to provide more versitile and configurable generator which is currently in development.

## Description

An advanced, easy-to-use, configurable C++ module generator which can create 
necessary files to get started with module development for 
[Godot Engine](https://github.com/godotengine/godot).

### Requirements

* Python 3.5+

### Usage

```bash
python init.py [-o <output_path>]  [-c <custom_config_path>]
```

### Step-by-step

1. Fill out [configs/default.json](configs/default.json) to suite your needs.
   The first two fields are required to fill:
   * `name` - descriptive name of the module;
   * `internal_name` - internal name of the module (lowercase);
   * `author` - your name, organization's name etc (optional).

2. Run `init.py`:

    ```bash
    python init.py
    ```
    
    Optionally, pass additional arguments to output the generated module at 
    specified location, or use different configuration file:
    
    ```bash
    python init.py -o "~/src/godot/modules/" -c "~/my_config.json
    ```
