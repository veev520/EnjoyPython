# -*- coding: utf-8 -*-
# @Date     : 2017/12/3 15:14
# @Author   : xiaochuang.wu
# @File     : dbutils.py

import pymysql


# 数据库操作类
class DBInstance(object):
    # 数据列的数据类型
    COLUMN_TYPES = ['string', 'int', 'string', 'string']

    def __init__(self):
        # self.db = pymysql.connect("127.0.0.1", "root", "123456", "py_test", charset='utf-8')
        self.db = pymysql.connect(host="127.0.0.1",
                                  port=3306,
                                  user="root",
                                  passwd="123456",
                                  db="py_test",
                                  charset='utf8')
        self.cursor = self.db.cursor()

    @staticmethod
    def tostring(target):
        ret = ""
        for val in target:
            ret += ',' + val
        return ret[1:]

    @staticmethod
    def dict_tostring(target, column_type, link=','):
        ret = ''
        for column, value in target.items():
            if column_type[column] == 'string':
                ret += ' ' + link + ' ' + column + '=' + "'" + str(value) + "'"
            else:
                ret += ' ' + link + ' ' + column + '=' + str(value)
        print(ret[len(link) + 1:])
        return ret[len(link) + 1:]

    def exec_commit(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print('sql is : %s' % sql)
        except Exception as e:
            print('excute error sql:%s : %s ' % (sql, e))
        # pass

    def query_record(self, tname):
        """查询全表所有信息，传入表名"""
        sql = 'select * from %s' % tname
        number = self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        for row in ret:
            print(row)
        print('query data number is: %s' % number)

    def add_record(self, tname=None, values=None, columns=None):
        """
        :param tname: 表名 字符串类型
        :param values: 插入的值 元祖类型
        :param columns: 插入的列名 元祖或者列表
        :return:
        """
        # insert into user values('askdf','goden',1,'asdfadf');
        # insert into user(openid, nickname, sex, unionid) values('askdf','goden',1,'asdfadf');
        if not columns:
            sql = "INSERT INTO %s VALUES %s" % (tname, values)
            # sql = join_arrays(sql, values)
        else:
            columns = self.tostring(columns)
            sql = "INSERT INTO %s (%s) VALUES %s" % (tname, columns, values)
        self.exec_commit(sql)

    # def update_record(self, tname, condition, result):
    #     """表名，条件，赋值"""
    #     if not condition:
    #         sql = 'update %s set %s' % (tname, result)
    #     else:
    #         sql = 'update %s set %s where %s' % (tname, result, condition)
    #     self.exec_commit(sql)

    def update_record1(self, tname, condition={}, result={}, columns_type={}):
        """表名，条件，赋值, 数据类型（指定操作列的数据类型）"""
        if not condition:
            sql = 'update %s set %s' % (tname, self.dict_tostring(result))
        else:
            sql = 'update %s set %s where %s' % (tname, self.dict_tostring(result, columns_type), self.dict_tostring(condition, columns_type, link='and'))
        self.exec_commit(sql)

    def del_record(self, tname, condition={}, columns_type={}):
        """表名，条件"""
        sql = 'delete from %s where %s' % (tname, self.dict_tostring(condition, columns_type, link='and'))
        self.exec_commit(sql)

    def __del__(self):
        """关闭数据库连接"""
        self.cursor.close()
        self.db.close()
        print('resource is released')


if __name__ == '__main__':
    db = DBInstance()
    # db.add_record('user', values=(0, 'wxc', 1, 'asfd', 'alsdfakf'))
    db.add_record('user', values=('12306', '王伟', 1, '6666'), columns=('openid', 'nickname', 'sex', 'unionid'))
    db.query_record('user')

    condition = {
        'nickname': 'skk',
        'sex': 1
    }

    set_ret = {
        'sex': 1,
        'nickname': 'skk'
    }

    coltype = {
        'nickname': DBInstance.COLUMN_TYPES[0],
        'sex': DBInstance.COLUMN_TYPES[1]
    }
    # db.update_record1('user', condition=condition, result=set_ret, columns_type=coltype)
    # db.del_record('user', condition=condition, columns_type=coltype)

    # dict_tostring(condition)
    # dict_tostring(set_ret)

