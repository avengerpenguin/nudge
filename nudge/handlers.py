from rdflib import Graph

from nudge import models


def dashboard(data=None):
    return Graph()


def collect(data=None):
    new_stuff = models.Stuff()
    models.User('foo').stuff.add()