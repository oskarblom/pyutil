#coding: utf-8

try:
    import simplejson as json
except ImportError:
    import json

import urllib
from urllib2 import Request, urlopen, HTTPError

class HttpRequest(Request):

    def __init__(self, method, *args, **kwargs):
        Request.__init__(self, *args, **kwargs)
        self.method = method

    def get_method(self):
        return self.method

class HttpResponse(object):

    def __init__(self, code, data):
        self.code = code
        self.data = data

class HttpContentType(object):
    TEXT = "text/plain"
    JSON = "application/json"
    HTML = "text/html"
    FORM = "application/x-www-form-urlencoded"

class HttpContent(object):

    def __init__(self, content_type, data):
        self.content_type = content_type
        self.data = data

    def get_encoded(self):
        if self.content_type in (HttpContentType.TEXT, HttpContentType.HTML):
            return self.data
        elif self.content_type == HttpContentType.JSON:
            return json.dumps(self.data)
        elif self.content_type == HttpContentType.FORM:
            return urllib.urlencode(self.data)
        else:
            return ""

class HttpClient(object):
    """ Http client with no external dependencies.
    Simple at the expense of completeness. No keep-alive or other fancy stuff """

    def __init__(self, base_url=None):
        self.base_url = base_url

    def get(self, url, content=None, headers=None):
        return self._do_request("GET", url, content, headers)

    def post(self, url, content=None, headers=None):
        return self._do_request("POST", url, content, headers)

    def delete(self, url, content=None, headers=None):
        return self._do_request("DELETE", url, content, headers)

    def put(self, url, content=None, headers=None):
        return self._do_request("PUT", url, content, headers)

    def _do_request(self, req_type, url, content=None, headers=None):
        if not headers:
            headers = {}

        if content:
            if hasattr(content, "get_encoded"):
                content_type = content.content_type
                data = content.get_encoded()
            elif isinstance(content, dict):
                if headers["Content-Type"] == HttpContentType.JSON:
                    data = json.dumps(content)
                else:
                    # Assume form
                    content_type = HttpContentType.FORM
                    data = urllib.urlencode(content)
            else:
                # Assume string
                content_type = HttpContentType.TEXT
                data = content

            if "Content-Type" not in headers:
                headers["Content-Type"] = content_type

        else:
            data = None

        if self.base_url:
            url = self.base_url + url

        req = HttpRequest(req_type, url, data=data)
        req.headers = headers

        try:
            response = urlopen(req)
            code = response.getcode()
            data = response.read()
        except HTTPError, e:
            code = e.code
            data = None

        return HttpResponse(code, data)

if __name__ == "__main__":

    client = HttpClient("http://localhost:5000")
    methods = (client.get, client.post, client.put, client.delete)
    endpoint = "/test"

    for method in methods:

        response = method(endpoint)
        print str(response.code) + " - " + response.data

        content = HttpContent(HttpContentType.TEXT, "this is testdata")
        response = method(endpoint, content)
        print str(response.code) + " - " + response.data

        content = HttpContent(HttpContentType.JSON, {"foo": "bar"})
        response = method(endpoint, content)
        print str(response.code) + " - " + response.data

        content = HttpContent(HttpContentType.FORM, {"foo": "bar"})
        response = method(endpoint, content)
        print str(response.code) + " - " + response.data
