from distutils.core import setup
import setuptools

setup(
    name='lightText',
    version='0.0.0.0',
    description= "lightsmile's text library",
    author='lightsmile',
    author_email='iamlightsmile@gmail.com',
    url='https://github.com/smilelight/lightText',
    packages=setuptools.find_packages(),
    install_requires=[
        'torchtext>=0.4.0',
        'tqdm>=4.28.1',
        'torch>=1.0.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
)
