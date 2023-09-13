"""Song management"""

import spotycli.settings

def set_parser(subparsers):
	parser_track=subparsers.add_parser('track',help='track utility')
	parser_track.set_defaults(func=m_track)

def m_track():
    pass

def set_like(track_ID,spotify=None):
	if not spotify:
		spotify = spotycli.api_help.get_spotify()
	spotify.current_user_saved_tracks_add(tracks=[track_ID])
	if spotycli.settings.verbose >= 2:
		print('Liked ',track_ID)