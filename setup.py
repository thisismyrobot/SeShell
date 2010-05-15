from distutils.core import setup


setup(name='Probie',
      version='0.1',
      packages=['probie'],
      package_dir={'probie': 'src/probie'},
      package_data={'probie': ['README.txt']},
      author='Robert Wallhead',
      author_email='rwallhead@gmail.com',
      maintainer='Robert Wallhead',
      maintainer_email='rwallhead@gmail.com',
      long_description='Probie acts as a protocol bridge, mapping string commands to Python methods.',
      url='http://thisismyrobot.blogspot.com',
     )
