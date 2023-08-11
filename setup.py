# import os
# import pathlib
#
# from setuptools import setup, find_packages
# from pkg_resources import resource_filename
#
# from setuptools import setup
# from setuptools.command.install import install
# import os
# import shutil
#
# class CustomInstall(install):
#     def run(self):
#         # Perform standard installation
#         install.run(self)
#
#         # Custom installation steps
#         self.copy_javascript_file()
#
#     def copy_javascript_file(self):
#         # Define the source and destination paths
#         src = pathlib.Path(self.install_lib) / 'graffle2pdftex/graffle2pdftex.omnijs'
#         home_directory = pathlib.Path(os.path.expanduser("~"))
#         dest = home_directory / "Library/Containers/com.omnigroup.OmniGraffle7/Data/Library/Application Support/Plug-Ins/"
#         dest.mkdir(parents=True, exist_ok=True)
#
#         # Copy the JavaScript file
#         shutil.copy(str(src), str(dest))
#
# def read(fname):
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()
#
# setup (
#     name = "graffle2pdftex",
#     version = "1.0.0",
#     packages = find_packages(exclude='tests'),
#     # package_data={'graffle2pdftex': ['scripts/*.js', 'scripts/*.scpt']},
#     cmdclass={'install': CustomInstall},
#     install_requires = ['appscript','pyobjc'],
#     author = "Peter El-Jiz",
#     author_email = "peter.eljiz@gmail.com",
#     description = "A command line utility that exports omnigraffle canvases files to pdf_tex.",
#     long_description = read("README.md"),
#     license = "http://www.opensource.org/licenses/mit-license.php",
#     keywords = "graffle2pdftex",
#     url = "https://github.com/peterjiz/graffle2pdftex",
#     classifiers=[
#         "Development Status :: 5 - Production/Stable",
#         'Operating System :: MacOS :: MacOS',
#         "Environment :: Console",
#         "License :: OSI Approved :: MIT License",
#         "Programming Language :: Python :: 3.9",
#         "Topic :: Utilities"
#     ],
#     entry_points = {
#         'console_scripts': [
#             'graffle2pdftex = graffle2pdftex:main',
#         ],
#     },
#     test_suite = 'tests',
#     zip_safe = True,
# )

#
# import os
# from pathlib import Path
# from setuptools import setup, find_packages
# from setuptools.command.install import install
# import shutil
#
# from pkg_resources import resource_filename
#
# class CustomInstall(install):
#     def run(self):
#         # Perform standard installation
#         install.run(self)
#
#         # Custom installation steps
#         self.copy_javascript_file()
#
#     def copy_javascript_file(self):
#         # Define the source and destination paths
#         src = Path(self.install_lib) / 'graffle2pdftex/graffle2pdftex/graffle2pdftex.omnijs'
#         src = resource_filename('graffle2pdftex', 'graffle2pdftex/graffle2pdftex.omnijs')
#         home_directory = Path(os.path.expanduser("~"))
#         dest = home_directory / "Library/Containers/com.omnigroup.OmniGraffle7/Data/Library/Application Support/Plug-Ins/"
#         dest.mkdir(parents=True, exist_ok=True)
#
#         # Copy the JavaScript file
#         shutil.copy(str(src), str(dest))
#
# def read(fname):
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()
#
# setup(
#     name="graffle2pdftex",
#     version="1.0.0",
#     packages=find_packages(exclude='tests'),
#     package_data={'graffle2pdftex': ['graffle2pdftex/*.applescript', 'graffle2pdftex/*.omnijs']},
#     cmdclass={'install': CustomInstall},
#     install_requires=['appscript', 'pyobjc'],
#     author="Peter El-Jiz",
#     author_email="peter.eljiz@gmail.com",
#     description="A command line utility that exports omnigraffle canvases files to pdf_tex.",
#     long_description=read("README.md"),
#     license="http://www.opensource.org/licenses/mit-license.php",
#     keywords="graffle2pdftex",
#     url="https://github.com/peterjiz/graffle2pdftex",
#     classifiers=[
#         "Development Status :: 5 - Production/Stable",
#         'Operating System :: MacOS :: MacOS',
#         "Environment :: Console",
#         "License :: OSI Approved :: MIT License",
#         "Programming Language :: Python :: 3.9",
#         "Topic :: Utilities"
#     ],
#     entry_points={
#         'console_scripts': [
#             'graffle2pdftex = graffle2pdftex.graffle2pdftex:main',
#         ],
#     },
#     test_suite='tests',
#     zip_safe=True,
# )

# from setuptools import setup, find_packages
# from setuptools.command.install import install
# from pathlib import Path
# import shutil
#
# class CustomInstall(install):
#     def run(self):
#         install.run(self)
#         self.copy_javascript_file()
#
#     def copy_javascript_file(self):
#         src = Path(self.install_lib) / 'graffle2pdftex/graffle2pdftex.omnijs'
#         home_directory = Path.home()
#         dest = home_directory / "Library/Containers/com.omnigroup.OmniGraffle7/Data/Library/Application Support/Plug-Ins/"
#         dest.mkdir(parents=True, exist_ok=True)
#         shutil.copy(src, dest)
#
# setup(
#     name="graffle2pdftex",
#     version="1.0.0",
#     packages=find_packages(include=['graffle2pdftex', 'graffle2pdftex.*']),
#     package_data={'graffle2pdftex': ['*.applescript', '*.omnijs']},
#     # cmdclass={'install': CustomInstall},
#     install_requires=['appscript', 'pyobjc'],
#     author="Peter El-Jiz",
#     author_email="peter.eljiz@gmail.com",
#     description="A command line utility that exports omnigraffle canvases files to pdf_tex.",
#     long_description=open("README.md").read(),
#     license="http://www.opensource.org/licenses/mit-license.php",
#     keywords="graffle2pdftex",
#     url="https://github.com/peterjiz/graffle2pdftex",
#     classifiers=[
#         "Development Status :: 5 - Production/Stable",
#         'Operating System :: MacOS :: MacOS X',
#         "Environment :: Console",
#         "License :: OSI Approved :: MIT License",
#         "Programming Language :: Python :: 3.9",
#         "Topic :: Utilities"
#     ],
#     entry_points={
#         'console_scripts': [
#             'graffle2pdftex = graffle2pdftex.graffle2pdftex:main',
#         ],
#     },
#     zip_safe=False,
# )


from setuptools import setup

setup(
    name='graffle2pdftex',
    version='0.1',
    description='A Python package to convert OmniGraffle diagrams to PDFTeX.',
    url='https://github.com/peterjiz/graffle2pdftex',
    author='Your Name',
    author_email='youremail@example.com',
    license='MIT',
    packages=['graffle2pdftex'],
    scripts=['graffle2pdftex/graffle2pdftex.applescript'],
    data_files=[('~/Library/Containers/com.omnigroup.OmniGraffle7/Data/Library/Application Support/Plug-Ins', ['graffle2pdftex/graffle2pdftex.omnijs'])],
)