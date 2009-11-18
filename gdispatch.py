# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

def memoize(original_func):
    """ This decorator memorize cached data in global memory """
    cache = {}
    def decorated_func(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = original_func(*args)
            return cache[args]
    return decorated_func

@memoize
def _routing_functions():
    """ List of routing functions. Singleton. """
    return []

def route(callback_func):
    """ This simply registers a routing function, which returns a 
        (url, request_handler_class) tuple.
        Later, we call each function to generate the URL mapping.
        This defered registration mechanism allows developers to put
        dispatch.route() BEFORE the definition of the RequestHandler
        class.
    """
    _routing_functions().append(callback_func)

@memoize
def _url_mapping():
    """ The list of (url, request_handler_class) tuples. Singleton. """
    return [f() for f in _routing_functions()]
    
def run(debug=True):
    application = webapp.WSGIApplication(_url_mapping(), debug=debug)
    run_wsgi_app(application)

def get_application(debug=True):
    """ For unit testing """
    return webapp.WSGIApplication(_url_mapping(), debug=debug)


