#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 17:19:26
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
from wxpy import *

robot = Bot('bot.pkl',console_qr=True)

robot.auto_mark_as_read = True

@robot.register()
def new_friends(msg):
   # 处理好友逻辑代码
   print msg

embed()
# bot = Bot('bot.pkl',console_qr=True)
# '''
# 验证信息
# '''
# def valid_msg(msg):
#     return '运维密码' in msg.text.lower()

# def invite(user):
#     group =  bot.groups().search('“运维密码”体验群')
#     group[0].add_members(user, use_invitation=True)


# '''
# 处理加好友信息
# '''
# @bot.register(msg_types=FRIENDS)def new_friends(msg):
#     user = msg.card.accept()
#     if valid_msg(msg):
#         invite(user)
#     else:
#         user.send('Hello {}，你忘了填写加群口令，快回去找找口令吧'.format(user.name))