#!/usr/bin/env make

extract-raw-data:
	@mkdir -p data/raw
	@PYTHONUNBUFFERED=true poetry run python setup/extract_raw_data.py | tee data/raw/extraction.log

parse-and-store:
	@PYTHONUNBUFFERED=true poetry run python setup/parse-and-store-data.py | tee data/raw/storage.log

create-plots:
	@PYTHONPATH=src poetry run python -m app

#show-plots:
#	bash tests/scripts/show-plots.bash
