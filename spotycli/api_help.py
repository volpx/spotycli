# -*- coding: utf-8 -*-
"""Functions to access and manage the API autentication and calls"""

import json
import spotipy

client_side_url = "http://127.0.0.1"
port = 8080
redirect_uri = "{}:{}/callback".format(client_side_url, port)
spotipy_api_scope = (
	"playlist-modify-public playlist-modify-private "
	"playlist-read-collaborative playlist-read-private")
cached_tokens='./.spotipyoauthcache'
config_file='./config.json'

def get_prefs():
	"""Get preferences json."""
	with open(config_file) as f:
		prefs = json.load(f)
	return prefs

def get_oauth():
	"""Return a Spotipy Oauth2 object."""
	prefs = get_prefs()
	return spotipy.oauth2.SpotifyOAuth(
		prefs["ClientID"], prefs["ClientSecret"], redirect_uri, 
		scope=spotipy_api_scope, cache_path=cached_tokens)

def get_spotify(auth_token=None):
	"""Return an authenticated Spotify object."""
	oauth = get_oauth()
	acc_token = oauth.get_access_token(as_dict=False)
	if not acc_token:
		# TODO: in my tests it never went here so 
		# I don't know exactly how to handle this
		acc_token=oauth.get_auth_response()
	return spotipy.Spotify(acc_token)
