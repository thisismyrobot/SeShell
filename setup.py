from distutils.core import setup


setup(name='Probie',
      version='0.1',
      py_modules=['probie'],
      package_data={'': ['README.txt']},
      author='Robert Wallhead',
      author_email='rwallhead@gmail.com',
      maintainer='Robert Wallhead',
      maintainer_email='rwallhead@gmail.com',
      long_description='Probie acts as a protocol bridge, mapping string commands to Python methods.',
     )
