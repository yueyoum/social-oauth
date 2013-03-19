# -*- coding: utf-8 -*-

from socialoauth.sites.base import OAuth2


class Baidu(OAuth2):
    AUTHORIZE_URL = 'https://openapi.baidu.com/oauth/2.0/authorize'
    ACCESS_TOKEN_URL = 'https://openapi.baidu.com/oauth/2.0/token'
    
    BAIDU_API_URL_PREFIX = 'https://openapi.baidu.com/rest/2.0/'
    SMALL_IMAGE = 'http://tb.himg.baidu.com/sys/portraitn/item/'
    LARGE_IMAGE = 'http://tb.himg.baidu.com/sys/portrait/item/'
    
    RESPONSE_ERROR_KEY = 'error_code'
    
    def build_api_url(self, url):
        return '%s%s' % (self.BAIDU_API_URL_PREFIX, url)
    
    def build_api_data(self, **kwargs):
        data = {
            'access_token': self.access_token,
        }
        data.update(kwargs)
        return data
    
    def parse_token_response(self, res):
        self.access_token = res['access_token']
        self.expires_in = res['expires_in']
        self.refresh_token = res['refresh_token']
        
        res = self.api_call_get('passport/users/getLoggedInUser')
        
        self.uid = int(res['uid'])
        self.name = res['uname']
        self.avatar = '%s%s' % (self.SMALL_IMAGE, res['portrait'])
        self.avatar_large = '%s%s' % (self.LARGE_IMAGE, res['portrait'])
