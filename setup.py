from setuptools import setup, find_packages

setup(
    name='pyimgresize',
    version='1.0',
    description='resize images in a folder while preserving aspect ratio',
    author='Daniel Baker',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    entry_points={
        'console_scripts': [
          'sortphotos = pyimgresize:main',
        ]
      }
)