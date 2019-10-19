from unittest import TestCase
import os

import gdgen
from gdgen import gdmodule


class GDModuleTest(TestCase):
    
    modules_dir = os.path.join(gdgen.get_path(), "tests/modules/")
    
    sample_config = "tests/configs/sample.json"

    @classmethod
    def setUpClass(cls):
        import shutil
        shutil.rmtree(cls.modules_dir, True)
        os.makedirs(cls.modules_dir)
    
    
    def test_init_from_default_config(self):
        config = gdmodule.load_config(gdmodule.get_default_config_path())
        config['name'] = "Default Module 3D"
        config['internal_name'] = "default_module_3d"
        gdmodule.init(config, self.modules_dir)
        
        self.current_dir = "default_module_3d/"
        
        self.should_exist('docs/')
        self.should_exist('editor/icons/')
        self.should_exist('thirdparty/')
        self.should_exist('.gitattributes')
        self.should_exist('.gitignore')
        self.should_exist('config.py')
        self.should_exist('default_module_3d.cpp')
        self.should_exist('default_module_3d.h')
        self.should_exist('LICENSE.txt')
        self.should_exist('README.md')
        self.should_exist('register_types.cpp')
        self.should_exist('register_types.h')
        self.should_exist('SCsub')
        
        self.should_not_exist('.gdignore')
        self.should_not_exist('classes/')
        
    
    def test_init_from_minimal_config(self):
        config = gdmodule.load_config(gdmodule.get_minimal_config_path())
        config['name'] = "Minimal Module"
        config['internal_name'] = "MINIMAL_MODULE"
        gdmodule.init(config, self.modules_dir)
    
        self.current_dir = "minimal_module/"
        
        self.assertTrue('minimal_module' in os.listdir(self.modules_dir), "Case mismatch detected!")
        
        self.should_exist('config.py')
        self.should_exist('register_types.cpp')
        self.should_exist('register_types.h')
        self.should_exist('SCsub')
        
        self.should_not_exist('docs/')
        self.should_not_exist('editor/icons/')
        self.should_not_exist('thirdparty/')
        self.should_not_exist('.gitattributes')
        self.should_not_exist('.gitignore')
        self.should_not_exist('.gdignore')
        self.should_not_exist('classes/')
        self.should_not_exist('minimal_module.cpp')
        self.should_not_exist('minimal_module.h')
        self.should_not_exist('LICENSE.txt')
        self.should_not_exist('README.md')
    
    
    def test_init_from_sample_config(self):
        config = gdmodule.load_config(self.sample_config)
        config['name'] = "Sample Module 2D"
        config['internal_name'] = "sample_module_2D"
        gdmodule.init(config, self.modules_dir)
        
        self.current_dir = "sample_module_2d/"
        
        self.assertTrue('sample_module_2d' in os.listdir(self.modules_dir), "Case mismatch detected!")
        
        self.should_exist('.git')
        
        self.should_exist('classes_a/')
        self.should_exist('classes_a/new_node_2d.cpp')
        self.should_exist('classes_a/new_node_2d.h')
        
        self.should_exist('classes_b/')
        self.should_exist('classes_b/new_reference.cpp')
        self.should_exist('classes_b/new_reference.h')
        
        self.should_exist('docs/')
        self.should_exist('editor/icons/')
        self.should_exist('thirdparty/')
        self.should_exist('.gdignore')
        self.should_exist('.gitattributes')
        self.should_exist('.gitignore')
        self.should_exist('config.py')
        self.should_exist('LICENSE.txt')
        self.should_exist('README.md')
        self.should_exist('register_types.cpp')
        self.should_exist('register_types.h')
        self.should_exist('sample_module_2d.cpp')
        self.should_exist('sample_module_2d.h')
        self.should_exist('SCsub')
        
        
    def exists(self, path):
        return os.path.exists(self.modules_dir + self.current_dir + path)
        
        
    def should_exist(self, path):
        return self.assertTrue(self.exists(path))
        
        
    def should_not_exist(self, path):
        return self.assertFalse(self.exists(path))
        

if __name__ == '__main__':
    from unittest import main
    main()
