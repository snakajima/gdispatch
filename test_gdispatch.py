#!/usr/bin/env python
""" This test uses Werkzeug (http://werkzeug.pocoo.org/).
    For some reason, just importing werkzeug does not work,
    that's why I added this site.addsitedir hack
"""
import site
site.addsitedir("/Library/Python/2.5/site-packages")
import werkzeug
from google.appengine.ext import webapp
import gdispatch
from werkzeug import EnvironBuilder


gdispatch.route(lambda: ('/', MainHandler))
class MainHandler(webapp.RequestHandler):
    def get(self):
        output = 'root'
        self.response.out.write(output)

gdispatch.route(lambda: ('/sub', SubHandler))
class SubHandler(webapp.RequestHandler):
    def get(self):
        output = 'get sub(%s)' % self.request.query_string
        self.response.out.write(output)
    def post(self):
        output = 'post sub'
        self.response.out.write(output)

gdispatch.route(lambda: ('/api/.*', APIHandler))
class APIHandler(webapp.RequestHandler):
    def get(self):
        output = 'api(%s)' % self.request.path
        self.response.out.write(output)
        
def main(verbose=False):
    if (verbose): print "%s: start testing" % __name__
    
    builder = EnvironBuilder(path='/', method='GET', query_string=None)
    (iter, status, headers) = werkzeug.run_wsgi_app(gdispatch.get_application(), builder.get_environ())
    assert status == '200 OK', status
    assert ('Content-Length', '4') in headers
    assert "".join(iter) == "root"
    builder = EnvironBuilder(path='/sub', method='GET', query_string="foo=bar")
    (iter, status, headers) = werkzeug.run_wsgi_app(gdispatch.get_application(), builder.get_environ())
    assert status == '200 OK', status
    assert "".join(iter) == "get sub(foo=bar)"
    builder = EnvironBuilder(path='/sub', method='POST', query_string=None)
    (iter, status, headers) = werkzeug.run_wsgi_app(gdispatch.get_application(), builder.get_environ())
    assert status == '200 OK', status
    assert "".join(iter) == "post sub"
    builder = EnvironBuilder(path='/api/f1', method='GET', query_string=None)
    (iter, status, headers) = werkzeug.run_wsgi_app(gdispatch.get_application(), builder.get_environ())
    assert status == '200 OK', status
    assert "".join(iter) == "api(/api/f1)"
    builder = EnvironBuilder(path='/error', method='GET', query_string=None)
    (iter, status, headers) = werkzeug.run_wsgi_app(gdispatch.get_application(), builder.get_environ())
    assert status == '404 Not Found', status

    if (verbose): print "%s: testing complete" % __name__

if __name__ == "__main__":
    verbose = len([arg for arg in sys.argv if arg=='-v']) > 0
    main(verbose)
