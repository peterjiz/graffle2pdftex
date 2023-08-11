import os
import pathlib
import shutil

from setuptools import setup, find_packages
from setuptools.command.install import install


class CustomInstall(install):
    def run(self):
        # Run the standard install process
        install.run(self)

        self.copy_javascript_file()

    def copy_javascript_file(self):
        # Get the home directory
        home_directory = pathlib.Path.home()

        # Get the location of the installed package
        # scriptsPathLocal = pathlib.Path(os.path.abspath(__file__)).parent / "graffle2pdftex"
        scriptsPath = pathlib.Path(self.install_scripts)

        # Path to the OmniGraffle Automation JS file
        src = scriptsPath / "graffle2pdftex.omnijs"
        dest = home_directory / "Library/Containers/com.omnigroup.OmniGraffle7/Data/Library/Application Support/Plug-Ins/"
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dest)
        try:
            os.remove(str(scriptsPath / "graffle2pdftex.omnijs"))
        except Exception:
            pass


setup(
    name="graffle2pdftex",
    version="1.0.0",
    packages=find_packages(include=['graffle2pdftex', 'graffle2pdftex.*']),
    scripts=['graffle2pdftex/graffle2pdftex.applescript', 'graffle2pdftex/graffle2pdftex.omnijs'],
    # data_files=['graffle2pdftex/graffle2pdftex.applescript', 'graffle2pdftex/graffle2pdftex.omnijs'],
    cmdclass={
        'install': CustomInstall,
        'develop': CustomInstall,
    },
    install_requires=['appscript', 'pyobjc'],
    author="Peter El-Jiz",
    author_email="peter.eljiz@gmail.com",
    description="A command line utility that exports omnigraffle canvases files to pdf_tex.",
    long_description=open("README.md").read(),
    license="http://www.opensource.org/licenses/mit-license.php",
    keywords="graffle2pdftex",
    url="https://github.com/peterjiz/graffle2pdftex",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Operating System :: MacOS :: MacOS X',
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities"
    ],
    entry_points={
        'console_scripts': [
            'graffle2pdftex = graffle2pdftex.graffle2pdftex:main',
        ],
    },
    zip_safe=False,
)