from setuptools import find_packages, setup

setup(
    name='mpose',
    packages=find_packages(),
    version='1.0.4',
    description='MPOSE2021: a Dataset for Short-time Pose-based Human Action Recognition',
    author='Simone Angarano',
    license='MIT',
    install_requires=['numpy', 'tqdm', 'pyyaml', 'importlib_resources'],
    package_data={'': ["*.yaml"]}
)