# -*- coding: utf-8 -*-

class SocialOAuthException(Exception):
    pass


class SocialConfigError(Exception):
    pass



class SocialAPIError(SocialOAuthException):
    """Occurred when doing API call"""
    def __init__(self, site_name, url, code, reason, api_error_msg, *args):
        self.site_name = site_name
        self.url = url
        self.code = code
        self.reason = reason
        self.api_error_msg = api_error_msg
        SocialOAuthException.__init__(self, reason, api_error_msg, *args)
