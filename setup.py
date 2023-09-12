# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import importlib
import os
import sys

## Constants
CODE_DIRECTORY = 'spotycli'
DOCS_DIRECTORY = 'docs'
TESTS_DIRECTORY = 'tests'
PYTEST_FLAGS = ['--doctest-modules']

# Import metadata. Normally this would just be:
#
#     from spotycli import metadata
#
# However, when we do this, we also import `spotycli/__init__.py'. If this
# imports names from some other modules and these modules have third-party
# dependencies that need installing (which happens after this file is run), the
# script will crash. What we do instead is to load the metadata module by path
# instead, effectively side-stepping the dependency problem. Please make sure
# metadata has no dependencies, otherwise they will need to be added to
# the setup_requires keyword.
metadata_spec=importlib.util.spec_from_file_location(
	'metadata', os.path.join(CODE_DIRECTORY, 'metadata.py'))
metadata = importlib.util.module_from_spec(metadata_spec)
sys.modules['metadata'] = metadata
metadata_spec.loader.exec_module(metadata)

# import types
# loader = SourceFileLoader(filename, plugin_path)
# loaded = types.ModuleType(loader.name)
# loader.exec_module(loaded)

## Miscellaneous helper functions

def get_project_files():
	"""Retrieve a list of project files, ignoring hidden files.

	:return: sorted list of project files
	:rtype: :class:`list`
	"""
	if is_git_project() and has_git():
		return get_git_project_files()

	project_files = []
	for top, subdirs, files in os.walk('.'):
		for subdir in subdirs:
			if subdir.startswith('.'):
				subdirs.remove(subdir)

		for f in files:
			if f.startswith('.'):
				continue
			project_files.append(os.path.join(top, f))

	return project_files


def is_git_project():
	return os.path.isdir('.git')


def has_git():
	return bool(spawn.find_executable("git"))


def get_git_project_files():
	"""Retrieve a list of all non-ignored files, including untracked files,
	excluding deleted files.

	:return: sorted list of git project files
	:rtype: :class:`list`
	"""
	cached_and_untracked_files = git_ls_files(
		'--cached',  # All files cached in the index
		'--others',  # Untracked files
		# Exclude untracked files that would be excluded by .gitignore, etc.
		'--exclude-standard')
	uncommitted_deleted_files = git_ls_files('--deleted')

	# Since sorting of files in a set is arbitrary, return a sorted list to
	# provide a well-defined order to tools like flake8, etc.
	return sorted(cached_and_untracked_files - uncommitted_deleted_files)


def git_ls_files(*cmd_args):
	"""Run ``git ls-files`` in the top-level project directory. Arguments go
	directly to execution call.

	:return: set of file names
	:rtype: :class:`set`
	"""
	cmd = ['git', 'ls-files']
	cmd.extend(cmd_args)
	return set(subprocess.check_output(cmd).splitlines())


def print_success_message(message):
	"""Print a message indicating success in green color to STDOUT.

	:param message: the message to print
	:type message: :class:`str`
	"""
	try:
		import colorama
		print(colorama.Fore.GREEN + message + colorama.Fore.RESET)
	except ImportError:
		print(message)


def print_failure_message(message):
	"""Print a message indicating failure in red color to STDERR.

	:param message: the message to print
	:type message: :class:`str`
	"""
	try:
		import colorama
		print(colorama.Fore.RED + message + colorama.Fore.RESET,
			  file=sys.stderr)
	except ImportError:
		print(message, file=sys.stderr)


def read(filename):
	"""Return the contents of a file.

	:param filename: file path
	:type filename: :class:`str`
	:return: the file's content
	:rtype: :class:`str`
	"""
	with open(os.path.join(os.path.dirname(__file__), filename)) as f:
		return f.read()


def _lint():
	"""Run lint and return an exit code."""
	# Flake8 doesn't have an easy way to run checks using a Python function, so
	# just fork off another process to do it.

	# Python 3 compat:
	# - The result of subprocess call outputs are byte strings, meaning we need
	#   to pass a byte string to endswith.
	project_python_files = [filename for filename in get_project_files()
							if filename.endswith(b'.py')]
	retcode = subprocess.call(
		['flake8', '--max-complexity=10'] + project_python_files)
	if retcode == 0:
		print_success_message('No style errors')
	return retcode


def _test():
	"""Run the unit tests.

	:return: exit code
	"""
	# Make sure to import pytest in this function. For the reason, see here:
	# <http://pytest.org/latest/goodpractises.html#integration-with-setuptools-test-commands>  # NOPEP8
	import pytest
	# This runs the unit tests.
	# It also runs doctest, but only on the modules in TESTS_DIRECTORY.
	return pytest.main(PYTEST_FLAGS + [TESTS_DIRECTORY])


def _test_all():
	"""Run lint and tests.

	:return: exit code
	"""
	return _lint() + _test()

setup_dict=dict(
	name=metadata.package,
	version=metadata.version,
	description=metadata.description,
	long_description=open('README.md').read(),
	author=metadata.authors[0],
	author_email=metadata.emails[0],
	maintainer=metadata.authors[0],
	maintainer_email=metadata.emails[0],
	url=metadata.url,
	license=open('LICENSE').read(),
	# Find a list of classifiers here:
	# <http://pypi.python.org/pypi?%3Aaction=list_classifiers>
	classifiers=[
		'Development Status :: 1 - Planning',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GPLv3 License',
		'Natural Language :: English',
		'Operating System :: Linux',
		'Programming Language :: Python :: 3.9',
		'Programming Language :: Python :: 3.3'
	],
	packages=find_packages(exclude=(TESTS_DIRECTORY,)),
	# Allow tests to be run with `python setup.py test'.
	tests_require=[
		'pytest==2.5.1',
		'mock==1.0.1',
		'flake8==2.1.0',
	],
	entry_points={
		'console_scripts': [
			'spotycli_cli = spotycli.__main__:entry_point'
		],
		# if you have a gui, use this
		# 'gui_scripts': [
		#     'spotycli_gui = spotycli.gui:entry_point'
		# ]
	}
)

def main():
	setup(**setup_dict)

if __name__ == '__main__':
	main()

