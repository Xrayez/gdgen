import os

import builders
from vcs import get_providers as get_vcs_providers


class Module:
    def __init__(self, config, module_path):
        self.config = config
        self.module_path = module_path
        
    # Generate methods
    def generate(self):
	
        # Initialize directory structure
        os.makedirs(self.module_path)
        
        if self.get_thirdparty_path():
            thirdparty_dir = os.path.join(self.module_path, self.get_thirdparty_path())
            os.makedirs(thirdparty_dir)

        ### Generate!
        
        # Essential
        builders.make_config(self, self.module_path)
        builders.make_register_types(self, self.module_path)
        builders.make_scsub(self, self.module_path)
        
        builders.make_classes(self, self.module_path)
        
        # Optional
        if self.should_initialize_readme():
            builders.make_readme(self, self.module_path)
            
        if self.get_license():
            builders.make_license(self, self.module_path)
        
        if self.get_vcs():
            initialize_repository(self.module_path, self.get_vcs())
        
    # Config methods
        
    def get_name(self):
        return self.config['name']
        
    def get_short_name(self):
        return self.config['short_name']
        
    def get_author(self):
        return self.config['author']
        
    def get_engine_version(self):
        return self.config['engine_version']
        
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
        
    def should_include_inside_project(self):
        return self.config['should_include_inside_project']


def initialize_repository(module_path, vcs_name):
	
	for vcs in get_vcs_providers():
		if not vcs.can_handle(vcs_name):
			continue
		vcs.initialize(module_path)
