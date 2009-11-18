#!/usr/bin/env python
import sys
import os

SDK_PATH = '/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine'
EXTRA_PATHS = [
    '..',
    SDK_PATH,
    os.path.join(SDK_PATH, 'lib', 'antlr3'),
    os.path.join(SDK_PATH, 'lib', 'django'),
    os.path.join(SDK_PATH, 'lib', 'webob'),
    os.path.join(SDK_PATH, 'lib', 'yaml', 'lib'),
]
sys.path = sys.path[:1] + EXTRA_PATHS + sys.path[1:]

if __name__ == "__main__":
    verbose = len([arg for arg in sys.argv if arg=='-v']) > 0
    units = ['gdispatch']
    for unit in units:
        module = __import__('test_%s' % unit)
        module.main(verbose)
