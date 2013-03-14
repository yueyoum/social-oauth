# -*- coding: utf-8 -*-

from urllib import urlencode
import urllib2
import json
import functools


from socialoauth.exception import SocialGetTokenError, SocialAPIError
from socialoauth import settings


class OAuth(object):
    """
    Base OAuth class, Sub class must define the following settings:
    
    AUTHORIZE_URL    - Asking user to authorize and get token
    ACCESS_TOKEN_URL - Get authorized access token
    REDIRECT_URI     - The url after user authorized and redirect to
    
    CLIENT_ID        - Your client id for the social site
    CLIENT_SECRET    - Your client secret for the social site
    """
    
    def __init__(self):
        self.api_call_get = functools.partial(self._api_call, method='GET')
        self.api_call_post = functools.partial(self._api_call, method='POST')
        
        key = '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        configs = settings.load_config(key)
        for k, v in configs.iteritems():
            setattr(self, k, v)
            
    
    
    def http_get(self, url, data):
        res = urllib2.urlopen('%s?%s' % (url, urlencode(data))).read()
        return json.loads(res)
    
    
    def http_post(self, url, data):
        req = urllib2.Request(url, data=urlencode(data))
        res = urllib2.urlopen(req).read()
        return json.loads(res)
    
    @property
    def authorize_url(self):
        url = "%s?client_id=%s&response_type=code&redirect_uri=%s" % (
            self.AUTHORIZE_URL, self.CLIENT_ID, self.REDIRECT_URI
        )
        
        if getattr(self, 'SCOPE', None) is not None:
            url = '%s&scope=%s' % (url, '+'.join(self.SCOPE))
        
        return url
    
    
    
    def get_access_token(self, code):
        data = {
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'redirect_uri': self.REDIRECT_URI,
            'code': code,
            'grant_type': 'authorization_code'
        }
        
        
        try:
            res = self.http_post(self.ACCESS_TOKEN_URL, data)
        except urllib2.HTTPError:
            raise SocialGetTokenError
        
        
        print 'res = ', res
        
        self.access_token = res['access_token']
        self.parse_ret(res)
        
        
    def _api_call(self, url, data, method):
        try:
            if method == 'GET':
                return self.http_get(url, data)
            return self.http_post(url, data)
        except urllib2.HTTPError:
            raise SocialAPIError(url)
        
    
    
    def parse_ret(self, res):
        raise NotImplementedError
    