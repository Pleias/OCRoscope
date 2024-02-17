from setuptools import setup, find_packages

setup(
    name='OCRoscope',
    version='0.1.0',
    description='A Python package for OCR evaluation metrics',
    author='Pierre-Carl Langlais',
    url='https://github.com/Pleias/OCRoscope',
    packages=find_packages(),
    install_requires=[
        'pycld2'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
)
