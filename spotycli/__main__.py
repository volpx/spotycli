#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Program entry point"""

import argparse
import sys

import spotycli.settings
from spotycli import metadata
from spotycli.api_help import config_file
import spotycli.user
import spotycli.playlist

spotycli.settings.init()

author_strings = []
for name, email in zip(metadata.authors, metadata.emails):
	author_strings.append('Author: {0} <{1}>'.format(name, email))
epilog = '''
{project} v{version}

{authors}
URL: <{url}>
'''.format(
	project=metadata.project,
	version=metadata.version,
	authors='\n'.join(author_strings),
	url=metadata.url)

def main(argv):
	global config_file
	global epilog
	"""Program entry point.

	:param argv: command-line arguments
	:type argv: :class:`list`
	"""


	# Argument parser
	parser = argparse.ArgumentParser(
		prog=argv[0],
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=metadata.description,
		epilog=epilog)
	parser.add_argument(
		'--version',
		action='version',
		version=metadata.version)
	parser.add_argument(
		'--verbose',
		'-v',
		action='count',
		default=spotycli.settings.verbose)
	parser.add_argument(
		'--config-file',
		action='store',
		default=config_file,
		help='config file to use instead of default')
	parser.set_defaults(func=m_default)
	subparsers = parser.add_subparsers(help='sub-command help')

	# User parser
	spotycli.user.set_parser(subparsers)

	# Playlist parser
	spotycli.playlist.set_parser(subparsers)

	# Config parser
	parser_playlist=subparsers.add_parser('config',help='config utility')
	parser_playlist.set_defaults(func=m_config)

	args=parser.parse_args()

	spotycli.settings.verbose=args.verbose
	if spotycli.settings.verbose>=2:
		print(args)
	config_file=args.config_file
	
	# Call the subroutine
	args.func(args)
	return 0

def m_default(args):
	pass
def m_config(args):
	pass

def entry_point():
	"""Zero-argument entry point for use with setuptools/distribute."""
	raise SystemExit(main(sys.argv))


if __name__ == '__main__':
	entry_point()
