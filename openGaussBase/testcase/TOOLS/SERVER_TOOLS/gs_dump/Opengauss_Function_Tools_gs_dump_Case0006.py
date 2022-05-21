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
Case Type   : 服务端工具
Case Name   : 导出数据库时指定verbose模式
Description :
    1.连接数据库：
    2.创建数据库
    3.切换到数据库test
    4.创建表并插入数据：
    5.退出数据库
    6.source环境变量
    7.导出数据库时指定verbose模式
    8.连接数据库，清理环境
Expect      :
    1.数据库连接成功
    2.创建数据库test成功
    3.切换到数据库test
    4.创建表并插入数据成功
    5.退出数据库
    6.source环境变量
    7.导出失败
    8.清理环境成功
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('----Opengauss_Function_Tools_gs_dump_Case0006start----')
        self.dbusernode = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        LOG.info('---------连接数据库并创建数据库---------')
        sql_cmd1 = '''drop database if exists testdump;
            create database testdump;
            '''
        excute_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.dbusernode.db_name} ' \
            f'-p {self.dbusernode.db_port} ' \
            f'-c "{sql_cmd1}";'
        LOG.info(excute_cmd1)
        msg1 = self.dbusernode.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, msg1)
        LOG.info('---------在创建好的数据库中创建表并插入数据----------')
        sql_cmd2 = '''drop table if exists test1; 
            create table test1 (id int ,name char(10));
            insert into test1 values (1,'aa'),(2,'bb');
            '''
        excute_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d testdump ' \
            f'-p {self.dbusernode.db_port}' \
            f' -c "{sql_cmd2}";'
        LOG.info(excute_cmd2)
        msg2 = self.dbusernode.sh(excute_cmd2).result()
        LOG.info(msg2)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg2)
        LOG.info('----------导出数据库时指定verbose模式---------')
        excute_cmd3 = f'''source {macro.DB_ENV_PATH} ;
            gs_dump -p {self.dbusernode.db_port} testdump -v
            '''
        LOG.info(excute_cmd3)
        msg3 = self.dbusernode.sh(excute_cmd3).result()
        LOG.info(msg3)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, msg3)

    def tearDown(self):
        LOG.info('---------清理环境：删除数据库----------')
        sql_cmd4 = '''drop database if exists testdump; '''
        excute_cmd4 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.dbusernode.db_name} ' \
            f'-p {self.dbusernode.db_port} ' \
            f'-c "{sql_cmd4}";'
        LOG.info(excute_cmd4)
        msg4 = self.dbusernode.sh(excute_cmd4).result()
        LOG.info(msg4)
        LOG.info('---Opengauss_Function_Tools_gs_dump_Case0006finish---')
