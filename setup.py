import os
from setuptools import setup, Distribution


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""

    def has_ext_modules(foo):
        return True


def find_package_data():
    """
    Recursively include all files in the dependencies directory.
    This ensures the JRE and QPS binaries downloaded during CI are included.
    """
    files = []
    # relative to the package inside src/quarchpy_binaries/
    base_dir = os.path.join('src', 'quarchpy_binaries', 'dependencies')

    if not os.path.exists(base_dir):
        # Fallback for local dev if dependencies aren't downloaded yet
        return {'quarchpy_binaries': []}

    # We want the pattern to be like 'dependencies/jre/bin/java'
    # relative to the package root 'quarchpy_binaries'
    data_files = []
    for root, dirs, filenames in os.walk(base_dir):
        for filename in filenames:
            abs_path = os.path.join(root, filename)
            # Make path relative to src/quarchpy_binaries
            rel_path = os.path.relpath(abs_path, os.path.join('src', 'quarchpy_binaries'))
            data_files.append(rel_path)

    return {'quarchpy_binaries': data_files}


setup(
    distclass=BinaryDistribution,
    package_data=find_package_data(),
    include_package_data=True,
)