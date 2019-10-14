import os

import common
import methods
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
        
        if self.get_docs_path():
            docs_dir = os.path.join(self.path, self.get_docs_path())
            os.makedirs(docs_dir)
            
        if self.get_icons_path():
            icons_dir = os.path.join(self.path, self.get_icons_path())
            os.makedirs(icons_dir)
        
        if self.get_thirdparty_path():
            thirdparty_dir = os.path.join(self.path, self.get_thirdparty_path())
            os.makedirs(thirdparty_dir)

        ### Generate!
        builders.configure(self)
        
        # Essential
        builders.make_config(self)
        builders.make_register_types(self)
        builders.make_scsub(self)
        
        builders.make_classes(self)
        
        # Optional
        if self.should_initialize_readme():
            builders.make_readme(self)
            
        if self.get_license():
            author = self.get_author()
            
            if not author: # try harder
                for vcs in get_vcs_providers():
                    author = vcs.get_author()
                    if author:
                        break
            
            builders.make_license(self, author)
            
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
        
    def get_internal_name(self):
        return self.config['internal_name'].lower()
        
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
        return self.config['readme']
        
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
        return methods.to_pascal_case(self.get_internal_name())
        
    def get_default_class_underscore_name(self):
	    return methods.to_snake_case(self.get_internal_name())
        
    def get_source_dirs(self):
        dirs = {}
        for c in self.get_classes():
            path = c['path']
            dirs[path] = True
        return dirs
