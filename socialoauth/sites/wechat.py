# -*- coding: utf-8 -*-

import json
from urllib import quote_plus

from socialoauth.sites.base import OAuth2
from socialoauth.exception import SocialAPIError, SocialSitesConfigError


class Wechat(OAuth2):
    AUTHORIZE_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    OPENID_URL = 'https://api.weixin.qq.com/sns/userinfo'

    SUPPORTED_SCOPES = ('snsapi_base', 'snsapi_userinfo')

    @property
    def authorize_url(self):
        url = "%s?appid=%s&redirect_uri=%s&response_type=code" % (
                self.AUTHORIZE_URL, self.CLIENT_ID, quote_plus(self.REDIRECT_URI)
            )
        
        if getattr(self, 'SCOPE', None) is not None:
            if (self.SCOPE in self.SUPPORTED_SCOPES):
                url = '%s&scope=%s' % (url, self.SCOPE)
            else:
                raise SocialSitesConfigError("SCOPE must be one of (%s)." %(','.join(self.SUPPORTED_SCOPES)), None)
        else:
            raise SocialSitesConfigError("SCOPE is required!", None)

        url = url + '&state=socialoauth#wechat_redirect'
        return url

    def get_access_token(self, code):
        data = {
                'appid': self.CLIENT_ID,
                'secret': self.CLIENT_SECRET,
                'redirect_uri': self.REDIRECT_URI,
                'code': code,
                'grant_type': 'authorization_code'
            }

        res = self.http_get(self.ACCESS_TOKEN_URL, data, parse=False)
        self.parse_token_response(res)

    def build_api_url(self, url):
        return url

    def build_api_data(self, **kwargs):
        data = {
            'access_token': self.access_token,
            'openid': self.uid
        }
        data.update(kwargs)
        return data

    def parse_token_response(self, res):
        res = json.loads(res)

        self.access_token = res['access_token']
        self.expires_in = int(res['expires_in'])
        self.refresh_token = res['refresh_token']

        self.uid = res['openid']

        if self.SCOPE == 'snsapi_userinfo':
            res = self.api_call_get(self.OPENID_URL, lang='zh_CN')
    
            if 'errcode' in res:
                raise SocialAPIError(self.site_name, self.OPENID_URL, res)
    
            self.name = res['nickname']
            self.avatar = res['headimgurl']
            self.avatar_large = res['headimgurl']
        else:
            self.name = ''
            self.avatar = ''
            self.avatar_large = ''
