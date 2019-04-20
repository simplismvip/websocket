#!/usr/bin/env python
#-*-coding:utf-8-*-
__author__ = 'zhaojunming'
import time
import threading
import pymysql

# 格式化文件写入数据库
class SqlManger(object):
	def __init__(self,socket):
		super(SqlManger,self).__init__()
		self.socket = socket;
		# xhzd_surnfu
		self.db = pymysql.connect(host="47.105.185.248",user="remote_test",passwd="18245393563",db="new_data",charset='utf8')
	
	def update(self,sql):
		# 打开数据库连接
		# 使用cursor()方法获取操作游标 
		try:
			with self.db.cursor() as cursor:
				cursor.execute(sql)
				self.db.commit()
		except Exception as e:
			print 'updata Error:%s!!!' % e
		finally:
			self.db.close()

	def readData(self,sql):
		try:
			with self.db.cursor() as cursor:
				cursor.execute(sql)
				results = cursor.fetchall()
				for row in results:
					name = row[0]
					age = row[1]
					print age,name
		except Exception as e:
			print 'readData Error:%s' % e
		finally:
			self.db.close()

if __name__ == "__main__":
	sql = SqlManger('socket')
	sql.readData('select * from students;')

'''
# 参加数据库
CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(255) COLLATE utf8_bin NOT NULL,
    `password` varchar(255) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1 ;

# 查询数据库
import pymysql.cursors
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='user',
                             password='passwd',
                             db='db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()

'''
