# socialoauth

Python Package For SNS sites with OAuth2 support

`socialoauth` 专注于中国大陆开放了OAuth2认证的网站


## Feature

*   易于扩展 [参见doc.md](/doc.md)
*   统一的接口
    
    *   各个站点，都有 `uid`, `name`, `avatar`, 属性
    
        QQ 取回的 `avatar` 是40x40尺寸的，其余站点基本都是 48~50的尺寸

    *   各个站点，都有统一的 `api_http_get` 和 `api_http_post` 接口

*   统一的错误处理

    `api_http_get` 和 `api_http_post` 都可能引发异常，
    
    应用程序只要 `try ... except SocialAPIError as e` 就能得到一致的错误信息：
    
    *   `e.site_name`         哪个站点发生错误
    *   `e.url`               发生错误是请求的url
    *   `e.api_error_msg`     由站点返回的错误信息 or urllib2 的错误信息


## Supported sites

*   人人
*   腾讯
*   豆瓣
*   新浪微博
*   网易微博
*   搜狐微博
*   百度
*   开心网
*   淘宝


## Contributors

Thanks for this guys

[Jiequan](https://github.com/Jiequan)

[smilekzs](https://github.com/smilekzs)

[andelf](https://github.com/andelf)

[zxkane](https://github.com/zxkane)

[yuanxu](https://github.com/yuanxu)


## Install

```bash
pip install socialoauth

# or

git clone https://github.com/yueyoum/social-oauth.git
cd social-oauth
python setup.py install
```



## Example

快速体验 socialoauth

```bash
git clone https://github.com/yueyoum/social-oauth.git
cd social-oauth/example
cp settings.py.example settings.py

# 在这里按照你的情况修改settings.py

python index.py
```

如何配置 settings.py ?  [参见doc.md](/doc.md)

现在用浏览器打开对应的地址，就能体验相应的功能。

下面是我用 人人网 帐号登录的过程：


##### 初始情况，首页只有一个 login 链接

![step1](http://i1297.photobucket.com/albums/ag23/yueyoum/x1_shadowed_zpsac1e046a.png)


##### 点击后，根据settings.py中的设置，显示可用的认证网站

![step2](http://i1297.photobucket.com/albums/ag23/yueyoum/x2_shadowed_zps47bd6fd8.png)


##### 我用人人网帐号进行测试，点击后，转到人人登录认证的界面

![step3](http://i1297.photobucket.com/albums/ag23/yueyoum/x4_shadowed_zps6aed31ec.png)


##### 认证完毕后，就会显示用户的名字和小头像。
example中有个简单的session机制，
此时再打开首页（不关闭浏览器）就不用再登录，会直接显示名字和头像

![step4](http://i1297.photobucket.com/albums/ag23/yueyoum/x3_shadowed_zpse6a0f575.png)



## Document

[参见doc.md](/doc.md)


## 吐槽

*   新浪微博，腾讯, 开心网的文档是最好的。
*   人人网文档虽然内容丰富，但层次略混乱
*   豆瓣文档太简陋
*   搜狐文档就是个渣！！！ 都不想添加搜狐支持了
*   发现一些文档和实际操作有出入， 主要是文档里说的必要参数，不传也一样工作
    
    *   [腾讯][tocao_tencent_1] 文档里说取code的时候，state 必须 参数，但发现不传一样
    *   [搜狐][tocao_souhu_1] 和上面一样， wrap_client_state 参数


[tocao_tencent_1]: http://wiki.opensns.qq.com/wiki/【QQ登录】使用Authorization_Code获取Access_Token
[tocao_souhu_1]: http://open.t.sohu.com/en/使用Authorization_Code获取Access_Token
[Jiequan]: https://secure.gravatar.com/avatar/1fc3c2ed714e2c2a26822ede8a927eac?s=50&d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-user-420.png
[smilekzs]: https://secure.gravatar.com/avatar/405626e107e40527578e65b05a5f7541?s=50&d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-user-420.png
[andelf]: https://secure.gravatar.com/avatar/0478b87ec69ce7ce034d370f326c50aa?s=50&d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-user-420.png

