import json

from django.conf.urls import url
from django.http import HttpResponse
from django.template import loader
from laconia import ThingFactory
from rdflib import Graph, URIRef


def post2graph(url, params):
    data = Graph()
    data.parse(format="json-ld", data=json.dumps({"@context": {"@vocab": url + "#"}}))
    return data


def resource(path_regex, method, handler, template_name):
    def view(request):
        if request.method == method:
            data = Graph()
            if method == "POST":
                data = post2graph(request.path, request.POST)
            graph = handler(data=data)
            template = loader.get_template(template_name)
            context = {"data": ThingFactory(graph)(URIRef(request.path))}
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse(status=405)

    return url(path_regex, view)
