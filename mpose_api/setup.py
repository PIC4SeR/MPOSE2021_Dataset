from setuptools import find_packages, setup

try:
    with open('README.md') as f:
        long_description = f.read()
except:
    long_description = ''
    
setup(
    name='mpose',
    packages=['mpose'],
    version='1.2',
    description='MPOSE2021: a Dataset for Short-time Pose-based Human Action Recognition',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important!
    author='Simone Angarano',
    author_email='simone.angarano@polito.it',
    license='MIT',
    install_requires=['numpy', 'tqdm', 'pyyaml', 'importlib_resources', 'matplotlib'],
    package_data={'': ["*.yaml"]},
    url='https://pypi.org/project/mpose/'
)
