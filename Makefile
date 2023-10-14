#!/usr/bin/env make

extract-raw-data:
	@mkdir -p data/raw
	@PYTHONUNBUFFERED=true poetry run python setup/extract-raw-data.py | tee data/raw/extraction.log

parse-and-store:
	poetry run python setup/parse-and-store-data.py

create-plots:
	PYTHONPATH=src poetry run python -m app

#show-plots:
#	bash tests/scripts/show-plots.bash
