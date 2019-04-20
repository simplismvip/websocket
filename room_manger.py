#!/usr/bin/env python
#-*-coding:utf-8-*-

__author__ = 'zhaojunming'
from uuid import uuid4
import json
import time

class Socket(object):
    """docstring for Socket"""
    ws_connection = True
    def get_argument(self,key):
        return self.map.get(key)

    def write_message(self,msg):
        print msg

 ######## 房间模型 ########
class RoomModel(object):
    """房间模型"""
    def __init__(self,rname):
        super(RoomModel, self).__init__()
        self.room_name = rname
        # self.room_id = "room-tony"
        # "room:" + str(uuid4())
        self.timestamp = str(int(time.time()))
        self.users = []

######## 用户模型类  ########
class UserModel(object):
    """用户模型"""
    def __init__(self,username):
        super(UserModel, self).__init__()
        self.name = username
        # self.name_id = "user-tony"
        # "user:" + str(uuid4())
        self.authority = 0
        self.acc_status = 1
        self.timestamp = str(int(time.time()))
        self.rooms = []

######## 主要处理聊天类  ########
class ChatHome(object):
    '''处理websocket 服务器与客户端交互'''
    # 所有注册信息映射，注册时首先检查这个映射，存在的话
    # 群组映射
    chatrooms_list = {}
    # 用户映射
    users_list = {}
    # 检测是否有空的数组，
    # 如果为空则认为是退出房间，删除之
    def del_emptyroom(self):
        for key,r_model in self.chatrooms_list.items():
            if len(r_model.users)==0:
                ctime = int(time.time())
                ltime = int(r_model.timestamp)
                if (ctime - ltime) > 7200:
                    self.chatrooms_list.pop(key)
        print self.chatrooms_list

    # 摧毁房间
    def destoryRoom(self,rname):
        roomModel = self.chatrooms_list.get(rname)
        # 1、删除房间成员
        if roomModel:
            for usermodel in roomModel.users[::-1]:
                if not roomModel.users:
                    # 1、接着需要再全局数组中删除对应的用户
                    # 退出房间意味着用户断开websocket连接，因此这里执行删除。
                    users_list.pop(usermodel.name)
                    # 2、删除房间成员
                    roomModel.remove(usermodel)

            # 删除房间
            self.leaveRoom(False,rname)
            return json.dumps({"code":"1","desc":"success"})
        else:
            return json.dumps({"code":"0","desc":"none user"})

    # 获取房间成员列表
    def getRoomMembers(self,rname):
        roomModel = self.chatrooms_list.get(rname)
        if roomModel:
            return roomModel.users

    # 修改用户授权
    def changeAuthori(self,uname,code):
        userModel = self.users_list.get(uname)
        if userModel:
            userModel.authority = code

    # 修改用户状态
    def changeStatus(self,uname,code):
        userModel = self.users_list.get(uname)
        if userModel:
            userModel.acc_status = code
            return json.dumps({"code":"1","desc":"success"})
        else:
            return json.dumps({"code":"0","desc":"none user"})

    # 用户退出房间时调用离开房间
    def leaveRoom(self,is_user,key):
        temp_list = self.users_list if is_user else self.chatrooms_list
        try:
            # 1、第一步，从当前用户数组中删除
            temp_list.pop(key)
            # 2、第二步，从roomModel的users属性数组中删除。相当于从房间中剔除
            # 调用 def roomModelUsersDel(self,key,usermodel): 方法
        except Exception as e:
            print "leaveRoom 不存在"

    # 用户退出房间时调用离开房间
    def roomModelUsersDel(self,key,usermodel):
        try:
            # 找到群组模型
            chatModel = self.chatrooms_list(key)
            # 删除退出的成员
            chatModel.users.remove(usermodel)
        except Exception as e:
            print "roomModelUsersDel 不存在"

