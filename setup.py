from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='nodata',
      version='0.4.2',
      description=u"Utilities for handling nodata",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Damon Burgett",
      author_email='damon@mapbox.com',
      url='https://github.com/mapbox/nodata',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'rasterio',
          'rio-mucho',
          'scipy',
          'raster-tester'
      ],
      extras_require={
          'test': ['pytest', 'pytest-cov'],
      },
      entry_points="""
      [console_scripts]
      nodata=nodata.scripts.cli:cli
      """
      )
