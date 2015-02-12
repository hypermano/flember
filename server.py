#!/usr/bin/python3
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for

from data.snippet import Snippet, SnippetRegistry
from rest.decorators import *

app = Flask(__name__)

registry = SnippetRegistry()

@app.route('/snippets', methods=['POST'])
@JsonResponse("snippet")
def addSnippet():
    return registry.add(Snippet(request.json['snippet']['text']))

@app.route('/snippets')
@JsonResponse("snippets", lambda x: [dict(y) for y in x])
def getSnippets():
    return registry.getAll()

@app.route('/snippets/<id>')
@JsonResponse("snippet")
@ValidatedResource(404)
def getSnippet(id):
    return registry.get(id)

@app.route('/snippets/<id>', methods=['PUT'])
@JsonResponse("snippet")
@ValidatedResource(404)
def updateSnippet(id):
    return registry.updateText(id, request.json['snippet']['text'])

@app.route('/snippets/<id>', methods=['DELETE'])
@JsonResponse("snippet")
@ValidatedResource(404)
def removeSnippet(id):
    return registry.remove(id)
    
@app.route('/snippets/<id>/subpath', methods=['GET', 'POST'])
def subPathSnippet(id):
    d = request.form

    subpath = d['snip_subpath']

    snippet = _getSnippet(id)

    if (snippet):
        if (subpath):
            return "OK"
        else:
            abort(401)
    else:
        abort(404)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)