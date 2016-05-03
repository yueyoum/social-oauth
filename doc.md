# socialoauth

##### 欢迎使用 socialoauth，目前版本 0.3.0，更新于 2013-06-11

[版本历史](/ChangeLog)


## 属性

对于一个站点的实例，用户需要关心的有以下属性：

    site_name
    site_name_zh

这两个属性是在settings文件中配置的。[如何配置settings](#-settingspy)
如果这个实例在用户认证完毕，成功调用 `get_access_token` 后，还会拥有下列属性

    uid             -   此站点上的用户uid
    username        -   名字
    avatar          -   小头像 （各个站点尺寸不一，大概为50x50）
    access_token    -   用于调用API



## 使用SocialSites类

自0.3.0版本后，不用在项目初始化的时候调用 `socialuser.config()`.
现在只在需要的地方调用即可

```python
from socialoauth import SoicalSites
def index():
    socialsites = SoicalSites(SOCIALOAUTH_SITES)

    socialsites.list_sites_name()           # 列出全部的站点名字
    socialsites.list_sites_class()          # 列出全部的站点Class名字
    socialsites.get_site_object_by_name()   # 根据站点名字获取此站点实例
    socialsites.get_site_object_by_class()  # 根据站点Class名字获取此站点实例
```


## 如何配置 settings.py

这就是配置文件，其实在你的应用中你可以随意换其他名字。

配置示例（模板参考 example/settings.py.example）:

```python
SOCIALOAUTH_SITES = (
    ('renren', 'socialoauth.sites.renren.RenRen', '人人',
        {
         'redirect_uri': 'http://test.codeshift.org/account/oauth/renren',
         'client_id': 'YOUR ID',
         'client_secret': 'YOUR SECRET',
        }
    ),

    ('weibo', 'socialoauth.sites.weibo.Weibo', '新浪微博',
        {
          'redirect_uri': 'http://test.codeshift.org/account/oauth/weibo',
          'client_id': 'YOUR ID',
          'client_secret': 'YOUR SECRET',
        }
    ),

    ('qq', 'socialoauth.sites.qq.QQ', 'QQ',
        {
          'redirect_uri': 'http://test.codeshift.org/account/oauth/qq',
          'client_id': 'YOUR ID',
          'client_secret': 'YOUR SECRET',
        }
    ),

    ('douban', 'socialoauth.sites.douban.DouBan', '豆瓣',
        {
          'redirect_uri': 'http://test.codeshift.org/account/oauth/douban',
          'client_id': 'YOUR ID',
          'client_secret': 'YOUR SECRET',
          'scope': ['douban_basic_common']
        }
    ),
)
```

配置的 template 就是这样：

```python
SOCIALOAUTH_SITES = (
    (site_name, site_oauth2_module_class_path, site_name_zh,
                site_oauth2_parameter
    )
```

`SOCIALOAUTH_SITES` 是此配置的名字，同样，你也可以随意更改

*   `SOCIALOAUTH_SITES` 是一个列表/元组，每个元素表示一个站点配置

*   每个站点的配置同样是列表/元组。

    *   第一个元素 站点名字。你可以随意取名字，但必须和 回调地址 `redirect_uri` 中的 站点标识 一样
        比如上面设置中的 `douban`，这个名字就必须和 redirect_uri 中的最后的名字一样，
        所以你也可以这样修改：

            'nimei': ('xxx'
                     {
                        'redirect_uri': 'http://test.org/account/oauth/nimei',
                     }
            )

    *   第二个元素 指定此站点的 OAuth2 类的包结构关系路径

    *   第三个元素是站点中文名字，可以用于在web页面上显示

    *   第四个元素为字典，里面设置了一个OAuth2应用必须的设置项。

        *   `client_id`, `client_secret`是申请开发者，创建好应用后的值

        *   `redirect_uri` 是在用户授权后的回调地址

        *   `scope`是选填的一项，在于某些API需要`scope`权限申请。具体的参考各个站点自己的文档


## socialoauth 认证流程

可以参考 `example/index.py` 中的例子


1.  得到 引导用户 授权的url

    ```python
    from socialoauth import SocialSites

    socialsites = SocialSites(SOCIALOAUTH_SITES)
    for s in socialsites.list_sites_class():
        site = socialsites.get_site_object_by_class(s)
        authorize_url = site.authorize_url
    ```

2.  引导用户授权后，浏览器会跳转到你设置的 `redirect_uri`，在这里要取到 `access_code`,
    并且进一步用 `access_code` 换取到 `access_token`.

    *注意这里的错误处理*

    假如你的 `redirect_uri` 对应的 views 处理函数为 `callback`， 如下所示：

    ```python
    from socialoauth import SocialSites, SocialAPIError

    def callback(request, sitename):
        # sitename 参数就是从 redirect_uri 中取得的
        # 比如 我在 settings.py.example 中设置的那样
        # renren 的 redirect_uri 为 http://test.org/account/oauth/renren
        # 那用web框架url的处理功能把 'renren' 取出来，作为sitename 传递给 callback 函数

        # request 是一个http请求对象，不同web框架传递此对象的方式不一样

        # 网站在用户点击认证后，会跳转到 redirect_uri， 形式是 http://REDIRECT_URI?code=xxx
        # 所以这里要取到get param code

        code = request.GET.get('code')
        if not code:
            # 认证返回的params中没有code，肯定出错了
            # 重定向到某处，再做处理
            redirect('/SOME_WHERE')

        socialsites = SoicalSites(SOCIALOAUTH_SITES)
        s = socialsites.get_site_object_by_name(sitename)

        # 用code去换取认证的access_token
        try:
            s.get_access_token(code)
        except SocialAPIError as e:
            # 这里可能会出错
            # e.site_name      - 哪个站点的OAuth2发生错误？
            # e.url            - 当时请求的url
            # e.error_msg      - 这里是由api返回的错误信息, 或者urllib2的错误信息

            # 就在这里处理错误

        # 到这里就处理完毕，并且取到了用户的部分信息： `uid`, `name`, `avatar`
    ```

3.  第二步顺利过完，整个流程也就结束了。

*   如果只需要 *第三方登录* 这个功能，这里取到了用户基本信息。也就足够了
*   如果还要更进一步操作更多用户资源，那么就要保存 `s.access_token` 作为后续调用API所用
*   这里取到的 `uid` 是字符串，目前除了腾讯的openid，其他站点的都可以转为int



## 如何扩展

要添加新的站点，正常网站只需要简单几步。（不正常网站比如腾讯，那就得多几步！）

1.  `cd social-oauth/socialoauth/sites`
2.  `vim new_site.py`

```python
#  this is new_site.py
from socialoauth.sites.base import OAuth2

class NewSite(OAuth2):
    AUTHORIZE_URL = 'https://xxx'
    ACCESS_TOKEN_URL = 'https://xxx'

    # 这两条url从站点文档中取到，
    # 第一个是请求用户认证的URL，
    # 第二个是根据第一步转到回调地址传会的code取得access_token的地址

    # RESPONSE_ERROR_KEY = 'xxx'
    # 某些网站在你api错误请求的时候，并没有设置http response code，
    # 其值依然是200，就像一个成功请求那样。但它是在返回的json字符串中
    # 有 RESPONSE_ERROR_KEY 的值
    # 比如 返回是这样 {'error_code': 1111, ...}
    # 那么这里就设置 RESPONSE_ERROR_KEY = 'error_code'
    # api_call_get 和 api_call_post 就会自动处理这些错误

    # 但如果站点还不是上述两种方式来表示错误
    # 那么就得你自己来处理错误
    # 通常是 raise SocialAPIError(site_name, url, response_content)


    @property
    def authorize_url(self):
        # 一般情况都不用重写此方法，只有一些特殊站点需要添加特殊参数的时候，
        # 再按照下面这种方式重写
        # url 中 已经有了 client_id, response_type, redirect_uri,
        # scope(如果在settings.py设置了 SCOPE)
        # 然后再加上这个站点所需的特殊参数即可
        url = super(NewSite, self).authorize_url
        return url + 'xxxxx'


    def build_api_url(self, url):
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

        # return url

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
        # 一般都不用重写此方法
        # 只是部分殊站点，比如豆瓣他的认证需要你设置header
        # 就重写此方法，req 是 urllib2.Reqeust 实例
        # req.add_header(name, value)



    def parse_token_response(self, res):
        # res 是请求access_token后的返回。
        # 在这里要取到此授权用户的基本信息，uid, name, avatar等
        # 各个站点在这里的差异较大
```


这样一个OAuth2的client就写完了， 然后你还需要把于此站点有关的设置添加到 settings.py中

