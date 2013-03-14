# -*- coding: utf-8 -*-

from socialoauth.sites.base import OAuth


class RenRen(OAuth):
    AUTHORIZE_URL = 'https://graph.renren.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'http://graph.renren.com/oauth/token'
    
    def parse_ret(self, res):
        self.uid = int(res['user']['id'])
        
        
        url = 'https://api.renren.com/restserver.do'
        data = {
            'v': 1.0,
            'access_token': self.access_token,
            'format': 'json',
            'method': 'users.getInfo',
        }
        
        res = self.api_call_post(url, data)
        
        print res
        
        self.name = res[0]['name']
        self.avatar = res[0]['tinyurl']
        self.avatar_large = res[0]['headurl']
        
        
        
    def post_status(self, text=None):
        text = text or u"测试OAuth".encode('utf-8')
        
        url = 'https://api.renren.com/restserver.do'
        data = {
            'v': 1.0,
            'access_token': self.access_token,
            'method': 'status.set',
            'status': text
        }
        
        res = self.api_call_post(url, data)
        print res

