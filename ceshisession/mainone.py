#!/usr/bin/env python
#coding:utf-8

import tornado.ioloop
import tornado.web                              #导入tornado模块下的web文件
import session_lei                              #导入session模块




class indexHandler(tornado.web.RequestHandler):  #定义一个类，继承tornado.web下的RequestHandler类
    def get(self):                               #get()方法，接收get方式请求
        session = session_lei.Session(self,1)    #创建session对象，cookie保留1天
        if session['zhuangtai'] == True:         #判断session里的zhuangtai等于True
            self.render("index.html")            #显示查看页面
        else:
            self.redirect("/dlu")                #跳转到登录页面

class dluHandler(tornado.web.RequestHandler):
    def get(self):
        session = session_lei.Session(self,1)    #创建session对象，cookie保留1天
        if session['zhuangtai'] == True:         #判断session里的zhuangtai等于True
            self.redirect("/index")              #跳转到查看页面
        else:
            self.render("dlu.html",tishi = '请登录')  #打开登录页面
    def post(self):
        yhm = self.get_argument('yhm')               #接收用户提交的用户名
        mim = self.get_argument('mim')               #接收用户提交的密码
        if yhm == 'admin' and mim == 'admin':        #判断用户名和密码
            session = session_lei.Session(self,1)    #创建session对象，cookie保留1天
            session['yhm'] = yhm                     #将用户名保存到session
            session['mim'] = mim                     #将密码保存到session
            session['zhuangtai'] = True              #在session写入登录状态
            self.redirect("/index")                  #跳转查看页面
        else:
            self.render("dlu.html",tishi = '用户名或密码错误') #打开登录页面

settings = {                                        #html文件归类配置，设置一个字典
    "template_path":"views",                     #键为template_path固定的，值为要存放HTML的文件夹名称
    "static_path":"statics",                         #键为static_path固定的，值为要存放js和css的文件夹名称
}

#路由映射
application = tornado.web.Application([         #创建一个变量等于tornado.web下的Application方法
    (r"/index", indexHandler),                   #判断用户请求路径后缀是否匹配字符串index,如果匹配执行MainHandler方法
    (r"/dlu", dluHandler),
],**settings)                                   #将html文件归类配置字典，写在路由映射的第二个参数里

if __name__ == "__main__":
    #内部socket运行起来
    application.listen(8888)                    #设置端口
    tornado.ioloop.IOLoop.instance().start()