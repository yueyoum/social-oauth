# -*- coding: utf-8 -*-

class SocialOAuthException(Exception):
    pass


class SocialConfigError(SocialOAuthException):
    pass


class SocialGetTokenError(SocialOAuthException):
    """Occurred when get Access Token"""
    pass

class SocialAPIError(SocialOAuthException):
    """Occurred when doing API call"""
    pass