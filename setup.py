import os
from setuptools import setup, find_packages, Distribution

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.universal = False
        def get_tag(self):
            # This forces the 'py3-none' part while keeping the OS platform
            python, abi, plat = _bdist_wheel.get_tag(self)
            return "py3", "none", plat
except ImportError:
    bdist_wheel = None

class BinaryDistribution(Distribution):
    """Force a binary package with platform name"""
    def has_ext_modules(foo):
        return True

def find_package_data():
    base_dir = os.path.join('src', 'quarchpy_binaries', 'dependencies')
    if not os.path.exists(base_dir):
        return []

    data_files = []
    for root, dirs, filenames in os.walk(base_dir):
        for filename in filenames:
            abs_path = os.path.join(root, filename)
            # Path relative to the package: quarchpy_binaries/
            rel_path = os.path.relpath(abs_path, os.path.join('src', 'quarchpy_binaries'))
            data_files.append(rel_path)
    return data_files

setup(
    # Name and version must be here to ensure they aren't 'UNKNOWN' 
    # during the bdist_wheel phase if pyproject.toml isn't parsed early enough.
    name="quarchpy-binaries",
    version="0.0.4",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    distclass=BinaryDistribution,
    package_data={'quarchpy_binaries': find_package_data()},
    include_package_data=True,
    cmdclass={'bdist_wheel': bdist_wheel} if bdist_wheel else {},
)
