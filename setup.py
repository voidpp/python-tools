from setuptools import setup, find_packages

setup(
    name = "voidpp-tools",
    desciption = "various python tools",
    version = "1.5.2",
    author = 'Lajos Santa',
    author_email = 'santa.lajos@coldline.hu',
    url = 'https://github.com/voidpp/python-tools.git',
    install_requires = [], # must be empty!
    scripts = [
    ],
    include_package_data = True,
    packages = find_packages(),
)
