# -*- coding: utf-8 -*-
import os
import sys


from bottle import Bottle, run, request, redirect

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.normpath(os.path.join(CURRENT_PATH, '..')))

app = Bottle()

from settings import SOCIALOAUTH_SITES
from socialoauth import settings
from socialoauth.utils import import_module

settings.config(SOCIALOAUTH_SITES)





@app.get('/login')
def login():
    def _link(s):
        m = import_module(s)
        _s = m()
        return '<p><a href="%s">%s</a></p>' % (_s.authorize_url, _s.name)
    
    links = map(_link, settings.list_sites())
    links = '\n'.join(links)
    
    
    html = """<!DOCTYPE html>
    <html>
    <body>
        %s
    </body>
    </html>
    """ % links
    
    return html
    
    
@app.get('/account/oauth/<sitename>')
def callback(sitename):
    code = request.GET.get('code')
    s = import_module(settings[sitename])()
    
    try:
        s.get_access_token(code)
    except Exception, e:
        print 'error', e
        
        redirect('/login')
    
    html = """<html>
    <body>
        <h2>%d</h2>
        <h2>%s</h2>
        <p>Large avatar</p>
        <img src="%s" />
        <p>Small avatar</p>
        <img src="%s" />
    </body>
    </html>
    """ % (s.uid, s.name, s.avatar_large, s.avatar)
    
    return html
    
    
    
    
    
    
    
    
run(app)