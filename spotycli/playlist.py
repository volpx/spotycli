"""Playlist access and management"""

import spotycli.settings
import spotycli.user
import spotycli.api_help

import random

def set_parser(subparsers):
	parser_playlist=subparsers.add_parser('playlist',help='playlist utility')
	parser_playlist.add_argument('playlistID',help='playlists to work on')
	parser_playlist.add_argument('--no-read-only',action='store_true',help='don\'t modify the playlist, throw error')
	parser_playlist.add_argument('--randomize',action='store_true',help='randomize user playlists')
	parser_playlist.add_argument('--outID',help='output playlist')
	parser_playlist.set_defaults(func=m_playlist)

def m_playlist(args):
	if args.randomize:
		in_id=args.playlistID
		if args.outID:
			out_id=args.outID
		else:
			out_id=in_id
		if (in_id == out_id) and (not args.no_read_only):
			print('Going to modify read only playlist, exiting.')
			exit(1)
		randomize(in_id,out_id)

def randomize(in_id,out_id):
	"""Randomize a playlist from a given source one."""

	spotify = spotycli.api_help.get_spotify()
	in_playlist = spotify.playlist(in_id)
	out_playlist = spotify.playlist(out_id)
	current_user=spotify.current_user()
	if out_playlist['owner']['id'] != current_user['id']:
		print('Cannot modify a playlist which is not yours.')

	# Get all the tracks
	# Spotify returns results in a pager,
	# get chunks of 100 items until finished.
	ret = in_playlist["tracks"]
	tracks = ret["items"]
	while ret["next"]:
		ret = spotify.next(ret)
		tracks.extend(ret["items"])

	if spotycli.settings.verbose >=2:
		in_owner = in_playlist['owner']
		print('Input playlist\n\tby {} ( {} )\n\tname {} ( {} )\n\tlen {}'.format(
			in_owner['display_name'] , in_owner['id'],
			in_playlist['name'],in_playlist['id'],len(tracks)))
		out_owner = out_playlist['owner']
		print('Output playlist\n\tby {} ( {} )\n\tname {} ( {} )'.format(
			out_owner['display_name'] , out_owner['id'],
			out_playlist['name'],out_playlist['id']))

	# Begin the shuffle
	shuffled_sequence = list(range(len(tracks)))
	random.shuffle(shuffled_sequence)
	track_names_id = [
		(track["track"]["name"], track["track"]["id"]) 
		for track in tracks]
	shuffled_id = [track_names_id[i][1] for i in shuffled_sequence]
	ids_portions=list(generate_portions(shuffled_id,100))
	
	n=0
	# Replace only first time to delete existing
	rc=spotify.user_playlist_replace_tracks(out_playlist['owner']['id'],out_playlist['id'],ids_portions[0])
	n+=len(ids_portions[0])
	if spotycli.settings.verbose >= 2:
		print(n, rc)
	for ids_portion in ids_portions[1:]:
		rc=spotify.user_playlist_add_tracks(out_playlist['owner']['id'],out_playlist['id'],ids_portion)
		n += len(ids_portion)
		if spotycli.settings.verbose >=2:
			print(n, rc)
	
	print("Done reshuffling {} tracks!".format(n))

def generate_portions(elements,portion_length):
	N=len(elements)
	i=0
	output = []
	while i < N:
		output.append(elements[i])
		if len(output) == portion_length or i == N-1:
			yield output
			output = []
		i+=1