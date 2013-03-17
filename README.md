# socialoauth

Python Package Of A Sets Of Social Websits OAuth2 Clients

## 简介

socialoauth 专注于中国大陆开放了OAuth2认证的网站，并且着重使用了 **用第三方帐号登录** 的功能。
为了将大量用户方便的导入到自己的网站，免去再次注册的麻烦。

但socialoauth也是很容易扩展的：
**对于支持OAuth2的网站，只需要一个子类重写3个（或更多）方法即可**


## Supported sites

*   人人
*   腾讯
*   新浪微博
*   豆瓣

#### 下面是TODO 中的站点

*   网易
*   搜狐




## Example

快速体验 socialoauth

    git clone https://github.com/yueyoum/social-oauth.git
    cd social-oauth/example
    cp settings.py.example settings.py
    
    # 在这里按照你的情况修改settings.py。详细情况见下面
    
    python index.py
    
    
现在用浏览器打开对应的地址，就能体验相应的功能。

下面是我用 人人网 帐号登录的过程：


#### 初始情况，首页只有一个 login 链接

![step1](http://i1297.photobucket.com/albums/ag23/yueyoum/x1_shadowed_zpsac1e046a.png)


#### 点击后，根据settings.py中的设置，显示可用的认证网站

![step2](http://i1297.photobucket.com/albums/ag23/yueyoum/x2_shadowed_zps47bd6fd8.png)


#### 我用人人网帐号进行测试，点击后，转到人人登录认证的界面

![step3](http://i1297.photobucket.com/albums/ag23/yueyoum/x4_shadowed_zps6aed31ec.png)


#### 认证完毕后，就会显示用户的名字和小头像。
example中有个简单的session机制，
此时再打开首页（不关闭浏览器）就不用再登录，会直接显示名字和头像

![step4](http://i1297.photobucket.com/albums/ag23/yueyoum/x3_shadowed_zpse6a0f575.png)


## settings.py

这就是配置文件，其实在你的应用中你可以随意换其他名字。

配置示例:


    SOCIALOAUTH_SITES = {
        'renren': ('socialoauth.sites.renren.RenRen',
                   {
                    'redirect_uri': 'http://test.org/account/oauth/renren',
                    'client_id': 'YOUR ID',
                    'client_secret': 'YOUR SECRET',
                    'scope': ['publish_feed', 'status_update']
                   }
        ),
            
        'weibo': ('socialoauth.sites.weibo.Weibo',
                  {
                    'redirect_uri': 'http://test.org/account/oauth/weibo',
                    'client_id': 'YOUR ID',
                    'client_secret': 'YOUR SECRET',
                  }
        ),
        
        'qq': ('socialoauth.sites.qq.QQ',
                  {
                    'redirect_uri': 'http://test.org/account/oauth/qq',
                    'client_id': 'YOUR ID',
                    'client_secret': 'YOUR SECRET',
                  }
        ),
            
        'douban': ('socialoauth.sites.douban.DouBan',
                  {
                    'redirect_uri': 'http://test.org/account/oauth/douban',
                    'client_id': 'YOUR ID',
                    'client_secret': 'YOUR SECRET',
                    'scope': ['douban_basic_common']
                  }
        ),
        
    }
    
    
`SOCIALOAUTH_SITES` 是此配置的名字，同样，你也可以随意更改

*   `SOCIALOAUTH_SITES` 是一个字典

*   key 为站点的名字，你可以随意取名字，但必须和 回调地址 `redirect_uri` 中的 站点标识 一样

*   value 为tuple

    *   第一个元素指定此站点的 OAuth2 类的 包结构关系
    
    *   第二个元素为字典，里面设置了一个OAuth2应用必须的设置项。
    
        *   client_id, client_secret是申请开发者，创建好应用后的值
        
        *   redirect_uri 是在用户授权后的回调地址，domain也需要在开发者应用中设置
        
        *   scope是选填的一项，在于某些API需要scope权限申请。具体的参考各个站点自己的文档
        
        
        
        
## 如何扩展

要添加新的站点，正常网站只需要简单几步。（不正常网站比如腾讯，那就得多几步！）

1.  cd social-oauth/socialoauth/sites
2.  vim new_site.py

        #  this is new_site.py
        from socialoauth.sites.base import OAuth2
        
        class NewSite(OAuth2):
            AUTHORIZE_URL = 'https://xxx'
            ACCESS_TOKEN_URL = 'https://xxx'
            
            # 这两条url从站点文档中取到，
            # 第一个是请求用户认证的URL，
            # 第二个是根据第一步转到回调地址传会的code取得access_token的地址
            
            def build_api_url(self, *args):
                # 如果一个网站它的api url是固定的，比如人人，
                # 那么这里每次返回固定的url即可。
                # 然后在调用 api_call_get/get_call_post时，只需要传递关键字参数即可
                # 例如 res = self.api_call_get(param=1)
                #
                # return SOME_URL
                
                # 但大多数站点每个API都有不同的url，
                # 这里有两种处理方式
                # 第一个中是把公共的地方提取出来，
                # 在api_call_get/api_call_post的时候值传递部分url。
                # 第二个就是在 api_call 时传递完整的url
                # 例如 res = self.api_call_get('https://xxx', param=1)
                
                # return args[0]
                
                pass
                
                
            def build_api_data(self, **kwargs):
                # api 调用的时候需要传递参数，对于固定参数比如 access_token 等，
                # 可以写在这里，在调用api_call只需要以关键字的方式传入所需参数即可
                
                data = {
                    'access_token': self.access_token
                }
                data.update(kwargs)
                return data
                
                
            def http_add_header(self, req):
                # 一般都不用理会此函数。
                # 只是一些特殊站点，比如豆瓣他的认证需要你设置header
                # 就重写此方法，req 是 urllib2.Reqeust 实例
                # req.add_header(name, value)
                
                
                
            def parse_token_response(self, res):
                # res 是请求access_token后的返回。
                # 在这里要取到此授权用户的基本信息，uid, name, avatar等
                # 各个站点在这里的差异较大




这样一个OAuth2的client就写完了， 然后你还需要把于此站点有关的设置添加到 settings.py中



## 注意

socialoauth 得知道有哪些站点，以及这些站点各自的设置。所以 以下代码 **必须** 在项目启动
的时候就要运行

    from settings import SOCIALOAUTH_SITES
    from socialoauth import socialsites
    
    socialsites.config(SOCIALOAUTH_SITES)


然后在后续的代码中 只要同样 `from socialoauth import socialsites` 就可以得到配置的站点信息

    # 取某一站点的设置
    config = socialsites.load_config('socialoauth.sites.renren.RenRen')
    
    # 列出全部配置的站点模块
    socialsites.list_sites()
    # ['socialoauth.sites.renren.RenRen', 'socialoauth.sites.weibo.Weibo'...]
    
    # 取某站点名字对于的OAuth2类
    socialsites['renren']
    # 'socialoauth.sites.renren.RenRen'
    