######################################################
    def checkModelExist(self,is_user,key):
        # python 的三目运算符
        temp_list = self.users_list if is_user else self.chatrooms_list
        return temp_list.get(key) 

    def createRoom(self,user):
        # 已经加入了其他房间，无法参加新房间
        if len(user.rooms) > 0:
            return 0
        else:
            # 开始创建房间，并加入
            room_model = RoomModel()
            room_model.room_name = str(user.niak_name)
            # 自己加入这个房间
            room_model.users.append(user)
            # 加入房间列表
            self.chatrooms_list.append(room_model)

    # 释放存在该用户，
    # 1、存在直接返回，
    # 2、不存在执行注册
    # 3、注册完成后添加到用户列表
    # 4、检查是否加入群组，加入群组后通知加入
    # 参数：
    # order_code:
    # uuid:用户名
    # hpic:头像
    # udesc:用户描述
    # auth:用户授权
    # status:用户状态

    # rname:房间名
    # rdesc:房间描述
    def register(self, socket):
        '''注册新用户，并且直接加入房间。保存新加入的客户端连接、监听实例，并向聊天室其他成员发送消息！'''
        # 获取命令类型
            # 0:注册
            # 1:加入房间
        # order_code = int(socket.get_argument('order_code'))
        # 谁 name
        uname = str(socket.get_argument('uname'))
        # 返回一个列表[状态,user]
        user_find = self.checkModelExist(True,uname)
        # 临时记录房间、用户模型
        room_temp = None
        user_temp = user_find
        if user_find:
            print "register 函数调用，代表找到了加入用户"
            #### 每个用户带一个socket,用户存在代表有socket
            # user_find.socket = socket
            # 1、存在，检查房间是否存在
            rname = str(socket.get_argument('rname'))
            room_find = self.checkModelExist(False,rname)
            if room_find:
                # 0、当前用户是否已经在在房间中
                uname_esixt_room = False
                for u_mdel in room_find.users:
                    if u_mdel.name == uname:
                        uname_esixt_room = True
                        print "************* find out *************"
                        break
                # m没找到的情况下进入添加
                if not uname_esixt_room:
                    # 1、存在，直接加入
                    room_find.users.append(user_find)

                    # 2、设置账户权限为加入者
                    user_find.authority = 0
                    user_find.acc_status = 1

                    ####赋值给临时模型
                    room_temp = room_find

            else:
                # 1、不存在，创建房间。加入房间到房间列表
                new_room = RoomModel(rname)
                # 2、加入房间
                new_room.users.append(user_find)
                # 3、设置账户权限为加入者
                user_find.authority = 1
                user_find.acc_status = 1
                ####赋值给临时模型
                room_temp = new_room

                # 3、添加到全局房间映射
                self.chatrooms_list[rname] = new_room
        else:
            # 1、初始化用户模型，存入数组
            new_user = UserModel(uname)
            new_user.name = uname
            new_user.acc_status = 1
            # 给临时用户模型赋值
            user_temp = new_user

            #### 每个用户带一个socket
            new_user.socket = socket;

            # 3、添加到全局用户映射
            self.users_list[uname] = new_user

            # 2、检查房间是否存在
            rname = str(socket.get_argument('rname'))
            room_find = self.checkModelExist(False,rname)
            if room_find:
                # 1、存在，直接加入
                room_find.users.append(new_user)

                # 2、设置账户权限为加入者
                new_user.authority = 0

                ####赋值给临时模型
                room_temp = room_find
            else:
                # 1、不存在，创建房间. 加入房间到房间列表
                new_room = RoomModel(rname)
                self.chatrooms_list[rname] = new_room
                
                # 2、加入房间
                new_room.users.append(new_user)
                
                # 3、设置账户权限为加入者
                new_user.authority = 1

                ####赋值给临时模型
                room_temp = new_room

        message = {
            'from': user_temp.name,
            'message': '%s Join chatroom success' % user_temp.name,
            'status':"1"
        }
        print "************* find out callbackTrigger run *************"
        self.callbackTrigger(room_temp, message)

    def unregister(self, lefter):
        '''客户端关闭连接，删除聊天室内对应的客户端连接实例'''
        # 退出登陆账户
        unameStr = str(lefter.get_argument('uname'))
        rnameStr = str(lefter.get_argument('rname'))
        message = {
            'from': unameStr,
            'message': '%s Leave chatroom success（%s）' % (unameStr, rnameStr),
            'status':"0"
        }

        # 检查用户在那个房间，检查用户在房间权限
        # 如果时创建者摧毁房间
        unameModel = self.checkModelExist(True,unameStr)
        # 注销登陆，从总数组中删除用户
        self.leaveRoom(True,unameStr)
        # 发送离开房间消息
        chatroom = self.checkModelExist(False,rnameStr)
        if unameModel and chatroom:
            chatroom.users.remove(unameModel)

            # self.roomModelUsersDel(rnameStr,unameModel)
        # if unameModel.authority == 1:
            # 退出房间
            # self.destoryRoom(rnameStr)
        self.callbackTrigger(chatroom, message)

    def callbackNews(self, sender, message):
        '''处理客户端提交的消息，发送给对应聊天室内所有的客户端'''
        # 谁、向那个房间发送了消息
        uuidStr = str(sender.get_argument('uname'))
        user = self.checkModelExist(True,uuidStr)

        rnameStr = str(sender.get_argument('rname'))
        chatroom = self.checkModelExist(False,rnameStr)
        # status:0 离开
        # status:1 加入
        # status:2 发送消息
        message = {
            'from': user.name,
            'message': message,
            'status':"2"
        }
        self.callbackTrigger(chatroom, message)

    def callbackTrigger(self, room, message):
        '''消息触发器，将最新消息返回给对应聊天室的所有成员'''
        print "--##当前群组##--：%s" % room.room_name
        for umodel in room.users:
            print "***消息发给***",umodel.name
            #,umodel.acc_status,umodel.authority,id(umodel.socket),type(umodel.socket),umodel.socket.ws_connection
            if (umodel.acc_status == 1) and umodel.socket.ws_connection:
                # print umodel.socket
                umodel.socket.write_message(json.dumps(message))

if __name__ == '__main__':
    ch = ChatHome()
    socket = Socket()
    socket.map = {"uname":"tony","rname":"room-test"}
    
    ch.register(socket)
    socket.map = {"uname":"jack","rname":"room-test"}

    ch.register(socket)
    socket.map = {"uname":"jhon","rname":"room-test"}
    ch.register(socket)

    # for rmodel in ChatHome.chatrooms_list.values():
    #     print rmodel.room_name
    #     for umodel in rmodel.users:
    #         print umodel.name
    # print ChatHome.chatrooms_list
    # print ChatHome.users_list


    