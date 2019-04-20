#!/usr/bin/env python
#-*-coding:utf-8-*-
__author__ = 'zhaojunming'
import time
import threading

def checkrooms(room_list):
	print room_list
	for key,r_model in room_list.items():
		if len(r_model)==0:
			room_list.pop(key)
	print room_list
		
def startDaemon():
	d = {"k1":["v1"],"k2":["v2","v22"],"k3":["v3","v2","v2"],"k4":["v4"],"k5":[]}
	checkrooms(d)
	t = threading.Thread(target=checkrooms,args=d)
	# t.setDaemon(True)
	t.start()

if __name__ == "__main__":
	while True:
		time.sleep(5)
		startDaemon()
