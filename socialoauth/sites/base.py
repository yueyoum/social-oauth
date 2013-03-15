# -*- coding: utf-8 -*-

from urllib import urlencode
import urllib2
import json


from socialoauth.exception import SocialGetTokenError, SocialAPIError
from socialoauth import settings


class OAuth(object):
    """
    Base OAuth class, Sub class must define the following settings:
    
    AUTHORIZE_URL    - Asking user to authorize and get token
    ACCESS_TOKEN_URL - Get authorized access token
    
    
    And the bellowing should define in settings file
    
    REDIRECT_URI     - The url after user authorized and redirect to
    CLIENT_ID        - Your client id for the social site
    CLIENT_SECRET    - Your client secret for the social site
    """
    
    def __init__(self):
        key = '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        configs = settings.load_config(key)
        for k, v in configs.iteritems():
            setattr(self, k, v)
            
    
    
    def http_get(self, url, data, parse=True):
        req = urllib2.Request('%s?%s' % (url, urlencode(data)))
        self.http_add_header(req)
        res = urllib2.urlopen(req).read()
        if parse:
            return json.loads(res)
        return res
    
    
    def http_post(self, url, data, parse=True):
        req = urllib2.Request(url, data=urlencode(data))
        self.http_add_header(req)
        res = urllib2.urlopen(req).read()
        if parse:
            return json.loads(res)
        return res
    
    
    def http_add_header(self, req):
        """Sub class rewiter this function If it's necessary to add headers"""
        pass
    
    
    
    @property
    def authorize_url(self):
        url = "%s?client_id=%s&response_type=code&redirect_uri=%s" % (
            self.AUTHORIZE_URL, self.CLIENT_ID, self.REDIRECT_URI
        )
        
        if getattr(self, 'SCOPE', None) is not None:
            url = '%s&scope=%s' % (url, '+'.join(self.SCOPE))
            
        # for qq
        if getattr(self, 'STATE', None) is not None:
            url = '%s&state=%s' % (url, self.STATE)
         
        return url
    
    
    
    def get_access_token(self, code, method='POST', parse=True):
        data = {
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'redirect_uri': self.REDIRECT_URI,
            'code': code,
            'grant_type': 'authorization_code'
        }
        
        
        try:
            if method == 'POST':
                res = self.http_post(self.ACCESS_TOKEN_URL, data, parse=parse)
            else:
                res = self.http_get(self.ACCESS_TOKEN_URL, data, parse=parse)
        except urllib2.HTTPError:
            raise SocialGetTokenError
        
        self.parse_token_response(res)
        
        
        
    def api_call_get(self, url=None, **kwargs):
        url = self.build_api_url(url)
        data = self.build_api_data(**kwargs)
        #return self._api_call(url, data, 'GET')
        return self.http_get(url, data)
    
    def api_call_post(self, url=None, **kwargs):
        url = self.build_api_url(url)
        data = self.build_api_data(**kwargs)
        #return self._api_call(url, data, 'POST')
        return self.http_post(url, data)
        
        
        
    #def _api_call(self, url, data, method):
    #    #try:
    #    if method == 'GET':
    #        return self.http_get(url, data)
    #    return self.http_post(url, data)
    #    #except urllib2.HTTPError:
    #    #    raise SocialAPIError(url)
        
    
    
    def parse_token_response(self, res):
        """
        Subclass MUST implement this function
        And set the following attributes:
        
        access_token, uid, name, avatar, avatar_large
        """
        raise NotImplementedError
    
    
    def build_api_url(self, url):
        raise NotImplementedError
    
    
    def build_api_data(self, **kwargs):
        raise NotImplementedError
        
    