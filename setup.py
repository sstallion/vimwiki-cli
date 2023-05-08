import os.path
from setuptools import find_packages, setup

dirname = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(dirname, 'README.md')) as f:
    long_description = f.read()

setup(name='vimwiki-cli',
      version='1.1.0',
      description='Vimwiki Command-Line Interface',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Steven Stallion',
      author_email='sstallion@gmail.com',
      url='https://github.com/sstallion/vimwiki-cli',
      packages=find_packages(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Text Editors',
          'Topic :: Text Editors :: Documentation'
      ],
      license='BSD-2-Clause',
      keywords='cli vim vimwiki wiki',
      install_requires=[
          'click>=7.1',
      ],
      entry_points={
          'console_scripts': [
              'vimwiki=vimwiki_cli.__main__:cli'
          ]
      },
      extras_require={
          'test': [
              'coverage~=5.5',
              'mock~=3.0',
              'pycodestyle~=2.7',
              'pytest>=4.6',
              'pytest-cov>=2.11'
          ],
          'release': [
              'build>=0.3.0',
              'bump2version>=1.0.0',
              'keepachangelog>=0.5.0'
          ]
      })
