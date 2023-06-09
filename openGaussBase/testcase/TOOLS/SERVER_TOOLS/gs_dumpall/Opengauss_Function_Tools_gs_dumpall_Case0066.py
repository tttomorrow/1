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
Case Name   : 导出数据时指定所连接的转储全局对象的数据库名称
Description :
    1.连接数据库：
    2.创建数据
    3.退出数据库
    4.source环境变量
    5.导出数据时指定所连接的转储全局对象的数据库名称
    6.连接数据库，清理环境
Expect      :
    1.数据库连接成功
    2.创建数据成功
    3.退出数据库
    4.source环境变量
    5.导出是失败
    6.清理环境成功
History     :
"""
import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Case0066start----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        LOG.info('------------创建数据-------------')
        sql_cmd1 = '''
            drop database if exists  db_test;
            create database db_test;
            drop user if exists user1; 
            create user user1 identified by 'qwer@123';
            grant all privileges to user1;
                        '''
        gsql_cmd1 = f'''
            source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} -p\
            {self.dbuser_node.db_port} -c "{sql_cmd1};"'''
        LOG.info(gsql_cmd1)
        sql_msg1 = self.dbuser_node.sh(gsql_cmd1).result()
        LOG.info(sql_msg1)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_msg1)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_msg1)
        sql_cmd2 = '''
            drop table if exists test1; 
            create table test1 (id int ,name char(10));
            insert into test1 values (1,'aa'),(2,'bb');
                                '''
        gsql_cmd2 = f'''
            source {macro.DB_ENV_PATH} ;
            gsql -d db_test -p {self.dbuser_node.db_port} -c "{sql_cmd2}";
                        '''
        LOG.info(gsql_cmd1)
        gsql_msg = self.dbuser_node.sh(gsql_cmd2).result()
        LOG.info(gsql_msg)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, gsql_msg)

        LOG.info('--导出数据时指定所连接的转储全局对象的数据库名称--')
        dumpall_cmd =\
            f"source {macro.DB_ENV_PATH} ;" \
            f"gs_dumpall " \
            f"-p {self.dbuser_node.db_port} " \
            f"-l db_test " \
            f"-U user1 " \
            f"-W qwer@123;"
        LOG.info(dumpall_cmd)
        dumpall_msg = self.dbuser_node.sh(dumpall_cmd).result()
        LOG.info(dumpall_msg)
        self.assertIn('CREATE TABLE test1', dumpall_msg)
        self.assertIn('COPY test1 (id, name) FROM stdin;', dumpall_msg)
        self.assertIn('CREATE ROLE user1', dumpall_msg)

    def tearDown(self):
        LOG.info('---清理环境---')
        sql_cmd3 = '''  
            drop user  user1;
            drop database  db_test;
                         '''
        clear_cmd = f'''
            source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name}\
            -p {self.dbuser_node.db_port} -c "{sql_cmd3}";
                          '''
        LOG.info(clear_cmd)
        clear_msg = self.dbuser_node.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Case0066finish----')
