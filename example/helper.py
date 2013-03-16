# -*- coding: utf-8 -*-

import json
import random
import hashlib




class SingletonGuard(type):
    def __init__(self, name, parent, class_dict):
        super(SingletonGuard, self).__init__(name, parent, class_dict)
        self.instance = None
        
        
    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = super(SingletonGuard, self).__call__(*args, **kwargs)
        return self.instance
        
        

class UserStorage(object):
    __metaclass__ = SingletonGuard
    
    def __init__(self):
        # 这是自身系统的用户ID，模拟数据库的自增长主键
        self.ID = 0
        # 存储社交网站uid于自身ID的对应关系
        self.table = {}
        # 用户信息
        self.user = {}
        
    def get_uid(self, site_name, site_uid):
        # site_name 是社交网站的 名字
        # site_uid 是此授权用户在此网站的uid
        # 查询此授权用户是否在自身数据库中的UID
        
        return self.table.get(site_name, {}).get(site_uid, None)
        
    
    
    def bind_new_user(self, site_name, site_uid):
        self.ID += 1
        if site_name in self.table:
            self.table[site_name][site_uid] = self.ID
        else:
            self.table[site_name] = {site_uid: self.ID}
            
        return self.ID
    
    
    def get_user(self, uid):
        return self.user[uid]
    
    def set_user(self, uid, **kwargs):
        self.user[uid] = kwargs





def gen_session_id():
    key = '%0.10f' % random.random()
    return hashlib.sha1(key).hexdigest()



class Session(object):
    __metaclass__ = SingletonGuard
    
    uid_session_keys = {}
    
    def __init__(self):
        self._sessions = {}
        
        
    @classmethod
    def make_session_id(cls, uid):
        if uid not in cls.uid_session_keys:
            cls.uid_session_keys[uid] = gen_session_id()
        return cls.uid_session_keys[uid]
    
    
    @classmethod
    def refresh_session_id(cls, uid):
        cls.uid_session_keys[uid] = gen_session_id()
        return cls.uid_session_keys[uid]
        
    
    def get(self, key):
        if key not in self._sessions:
            return {}
        return json.loads(self._sessions[key])
    
    def set(self, key, **kwargs):
        self._sessions[key] = json.dumps(kwargs)
        
        
    def update(self, key, **kwargs):
        s = self.get(key)
        if not s:
            self.set(key, **kwargs)
        else:
            s.update(kwargs)
            self.set(key, **s)
            
            
    def rem(self, key):
        if key in self._sessions:
            del self._sessions[key]
