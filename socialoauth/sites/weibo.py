# -*- coding: utf-8 -*-

from socialoauth.sites.base import OAuth


class Weibo(OAuth):
    AUTHORIZE_URL = 'https://api.weibo.com/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'
    
    def parse_ret(self, res):
        self.uid = int(res['uid'])
        
        url = 'https://api.weibo.com/2/users/show.json'
        data = {
            'access_token': self.access_token,
            'uid': self.uid
        }
        res = self.api_call_get(url, data)
        
        self.name = res['name']
        self.avatar = res['profile_image_url']
        self.avatar_large = res['avatar_large']
        
        print res
        
