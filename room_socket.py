#!/usr/bin/env python
#-*-coding:utf-8-*-
__author__ = 'zhaojunming'
import json
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options

from room_manger import SqlManger
import md5Check
import room_mysql

class Upload(tornado.web.RequestHandler):
    def post(self,*args,**kwargs):
        filesName = str(self.get_argument('files'))
        upload_path = os.path.join(os.path.dirname(__file__), filesName)
        # 检查是否存在用户文件，不存在创建
        if not os.path.exists(upload_path):
            os.mkdir(upload_path)
        ret = {'result': 'OK'}
        file_metas = self.request.files.get('file', None)  # 提取表单中‘name’为‘file’的文件元数据
        if not file_metas:
            ret['result'] = 'Invalid Args'
            return ret
        for meta in file_metas:
            filename = meta['filename']
            file_path = os.path.join(upload_path, filename)
            with open(file_path, 'wb') as file:
                file.write(meta['body'])
                # OR do other thing
        self.write(json.dumps(ret))
        
# 群组房间管理类
# 剔除、禁言类
# 修改群组内成员权限等
class RoomManger(tornado.web.RequestHandler):
    """管理房间成员"""
    def get(self, *args, **kwargs):
        # 返回值
        return_msg = self.handleCode()
        self.write(return_msg)
        
    def post(self, *args, **kwargs):
        return_msg = self.handleCode()
        self.write(return_msg)
    
    def write_error(self, status_code,**kwargs):
        pass

    # chatrooms_list
    # users_list
    # code:0
    def destoryRoom(self,rname):
        return self.application.chathome.destoryRoom(rname)
    
    # code:1
    def getRoomMembers(self,rname):
        users = self.application.chathome.getRoomMembers(rname)
        message = []
        if users and len(users) > 0:
            for userModel in users:
                userinfo = {"name":userModel.name,"acc_status":userModel.acc_status,"timestamp":userModel.timestamp}
                message.append(userinfo)
        return json.dumps(message)
    
    # code:2
    # 1、自己主动退出，这个断开websocket就行，会自动剔除维护的用户和群组数组
    # 2、群组主动剔除某个人，这个需要调用这个方法
    def deleteMember(self,rname,uname):
        pass

    # code:3
    # 1、这个只能是群组主动禁言某人，成员无权限
    def controlSpeak(self,uname,iaBan):
        return self.application.chathome.changeStatus(uname,iaBan)

    def del_emptyroom(self):
        return self.application.chathome.del_emptyroom()

    def room_users_list(self):
        return json.dumps(self.application.chathome.chatrooms_list)

    # 处理各种类型
    def handleCode(self):
        return_msg = None
        order_coder = int(self.get_argument('code'))
        if order_coder == 0:
            rname = str(self.get_argument('rname'))
            return_msg = self.destoryRoom(rname)
        elif order_coder == 1:
            rname = str(self.get_argument('rname'))
            return_msg = self.getRoomMembers(rname)
        elif order_coder == 2:
            uname = str(self.get_argument('uname'))
            return_msg = self.deleteMember(uname)
        elif order_coder == 3:
            uname = str(self.get_argument('uname'))
            isban = int(self.get_argument('isban'))
            return_msg = self.controlSpeak(uname,isban)
        elif order_coder == 4:
            return_msg = self.del_emptyroom()
        elif order_coder == 5:
            return_msg = self.room_users_list()
        return return_msg

# websocket类：
# 处理发送/接受 数据
# 断开/连接用户
class newChatStatus(tornado.websocket.WebSocketHandler):
    '''websocket， 记录客户端连接，删除客户端连接，接收最新消息'''
    def on_pong(self, data):
        """Invoked when the response to a ping frame is received."""
        print "on_pong"

    def check_origin(self,origin):
        return True

    def open(self):
        uname = str(self.get_argument('uname'))
        rname = str(self.get_argument('rname'))
        # print "on_open",id(self),type(self),self.ws_connection,self.close_reason,self.close_code
        # self.write_message("on_open")
        # self.write_message(json.dumps({'from':uname, 'message':'Welcome chatroom %s' % rname}))      #向新加入用户发送首次消息
        self.application.chathome.register(self)    #记录客户端连接

    def on_close(self):
        # print "on_close",id(self),type(self),self.ws_connection,self.close_reason,self.close_code
        self.application.chathome.unregister(self)  #删除客户端连接

    def on_message(self, message):
        print message
        self.application.chathome.callbackNews(self, message)   #处理客户端提交的最新消息

class Application(tornado.web.Application):
    def __init__(self):
        # 管理用户类
        self.chathome = room_manger.ChatHome()
        # 数据库管理类
        self.sqlmanger = SqlManger()
        handlers = [
            (r'/chat', newChatStatus),
            (r'/info', RoomManger),
            (r'/upload', Upload),
        ]
        settings = {
            'template_path': 'html',
            'static_path': 'static'
        }
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(8500)
    tornado.ioloop.IOLoop.instance().start()
    # ch = roomManger.ChatHome()
    # socket = roomManger.Socket()
    # ch.register(socket)


    