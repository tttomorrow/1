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
Case Name   : 不支持-t加schema_name.table_name的导入格式
Description :
    1.连接数据库并创建数据
    2.创建数据
    3.导出tat格式的文件：
    4.查看导出的数据是否正确
    5.导入之前导出的数据：以-t加schema_name.table_name的格式导入
    6.清理环境：
Expect      :
    1.连接成功
    2.成功创建数据
    3.导出数据
    4.查看导出的数据正确
    5.导入失败：提示还原操作完成，但是数据未导入
    6.清理环境结束
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
        LOG.info('----Opengauss_Function_Tools_gs_restore_Case0052start----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        LOG.info('------------------1.连接数据库并创建数据库-----------------')
        sql_cmd1 = '''drop database if exists testdump;
            create database testdump;
            '''
        excute_cmd1 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name}\
            -p {self.dbuser_node.db_port}\
            -c "{sql_cmd1}";
            '''
        LOG.info(excute_cmd1)
        msg1 = self.dbuser_node.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, msg1)

        LOG.info('---------2.创建数据----------')
        LOG.info('---------在创建好的数据库中创建数据----------')
        sql_cmd2 = '''drop table if exists test1;
            drop table if exists test2;
            drop table if exists test3;
            drop table if exists test4;
            create table test1 (id int ,name char(10));
            insert into test1 values (1,'aa'),(2,'bb');
            create table test2 (id  int,name char(20));
            insert into test2 values(1,'xixi'),(2,'haha'),(3,'hehe');
            create table test3(id  int,name char(20));
            insert into test3 values(33,'xiao'),(296,'bai'),(783,'cai');
            create table test4(id  int,name char(20));
            insert into test4 values(7,'yang'),(29886,'bai'),(9,'lao');
            drop schema if exists schema1;
            drop schema if exists schema2;
            drop schema if exists schema3;
            create schema schema1;
            create schema schema2;
            create schema schema3;
            alter table test1 set schema schema1;
            alter table test2 set schema schema2;
            alter table test3 set schema schema3;
            select * from schema1.test1;
            '''
        excute_cmd2 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d testdump\
            -p {self.dbuser_node.db_port}\
            -c "{sql_cmd2}"
            '''
        LOG.info(excute_cmd2)
        msg2 = self.dbuser_node.sh(excute_cmd2).result()
        LOG.info(msg2)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg2)
        self.assertIn(self.constant.ALTER_TABLE_MSG, msg2)
        self.assertIn('2 rows', msg2)

        LOG.info('-------3.导出文本格式的文件--------')
        dump_cmd = f'''source {macro.DB_ENV_PATH} ;
            gs_dump -p {self.dbuser_node.db_port}\
            testdump --format=t\
            -f {macro.DB_INSTANCE_PATH}/dump52.tar;
            '''
        LOG.info(dump_cmd)
        dump_msg = self.dbuser_node.sh(dump_cmd).result()
        LOG.info(dump_msg)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, dump_msg)

        LOG.info('-------4.校验导出的数据--------')
        du_cmd = f'''du -h {macro.DB_INSTANCE_PATH}/dump52.tar;'''
        du_msg = self.dbuser_node.sh(du_cmd).result()
        LOG.info(du_msg)
        dumsg_list = du_msg.split()[0]
        self.assertTrue(float(dumsg_list[:-1]) > 0)

        LOG.info('-------5.以-t加schema_name.table_name的格式导入--------')
        restore_cmd = f'''source {macro.DB_ENV_PATH};
            gs_restore -p {self.dbuser_node.db_port}\
            -d testdump\
            {macro.DB_INSTANCE_PATH}/dump52.tar\
            -t schema1.test1;
            '''
        LOG.info(restore_cmd)
        restore_msg = self.dbuser_node.sh(restore_cmd).result()
        LOG.info(restore_msg)
        self.assertIn('restore operation successful', restore_msg)
        LOG.info('----------------验证是否成功导入数据-----------------')
        sql_cmd3 = '''select * from  schema1.test1; '''
        excute_cmd3 = f'''source {macro.DB_ENV_PATH};
            gsql -d testdump\
            -p {self.dbuser_node.db_port}\
            -c "{sql_cmd3}";
            '''
        LOG.info(excute_cmd3)
        msg3 = self.dbuser_node.sh(excute_cmd3).result()
        LOG.info(msg3)
        self.assertIn('2 rows', msg3)

    def tearDown(self):
        LOG.info('-----------------6.清理环境：删除数据库-----------------')
        sql_cmd5 = '''drop database if exists testdump; '''
        excute_cmd5 = f'''source {macro.DB_ENV_PATH};
            gsql -d {self.dbuser_node.db_name}\
            -p {self.dbuser_node.db_port} -c "{sql_cmd5}";
            rm -rf {macro.DB_INSTANCE_PATH}/dump52.tar;
            '''
        LOG.info(excute_cmd5)
        msg5 = self.dbuser_node.sh(excute_cmd5).result()
        LOG.info(msg5)
        LOG.info('----Opengauss_Function_Tools_gs_restore_Case0052finish----')
