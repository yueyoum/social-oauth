# -*- coding: utf-8 -*-

from socialoauth.sites.base import OAuth


class RenRen(OAuth):
    AUTHORIZE_URL = 'https://graph.renren.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'http://graph.renren.com/oauth/token'
    
    RENREN_API_URL = 'https://api.renren.com/restserver.do'
    
    
    def build_api_url(self, *args):
        return self.RENREN_API_URL
    
    
    def build_api_data(self, **kwargs):
        data = {
            'v': 1.0,
            'access_token': self.access_token,
            'format': 'json',
        }
        data.update(kwargs)
        return data
    
    
    
    def parse_token_response(self, res):
        print res
        
        self.uid = int(res['user']['id'])
        self.access_token = res['access_token']
        
        res = self.api_call_post(method='users.getInfo')
        
        
        self.name = res[0]['name'].encode('utf-8')
        self.avatar = res[0]['tinyurl']
        self.avatar_large = res[0]['headurl']
        
        #self.post_status(u'啊啊啊')
        
        
        
    def post_status(self, text):
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        
        res = self.api_call_post(method='status.set', status=text)
        print res

