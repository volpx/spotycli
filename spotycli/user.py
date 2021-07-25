"""User access and management"""

import spotycli.api_help

def set_parser(subparsers):
	parser_user=subparsers.add_parser('user',help='user utility')
	parser_user.add_argument('--list','-l',action='store_true',help='list user playlists')
	parser_user.set_defaults(func=m_user)

def m_user(args):
	if args.list:
		#list playlists
		playlists = get_playlists()
		print("Your playlists:")
		for el in playlists:
			print("id:",el["id"],"  name:",el["name"])

def get_playlists():
	"""Return an {id, name} array of dictionaries"""
	spotify = spotycli.api_help.get_spotify()
	user_id = spotify.current_user()["id"]
	results = spotify.user_playlists(user_id)

	playlists = results["items"]
	while results["next"]:
		results = spotify.next(results)
		playlists.extend(results["items"])

	playlist_names = [{"id": playlist["id"], "name": playlist["name"]} 
					  for playlist in playlists]
	return playlist_names
