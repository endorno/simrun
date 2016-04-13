from setuptools import setup, find_packages

setup(name='simrun',
      version='0.0.1',
      description='simulator run tool',
      author='teppei.fujisawa',
      author_email='teppei.fujisawa@gmail.com',
      url='https://github.com/endorno',
      packages=find_packages(),
      install_requires=[
        'cement',
      ],
      entry_points="""
      [console_scripts]
      simrun = simrun.cli:main
      """,
      )