
class Module:
    def __init__(self, config):
        self.config = config
        
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
