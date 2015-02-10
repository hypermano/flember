#!/usr/bin/python3
from flask import Flask
from flask import render_template
from flask import request
from flask import abort, redirect, url_for
from flask import json
from functools import wraps

app = Flask(__name__)

snippets = {}

class Snippet:
    def __init__(self, id, text):
        self.id = id
        self.text = text
        self.path = []

    def subPath(self, subpath):
        self.path.append(subpath)

    def __iter__(self):
        yield('id', self.id)
        yield('text', self.text)

def ValidatedResource(code):
    def wrap(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            res = f(*args, **kwargs)
            if (not res):
                abort(code)
            else:
                return res
        return wrapped_f
    return wrap

def JsonResponse(container):
    def wrap(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            res = f(*args, **kwargs)

            jsonArgs = {container: dict(res)}

            return json.jsonify(**jsonArgs)
        return wrapped_f
    return wrap

def _getSnippet(id):
    try:
        return snippets[int(id)]
    except:
        return None

# POST SNIPPET
@app.route('/snippets', methods=['POST'])
def addSnippet():
    sid = len(snippets)
    snippet = Snippet(sid, request.json['snippet']['text'])

    snippets[sid] = snippet

    return json.jsonify(snippet=dict(snippet))

# GET ALL SNIPPETS
@app.route('/snippets')
def getSnippets():
    retVal = []
    for (id, snippet) in snippets.items():
        retVal.append(dict(snippet))
    return json.jsonify(snippets=retVal)

# GET SNIPPET BY ID
@app.route('/snippets/<id>')
@JsonResponse("snippet")
@ValidatedResource(404)
def getSnippet(id):
    return _getSnippet(id)

# PUT SNIPPET BY ID
@app.route('/snippets/<id>', methods=['PUT'])
@JsonResponse("snippet")
@ValidatedResource(404)
def updateSnippet(id):
    snippet = _getSnippet(id)
     
    if (snippet):
        snippet.text = request.json['snippet']['text']
    
    return snippet

# DELETE SNIPPET BY ID
@app.route('/snippets/<id>', methods=['DELETE'])
@JsonResponse("snippet")
@ValidatedResource(404)
def removeSnippet(id):
    snippet = _getSnippet(id)
    if (snippet):
        del snippets[int(id)]
        
    return snippet

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