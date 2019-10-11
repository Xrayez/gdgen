import subprocess
import os


class VCSProvider:
    
    @staticmethod
    def initialize(path):
        pass
    
    @staticmethod
    def get_name():
        return ''
        
    @classmethod
    def can_handle(cls, name):
        return cls.get_name() == name
    
    
class VCSGit(VCSProvider):
    
    @staticmethod
    def initialize(path):
        subprocess.run(['git', 'init'], cwd=path).check_returncode()
    
    @staticmethod
    def get_name():
        return 'git'
    
    
def get_providers():
    return [VCSGit]
