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
Case Name   : 转储全局对象时不转出表空间
Description :
    1.连接数据库：
    2.创建数据
    3.退出数据库
    4.source环境变量
    5.转储全局对象时不转出表空间
    6.连接数据库，清理环境
Expect      :
    1.数据库连接成功
    2.创建数据成功
    3.退出数据库
    4.source环境变量
    5.导出成功
    6.清理环境成功
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
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Casestart----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        LOG.info('------------创建数据-------------')
        sql_cmd1 = '''drop table if exists test1; 
            create table test1 (id int ,name char(10));
            insert into test1 values (1,'aa'),(2,'bb');
            drop role if exists manager; 
            create role manager identified by 'qwer@123';
            drop tablespace if exists tbspace;
            create tablespace tbspace relative location 'tbspace_qm/tbspace';
            '''
        gsql_cmd1 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} -p\
            {self.dbuser_node.db_port} -c "{sql_cmd1}"
            '''
        LOG.info(gsql_cmd1)
        sql_msg1 = self.dbuser_node.sh(gsql_cmd1).result()
        LOG.info(sql_msg1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_msg1)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, sql_msg1)
        LOG.info('--转储全局对象时不转出表空间--')
        dumpall_cmd = f'source {macro.DB_ENV_PATH} ;' \
            f'gs_dumpall ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'-g ' \
            f'--no-tablespaces ' \
            f'-f {macro.DB_INSTANCE_PATH}/dumpall.sql;'
        LOG.info(dumpall_cmd)
        dumpall_msg = self.dbuser_node.sh(dumpall_cmd).result()
        LOG.info(dumpall_msg)
        self.assertIn(self.constant.gs_dumpall_success_msg, dumpall_msg)
        cat_cmd = f'cat {macro.DB_INSTANCE_PATH}/dumpall.sql;'
        LOG.info(cat_cmd)
        cat_msg = self.dbuser_node.sh(cat_cmd).result()
        LOG.info(cat_msg)
        self.assertIn('CREATE ROLE manager', cat_msg)

    def tearDown(self):
        LOG.info('---清理环境---')
        sql_cmd2 = '''drop table test1;
            drop role if exists manager;
            drop tablespace tbspace;
            '''
        clear_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name}\
            -p {self.dbuser_node.db_port} -c "{sql_cmd2}";
            rm -rf {macro.DB_INSTANCE_PATH}/dumpall.sql;
            rm -rf {macro.DB_INSTANCE_PATH}/pg_location/tbspace_qm;
            '''
        LOG.info(clear_cmd)
        clear_msg = self.dbuser_node.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Case0089finish----')
