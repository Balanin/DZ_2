from setuptools import setup, find_packages


setup(name='clean_folder',
      version='1.9',
      packages = find_packages(), 
      description='Very useful code',
      long_description=open('README.md').read(),
      author='Volodymyr Balan',
      author_email='vova.balan1988@gmail.com',
      #license='MIT',
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}

      )