# -*- coding: utf-8 -*-

import base64

from socialoauth.sites.base import OAuth2


class Sohu(OAuth2):
    AUTHORIZE_URL = 'https://api.t.sohu.com/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://api.t.sohu.com/oauth2/access_token'
    
    SOHU_API_URL_PREFIX = 'https://api.t.sohu.com/'
    
    def __init__(self):
        super(Sohu, self).__init__()
        self.CLIENT_SECRET = base64.b64encode(self.CLIENT_SECRET)
    
    
    @property
    def authorize_url(self):
        url = super(Sohu, self).authorize_url
        return '%s&scope=basic&wrap_client_state=socialoauth' % url
        
    
    
    def build_api_url(self, url):
        return '%s%s' % (self.SOHU_API_URL_PREFIX, url)
    
    def build_api_data(self, **kwargs):
        data = {
            'access_token': self.access_token
        }
        data.update(kwargs)
        return data
    
    def parse_token_response(self, res):
        self.access_token = res['access_token']
        self.expires_in = res['expires_in']
        self.refresh_token = res['refresh_token']
        
        res = self.api_call_get('users/show.json')
        
        self.uid = res['id']
        self.name = res['screen_name']
        self.avatar = res['profile_image_url']
        self.avatar_large = ""
        
        
        
