class Snippet:
    def __init__(self, text):
        self._id = None

        self.text = text
        self.path = []

    def subPath(self, subpath):
        self.path.append(subpath)

    def __iter__(self):
        """Iterable for snippet, used to dictionarize for JSON"""
        yield('id', self._id)
        yield('text', self.text)

class SnippetRegistry:
    def __init__(self):
        self._registry = {}
        self._nextIdInt = 0

    def _nextId(self):
        """Generates the next available Id for a snippet"""
        res = self._nextIdInt
        self._nextIdInt += 1
        return res

    def _assertId(self, snippet, id):
        assert snippet._id == int(id)

    def add(self, snippet):
        """Adds the snippet to the registry, populating its id in the process"""
        snippet._id = self._nextId()
        self._registry[snippet._id] = snippet

        return snippet

    def get(self, id):
        """Retrieves a snippet by the given Id"""
        try:
            return self._registry[int(id)]
        except:
            return None

    def getAll(self):
        """Retrieves all the snippets in the system"""
        return list(self._registry.values())

    def updateText(self, id, newText):
        """Updates the Snippet's text entry for id with a new value"""
        snippet = self.get(id)

        if (snippet):
            self._assertId(snippet, id)

            snippet.text = newText

        return snippet

    def remove(self, id):
        snippet = self.get(id)

        if (snippet):
            self._assertId(snippet, id)
            
            del self._registry[int(id)]

        return snippet