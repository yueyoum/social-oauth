# -*- coding: utf-8 -*-
import os
import sys


from bottle import Bottle, run, request, redirect

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.normpath(os.path.join(CURRENT_PATH, '..')))

app = Bottle()

from settings import SOCIALOAUTH_SITES
from socialoauth import socialsites
from socialoauth.utils import import_module

socialsites.config(SOCIALOAUTH_SITES)




@app.get('/login')
def login():
    def _link(s):
        m = import_module(s)
        _s = m()
        return '<p><a href="%s">%s</a></p>' % (_s.authorize_url, _s.name)
    
    links = map(_link, socialsites.list_sites())
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
    s = import_module(socialsites[sitename])()
    
    s.get_access_token(code)
    
    
    html = """<html>
    <body>
        <h2>{0}</h2>
        <h2>{1}</h2>
        <p>Large avatar</p>
        <img src="{2}" />
        <p>Small avatar</p>
        <img src="{3}" />
    </body>
    </html>
    """ .format(s.uid, s.name, s.avatar_large, s.avatar)
    
    # qq 返回是是 openid， 是string
    
    return html
    
    
    
    
    
    
    
    
run(app)