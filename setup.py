from setuptools import setup, find_packages

setup(
    name = "voidpp-tools",
    description = "various python tools",
    version = "1.8.0",
    author = 'Lajos Santa',
    author_email = 'santa.lajos@coldline.hu',
    url = 'https://github.com/voidpp/python-tools.git',
    install_requires = [], # must be empty!
    scripts = [
    ],
    include_package_data = True,
    packages = find_packages(),
)
