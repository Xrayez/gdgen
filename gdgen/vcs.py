import subprocess
import os

import gdgen

from gdgen import common
from gdgen.builders import TemplateWriter


class VCSProvider:
    
    @classmethod
    def initialize(cls, path):
        pass
    
    @staticmethod
    def get_name():
        return ''
    
    @classmethod
    def get_templates_path(cls):
        return ''
        
    @classmethod
    def can_handle(cls, name):
        return cls.get_name() == name
        
    @staticmethod
    def get_author():
        return ""
    
    
class VCSGit(VCSProvider):
    
    @classmethod
    def initialize(cls, path):
        subprocess.run(['git', 'init'], cwd=path).check_returncode()
        
        templates = os.listdir(cls.get_templates_path())
        
        for f in templates:
            src = os.path.join(cls.get_templates_path(), f)
            dest = os.path.join(path, f)
            
            tw = TemplateWriter(src, dest)
            tw.write_out()
        
    @staticmethod
    def get_name():
        return 'git'
        
    @classmethod
    def get_templates_path(cls):
        return os.path.join(gdgen.get_path(), common.vcs_path, cls.get_name())
        
    @staticmethod
    def get_author():
        git_author = ['git', 'config', 'user.name']
        output = subprocess.check_output(git_author, shell=True)
        author = output.decode("utf-8").strip("\n")
        return author
        
    
def get_providers():
    return [VCSGit]
