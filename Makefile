checkfiles = fastapi_monitor/ tests/ examples/ conftest.py
black_opts = -l 100 -t py38
py_warn = PYTHONDEVMODE=1

up:
	@poetry update

deps:
	@poetry install

style: deps
	isort -src $(checkfiles)
	black $(black_opts) $(checkfiles)

check: deps
	black --check $(black_opts) $(checkfiles)
	flake8 $(checkfiles)
	mypy $(checkfiles)

test: deps
	$(py_warn) pytest

ci: check test

build: deps
	@poetry build
