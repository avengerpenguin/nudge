.PHONY: clean test deploy-test deploy-live

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/py.test
PEP8 := $(VENV)/bin/pep8
ZAPPA := $(VENV)/bin/zappa

PYSRC := $(shell find nudge -iname '*.py' ; find test -iname '*.py')


###############
# Boilerplate #
###############

default: test

clean:
	rm -rf htmlcov .coverage .eggs results node_modules


##############
# Virtualenv #
##############

$(VENV)/deps.touch: $(PIP) requirements.txt
	$(PIP) install -r requirements.txt
	touch $(VENV)/deps.touch

$(VENV)/bin/%: $(PIP)
	$(PIP) install $*

$(VENV)/bin/py.test: $(PIP)
	$(PIP) install pytest pytest-cov pytest-xdist pytest-django

$(PYTHON) $(PIP):
	virtualenv venv
	$(PIP) install virtualenv

$(VENV)/bin/pip-sync $(VENV)/bin/pip-compile: $(PIP)
	$(PIP) install --upgrade pip setuptools pip-tools

requirements.txt: requirements.in venv/bin/pip-compile
	venv/bin/pip-compile requirements.in


################
# Code Quality #
################

pep8.errors: $(PEP8) $(PYSRC)
	$(PEP8) --exclude="venv" . | tee /pep8.errors || true


################
# Unit Testing #
################

test: $(PYSRC) $(PYTHON) venv/bin/pip-sync requirements.txt $(PYTEST)
	source venv/bin/activate \
	    && venv/bin/pip-sync \
        && export DJANGO_SETTINGS_MODULE=nudge.settings.pytest \
        && $(PYTEST) --ds nudge.settings.pytest test/*.py



run: $(PYSRC) $(PYTHON) venv/bin/pip-sync requirements.txt $(PYTEST) manage.py
	source venv/bin/activate \
	    && venv/bin/pip-sync \
	    && export DJANGO_SETTINGS_MODULE=nudge.settings.local \
	    && $(PYTHON) manage.py runserver


##############
# Deployment #
##############

$(ZAPPA):
	$(PIP) install zappa

deploy-test: $(PIP) test requirements.txt
	source venv/bin/activate \
	    && venv/bin/pip-sync \
        && export DJANGO_SETTINGS_MODULE=nudge.settings.test \
        && $(PYTHON) manage.py deploy test

deploy-live: $(PIP) test requirements.txt
	source venv/bin/activate \
	    && venv/bin/pip-sync \
        && export DJANGO_SETTINGS_MODULE=nudge.settings.live \
        && $(PYTHON) manage.py deploy live
