# Spotycli

## No Installation

To test it without installing I use conda to manage my environment:

	conda create -n spotycli pip
	conda activate spotycli
	pip install -r requirements.txt

And use it from the root folder with:

	python -m spotycli [args]

## Running

First time running it tries to authenticate, 
It tries to open a Firefox tab but to me it didn't work 
if you already have Firefox open, so close it and run.