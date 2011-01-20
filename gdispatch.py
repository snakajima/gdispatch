# -*- coding: utf-8 -*-
#
# Hosted at: http://github.com/snakajima/gdispatch
#
# Copyright (c) 2009, 2010, 2011 Satoshi Nakajima
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

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
def is_development():
    return os.environ['SERVER_SOFTWARE'].startswith('Development/')

def transactional(original_func):
    def decorated_func(*args, **kwargs):
        return db.run_in_transaction(original_func, *args, **kwargs)
    return decorated_func

def kwargs(original_func):
    """ This decorator allows RequestHandlers to receive get/post parameters as named arguments """
    import inspect
    argspec = inspect.getargspec(original_func) 
    args = tuple(argspec[0][1:])
    def decorated_func(rh):
        kwargs = dict([(arg, rh.request.get(arg)) for arg in args])
        return original_func(rh, **kwargs)
    return decorated_func

@memoize
def _routing_functions(namespace):
    """ List of routing functions. Singleton. """
    return []
    
def route(callback_func, namespace=None):
    """ This simply registers a routing function, which returns a 
        (url, request_handler_class) tuple.
        Later, we call each function to generate the URL mapping.
        This defered registration mechanism allows developers to put
        dispatch.route() BEFORE the definition of the RequestHandler
        class.
    """
    _routing_functions(namespace).append(callback_func)

@memoize
def _url_mapping(namespace):
    """ The list of (url, request_handler_class) tuples. Singleton. """
    return [f() for f in _routing_functions(namespace)]
    
def run(namespace=None):
    application = webapp.WSGIApplication(_url_mapping(namespace), debug=True)
    run_wsgi_app(application)

