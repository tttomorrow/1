"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
"""
Case Type   : DML
Case Name   : row exclusive锁发生时进行并发读取
Description :
    1. 创建测试表并插入数据
    2. 开启事务，对表加row exclusive锁,不做提交，进行查询操作
    3. 开启新的事务，进行查询操作
    4. 清理环境
Expect      :
    1. 创建测试表并插入数据成功
    2. 开启事务，对表加row share锁,不做提交，进行查询操作成功
    3. 开启新的事务，进行查询操作成功，查询成功
    4. 清理环境
History     :
"""
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DmlTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_DML_Lock_Case0011开始')
        self.constant = Constant()
        self.commonsh1 = CommonSH('PrimaryDbUser')
        self.commonsh2 = CommonSH('PrimaryDbUser')
        self.tb_name = 't_lock_0011'

    def test_dml_lock(self):
        text1 = '-----step1: 创建测试表; expect: 创建表并插入数据成功-----'
        self.log.info(text1)
        sql_cmd = self.commonsh1.execut_db_sql(
            f"drop table if exists {self.tb_name};"
            f"create table {self.tb_name}(sk integer,id char(16),"
            f"name varchar(20),sq_ft integer);"
            f"insert into {self.tb_name} values (001,'sk1','tt',3332);")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, sql_cmd,
                      '执行失败:' + text1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text1)

        text2 = '-step2: 开启事务，对表加row exclusive锁,不做提交，进行查询操作; expect: 查询成功-'
        self.log.info(text2)
        sql = "start transaction;" \
              f"lock table {self.tb_name} in row exclusive mode;" \
              f"select * from {self.tb_name};" \
              f"select pg_sleep(5);"
        thread_1 = ComThread(self.commonsh1.execut_db_sql, args=(sql, ''))
        thread_1.setDaemon(True)
        thread_1.start()

        text3 = '-----step3: 开启新的事务，进行查询操作; expect: 查询成功-----'
        self.log.info(text3)
        sql = f"select pg_sleep(3);" \
              f"start transaction;" \
              f"select * from {self.tb_name};" \
              f"select pg_sleep(5);"
        thread_2 = ComThread(self.commonsh2.execut_db_sql, args=(sql, ''))
        thread_2.setDaemon(True)
        thread_2.start()

        thread_1.join(30)
        msg_result_1 = thread_1.get_result()
        self.log.info(msg_result_1)

        thread_2.join(10)
        msg_result_2 = thread_2.get_result()
        self.log.info(msg_result_2)

        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG
                      and self.constant.LOCK_TABLE_MSG,
                      msg_result_1, '执行失败:' + text2)
        self.assertIn('1 | sk1              | tt   |  3332',
                      msg_result_1, '执行失败:' + text2)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG,
                      msg_result_2, '执行失败:' + text3)
        self.assertIn('1 | sk1              | tt   |  3332',
                      msg_result_2, '执行失败:' + text3)

    def tearDown(self):
        text = '--step4: 清理环境; expect: 清理成功--'
        self.log.info(text)
        sql_cmd = self.commonsh1.execut_db_sql(
            f"drop table if exists {self.tb_name};")
        self.log.info(sql_cmd)
        self.log.info('Opengauss_Function_DML_Lock_Case0011结束')
