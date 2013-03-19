# -*- coding: utf-8 -*-

from socialoauth.sites.base import OAuth2


class NetEase(OAuth2):
    AUTHORIZE_URL = 'https://api.t.163.com/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://api.t.163.com/oauth2/access_token'
    
    NETEASE_API_URL_PREFIX = 'https://api.t.163.com/'
    
    def build_api_url(self, url):
        return '%s%s' % (self.NETEASE_API_URL_PREFIX, url)
    
    def build_api_data(self, **kwargs):
        data = {
            'access_token': self.access_token
        }
        data.update(kwargs)
        return data
    
    def parse_token_response(self, res):
        self.uid = res['uid']
        self.access_token = res['access_token']
        self.expires_in = res['expires_in']
        self.refresh_token = res['refresh_token']
        
        res = self.api_call_get('users/show.json')
        
        self.name = res['name']
        self.avatar = res['profile_image_url']
        self.avatar_large = ""
        
        
        
