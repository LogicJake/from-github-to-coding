# from-github-to-coding
将github仓库备份到coding
### 使用步骤
* clone仓库
* 在https://github.com/settings/tokens Generate new token，申请repo：Full control of private repositories权限即可，记住新生成的token。
* 打开main.py修改参数。
### 参数说明
打开main.py，开头有4个参数变量。
* cookie：登陆coding账号，打开浏览器开发者工具，刷新coding页面，在网络请求中，复制Request Headers中的Cookie一项。主要用作在coding中创建项目。
* github_name：github用户名
* coding_name：Coding用户名
* token：之前申请的github的token，用作Github的api请求
