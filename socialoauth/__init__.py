# -*- coding: utf-8 -*-

from socialoauth.exception import SocialConfigError


version_info = (0, 2, 0)
VERSION = __version__ = '.'.join( map(str, version_info) )


class Settings(object):
    """
    This class hold the sites settings.
    User define OAuth2 configs, e.g. site name, oauth class, client_id, client_secret
    in settings file. This Class will parse and store it.
    
    When a site OAuth2 class instantiated, It will load settings from there
    """
    def __init__(self):
        self._configed = False
        self._sites_id_name_table = {}
        # {1: 'renren', 2: 'douban'...}
        self._sites_name_class_table = {}
        # {'renren': 'socialoauth.sites.renren.RenRen',...}
        self._sites_class_config_table = {}
        # {'socialoauth.sites.renren.RenRen': {...}, ...}
        
        
    def __getitem__(self, name):
        """Get OAuth2 Class by it's setting name"""
        if not self._configed:
            raise SocialConfigError("No configure")
        
        try:
            return self._sites_name_class_table[name]
        except KeyError:
            raise SocialConfigError("No settings for site: %s" % name)
        
        
        
    def config(self, settings):
        """Call This method when application start"""
        for k, v in settings.iteritems():
            _module_class, _site_id, _site_config = v
            if _site_id in self._sites_id_name_table:
                raise SocialConfigError(
                    "Duplicate site id %d with site name %s" % _site_id, k
                )
            self._sites_id_name_table[_site_id] = k
            
            self._sites_name_class_table[k] = _module_class
            self._sites_class_config_table[_module_class] = {
                'site_name': k, 'site_id': _site_id
            }
            
            for _k, _v in _site_config.iteritems():
                self._sites_class_config_table[_module_class][_k.upper()] = _v
                
        self._configed = True
        
    
    def load_config(self, module_class_name):
        """
        OAuth2 Class get it's settings at here.
        Example:
            from socialoauth import socialsites
            class_key_name = Class.__module__ + Class.__name__
            settings = socialsites.load_config(class_key_name)
        """
        return self._sites_class_config_table[module_class_name]
        
        
    def list_sites(self):
        return self._sites_class_config_table.keys()
    
    
    def get_site_name_by_id(self, site_id):
        try:
            return self._sites_id_name_table[site_id]
        except KeyError:
            raise SocialConfigError("No settings for site id : %d" % site_id)
        
    def get_site_class_by_id(self, site_id):
        site_name = self.get_site_class_by_id(site_id)
        return self.__getitem__(site_name)
        
        
        
socialsites = Settings()

