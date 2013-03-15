# -*- coding: utf-8 -*-

from socialoauth.sites.base import OAuth


class DouBan(OAuth):
    AUTHORIZE_URL = 'https://www.douban.com/service/auth2/auth'
    ACCESS_TOKEN_URL = 'https://www.douban.com/service/auth2/token'
    
    DOUBAN_API_URL = 'https://api.douban.com'
    
    
    def build_api_url(self, url):
        return '%s%s' % (self.DOUBAN_API_URL, url)
    
    def build_api_data(self, **kwargs):
        return kwargs
    
    def http_add_header(self, req):
        if getattr(self, 'access_token', None) is None:
            return
        req.add_header('Authorization',  'Bearer %s' % self.access_token)
        
    
    def parse_token_response(self, res):
        print res
        
        self.uid = int(res['douban_user_id'])
        self.access_token = res['access_token']
        self.expires_in = res['expires_in']
        self.refresh_token = res['refresh_token']
        
        res = self.api_call_get('/v2/user/~me')
        
        print res
        
        self.name = res['name'].encode('utf-8')
        self.avatar = res['avatar']
        self.avatar_large = ""
        
        
        
    #def post_status(self, text):
    #    if isinstance(text, unicode):
    #        text = text.encode('utf-8')
    #        
    #    url = 'https://api.weibo.com/2/statuses/update.json'
    #    res = self.api_call_post(url, status=text)
    #    print res
        
