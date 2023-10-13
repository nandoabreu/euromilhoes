#!/usr/bin/env make

scrap:
	poetry run python setup/scrap.py

plots:
	PYTHONPATH=src poetry run python -m app

show-plots:
	bash tests/scripts/show-plots.bash