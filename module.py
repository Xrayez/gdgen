import os

import common
import builders
from vcs import get_providers as get_vcs_providers


class Module:
    def __init__(self, config, path):
        self.config = config
        self.path = path
        
    # Generate methods
    def generate(self):
	
        # Initialize directory structure
        os.makedirs(self.path)
        
        if self.get_thirdparty_path():
            thirdparty_dir = os.path.join(self.path, self.get_thirdparty_path())
            os.makedirs(thirdparty_dir)

        ### Generate!
        
        # Essential
        builders.make_config(self)
        builders.make_register_types(self)
        builders.make_scsub(self)
        
        builders.make_classes(self)
        
        # Optional
        if self.should_initialize_readme():
            builders.make_readme(self)
            
        if self.get_license():
            builders.make_license(self)
            
        if self.to_be_included_inside_project():
            builders.make_gdignore(self)
        
        if self.get_vcs():
            self.initialize_repository()
    
    def initialize_repository(self):
        
        for vcs in get_vcs_providers():
            if not vcs.can_handle(self.get_vcs()):
                continue
            vcs.initialize(self.path)

    # Config methods
        
    def get_name(self):
        return self.config['name']
        
    def get_short_name(self):
        return self.config['short_name']
        
    def get_author(self):
        return self.config['author']
        
    def get_engine_version(self, as_string=True):
        
        if not as_string:
            ver_str = self.config['engine_version']
            
            if ver_str == 'latest':
                ver_str = common.engine_latest_version
                
            ver_comp = ver_str.split('.')
            ver = {
                'major': int(ver_comp[0]),
                'minor': int(ver_comp[1]),
            }
            return ver
            
        return self.config['engine_version']
        
    def get_cpp_version(self):
        return self.config['cpp_version'].lower()
        
    def get_classes(self):
        return self.config['classes']
        
    def get_docs_path(self):
        return self.config['docs_path']
        
    def get_icons_path(self):
        return self.config['icons_path']
        
    def get_thirdparty_path(self):
        return self.config['thirdparty_path']
        
    def should_initialize_readme(self):
        return self.config['readme']['initialize']
        
    def should_include_installation_instructions(self):
        return self.config['readme']['include_installation_instructions']
        
    def get_license(self):
        return self.config['license']
        
    def get_vcs(self):
        return self.config['version_control']
        
    def get_changelog(self):
        return self.config['changelog']
        
    def get_ci(self):
        return self.config['continuous_integration']
        
    def to_be_included_inside_project(self):
        return self.config['to_be_included_inside_project']
    
    # Config utility methods
    
    def get_default_class_name(self):
	    return ''.join(x for x in self.get_short_name().title() if not x.isspace())
    