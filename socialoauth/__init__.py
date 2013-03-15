# -*- coding: utf-8 -*-

from socialoauth.exception import SocialConfigError


class Settings(object):
    """
    This class hold the sites settings.
    User define OAuth2 configs, e.g. site name, oauth class, client_id, client_secret
    in settings file. This Class will parse and store it.
    
    When a site OAuth2 class instantiated, It will load settings from there
    """
    def __init__(self):
        self._configed = False
        self.sites = {}
        self.sites_config = {}
        
        
    def __getitem__(self, name):
        """Get OAuth2 Class by it's setting name"""
        if not self._configed:
            raise SocialConfigError("No configure")
        
        if name not in self.sites:
            raise SocialConfigError("No settings for site: %s" % name)
        
        return self.sites[name]
        
        
        
    def config(self, settings):
        """Call This method when application start"""
        for k, v in settings.iteritems():
            self.sites[k] = v[0]
            self.sites_config[v[0]] = {'name': k}
            for _k, _v in v[1].iteritems():
                self.sites_config[v[0]][_k.upper()] = _v
                
        self._configed = True
        
    
    def load_config(self, module_name):
        """
        OAuth2 Class get it's settings at here.
        Example:
            from socialoauth import socialsites
            class_key_name = Class.__module__ + Class.__name__
            settings = socialsites.load_config(class_key_name)
        """
        return self.sites_config[module_name]
        
        
    def list_sites(self):
        return self.sites_config.keys()
        
        
        
socialsites = Settings()

