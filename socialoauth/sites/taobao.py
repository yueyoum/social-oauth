# -*- coding: utf-8 -*-

from socialoauth.sites.base import OAuth2


class TaoBao(OAuth2):
    AUTHORIZE_URL = 'https://oauth.taobao.com/authorize'
    ACCESS_TOKEN_URL = 'https://oauth.taobao.com/token'
    TAOBAO_API_URL = 'https://eco.taobao.com/router/rest'

    
    def build_api_url(self, url):
        return self.TAOBAO_API_URL

    def build_api_data(self, **kwargs):
        data = {
            'access_token': self.access_token,
            'v': 2.0,
            'format':'json'
        }
        data.update(kwargs)
        return data

    def parse_token_response(self, res):
        self.uid = res['taobao_user_id']
        self.access_token = res['access_token']
        self.expires_in = res['expires_in']
        self.refresh_token = res['refresh_token']
        
        res = self.api_call_get(method='taobao.user.buyer.get', 
                                fields='nick,avatar')

        user = res['user_buyer_get_response']['user']
        self.name = user['nick']
        self.avatar = user['avatar']
        self.avatar_large = ""