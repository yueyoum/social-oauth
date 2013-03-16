# -*- coding: utf-8 -*-
import os
import sys


from bottle import Bottle, run, request, response, redirect, static_file

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.normpath(os.path.join(CURRENT_PATH, '..')))

IMAGE_PATH = os.path.join(CURRENT_PATH, 'images')

from settings import SOCIALOAUTH_SITES
from socialoauth import socialsites
from socialoauth.utils import import_oauth_class

from helper import Session, UserStorage, gen_session_id

socialsites.config(SOCIALOAUTH_SITES)



app = Bottle()


@app.get('/static/images/<filepath:path>')
def static_files(filepath):
    return static_file(filepath, IMAGE_PATH, mimetype='image/png')


@app.get('/')
def index():
    session_id = request.get_cookie('session_id')
    if session_id:
        session = Session()
        data = session.get(session_id)
        uid = data.get('uid', None)
        if uid:
            storage = UserStorage()
            user = storage.get_user(uid)
            
            
            html = """<!DOCTYPE html>
            <html>
                <body>
                <h2>Welcome. %s</h2>
                <img src="%s" />
                <p><a href="/logout">Logout</a></p>
                </body>
            </html>""" % (user['name'], user['avatar'])
            
            return html
    
    if not session_id:
        response.set_cookie('session_id', gen_session_id())
    html = """<html>
    <body><a href="/login">Login</a></body>
    </html>"""
    
    return html




@app.get('/login')
def login():
    def _link(s):
        m = import_oauth_class(s)
        _s = m()
        return """<div style="margin: 20px;">
        <a href="%s"><img src="/static/images/%s.png" /></a>
        </div>""" % (_s.authorize_url, _s.site_name)
    
    links = map(_link, socialsites.list_sites())
    links = '\n'.join(links)
    
    
    html = """<!DOCTYPE html>
    <html>
        <body>%s</body>
    </html>
    """ % links
    
    return html
    
    
    
@app.get('/account/oauth/<sitename>')
def callback(sitename):
    code = request.GET.get('code')
    if not code:
        # error occurred
        redirect('/oautherror')
    
    s = import_oauth_class(socialsites[sitename])()
    s.get_access_token(code)
    
    # 到这里授权完毕，并且取到了用户信息，uid, name, avatar...
    storage = UserStorage()
    UID = storage.get_uid(s.site_name, s.uid)
    if not UID:
        # 此用户第一次登录，为其绑定一个自身网站的UID
        UID = storage.bind_new_user(s.site_name, s.uid)
        
    
    storage.set_user(UID, name=s.name, avatar=s.avatar)
    session_id = request.get_cookie('session_id')
    if not session_id:
        session_id = Session.make_session_id(UID)
    session = Session()
    session.set(session_id, uid=UID)
    response.set_cookie('session_id', session_id)
    
    #print storage.user
    #print storage.table
    #
    #print session._sessions
    
    
    redirect('/')
    
    
    
    
@app.get('/logout')
def logout():
    session_id = request.get_cookie('session_id')
    if not session_id:
        redirect('/')
    
    session = Session()
    data = session.get(session_id)
    session.rem(session_id)
    uid = data.get('uid', None)
    if uid:
        # 重置其session_id
        Session.refresh_session_id(uid)
        
    response.set_cookie('session_id', '')
    redirect('/')
    
    
    
@app.get('/oautherror')
def oautherror():
    print 'OAuth Error!'
    redirect('/')
    
    
if __name__ == '__main__':    
    run(app)
    