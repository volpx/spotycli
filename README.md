# Spotycli

Command line utility for managing your spotify.

## Why

I started this project to bypass the shuffle function of spotify, so that is the first feature that it does. As of now it just does that but the lower api plumbing is there to expand the functionalities.

## No Installation

To test it without installing I use conda to manage my environment:

	conda create -n spotycli pip
	conda activate spotycli
	pip install -r requirements.txt

And use it from the root folder with:

	python -m spotycli [args]

Copy the `config_example.json` to `config.json`.

### API token

For writing API calls you need a developer token to place inside the `config.json`.

To get one go to [the dev page](https://developer.spotify.com) and create an app.

Put the "Redirect URI" to `http://127.0.0.1:8080/callback`.

## Running

First time running it tries to authenticate, It tries to open a Firefox tab but to me it didn't work if you already have Firefox open, so close it and run.

## What it does as of now

- Randomize a playlist (since spotify shuffle doesn't work)

## TODO

- Save playlist
- Add to playlist