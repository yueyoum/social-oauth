# -*- coding: utf-8 -*-
import os
import sys


from _bottle import Bottle, run, request, response, redirect, static_file


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.normpath(os.path.join(CURRENT_PATH, '..')))

IMAGE_PATH = os.path.join(CURRENT_PATH, 'images')

from settings import SOCIALOAUTH_SITES
from socialoauth import socialsites
from socialoauth.utils import import_oauth_class
from socialoauth.exception import SocialAPIError

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
        _s = import_oauth_class(s)()
        if os.path.exists(os.path.join(IMAGE_PATH, _s.site_name + '.png')):
            a_content = '<img src="/static/images/%s.png" />' % _s.site_name
        else:
            a_content = '使用 %s 登录' % _s.site_name
        
        return """<div style="margin: 20px;">
        <a href="%s">%s</a>
        </div>""" % (_s.authorize_url, a_content)
    
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
    try:
        s.get_access_token(code)
    except SocialAPIError as e:
        # 这里可能会发生错误
        print e.site_name      # 哪个站点的OAuth2发生错误？
        print e.url            # 请求的url
        print e.error_msg      # 由站点返回的错误信息 / urllib2 的错误信息
        raise
    
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
    