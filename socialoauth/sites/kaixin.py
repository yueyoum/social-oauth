# -*- coding: utf-8 -*-

from socialoauth.sites.base import OAuth2


class KaiXin(OAuth2):
    AUTHORIZE_URL = 'http://api.kaixin001.com/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://api.kaixin001.com/oauth2/access_token'
    
    API_URL_PREFIX = 'https://api.kaixin001.com'
    
    
    def build_api_url(self, url):
        return '%s%s' % (self.API_URL_PREFIX, url)
    
    def build_api_data(self, **kwargs):
        data = {
            'access_token': self.access_token
        }
        data.update(kwargs)
        return data
    
    def parse_token_response(self, res):
        self.access_token = res['access_token']
        self.expires_in = res['expires_in']
        
        res = self.api_call_get('/users/me.json')
        
        self.uid = int(res['uid'])
        self.name = res['name']
        self.avatar = res['logo50']
        self.avatar_large = ""

