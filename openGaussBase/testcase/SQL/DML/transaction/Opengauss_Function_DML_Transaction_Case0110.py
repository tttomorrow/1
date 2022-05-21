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
Case Type   : 事务控制
Case Name   : 使用普通用户开启事务，使用管理员回滚事务
Description :
    1.创建普通用户并赋予权限
    2.开启事务并执行事务
    3.使事务保存在磁盘上
    4.查看保存信息，信息保存在磁盘
    5.退出数据库连接
    6.重新连接数据库查看保存信息
    7.进行事务回滚
    8.查看保存信息
Expect      :
    1.创建普通用户并赋予权限成功
    2.开启事务并执行事务成功
    3.使事务保存在磁盘上成功
    4.查看保存信息，信息保存在磁盘成功
    5.退出数据库连接成功
    6.重新连接数据库查看保存信息成功
    7.进行事务回滚成功
    8.查看保存信息，磁盘上信息已回滚
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class TransactionFile(unittest.TestCase):
    def setUp(self):
        logger.info('--------------------Opengauss_Function_DML_Transaction_Case0110开始执行--------------------')
        self.PrimaryNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()
        self.macro = macro

    def test_transaction_file(self):
        logger.info('---------------------若为单机环境，后续不执行，直接通过--------------------')
        excute_cmd = f''' source {self.DB_ENV_PATH}
                       gs_om -t status --detail
                      '''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        if 'Standby' not in msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.StandbyNode = Node('Standby1DbUser')
            logger.info('------------------------新建普通用户并赋予权限--------------------')
            sql_cmd = f'''
                         drop user if exists zl cascade;
                         create user zl identified by '{macro.PASSWD_REPLACE}';
                         grant all privileges to zl;
                         '''
            excute_cmd = f'''
                                source {self.DB_ENV_PATH} ;
                                gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                                '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg)

            logger.info('------------------------使用普通用户开启事务并执行事务--------------------')
            sql_cmd = '''begin;
                         create table demo (a text,b integer);
                         prepare transaction 'the first prepare transaction';
                        '''
            excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -U zl -W '{macro.PASSWD_REPLACE}' -c "{sql_cmd}"
                        '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.PREPARED_TRANSACTION_MSG, msg)

            logger.info('---------------使用系统用户重新连接数据库查看保存信息,并进行事务回滚------------')
            sql_cmd = '''select * from pg_prepared_xacts;
                         rollback prepared 'the first prepare transaction';'''
            excute_cmd = f'''
                            source {self.DB_ENV_PATH} ;
                            gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                            '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn('the first prepare transaction', msg)
            self.assertIn(self.Constant.PREPARED_ROLLBACK_MSG, msg)

        logger.info('---------------------查看数据是否回滚----------------------')
        sql_cmd = f'''select * from pg_prepared_xacts;'''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn('the first prepare transaction', msg)

    def tearDown(self):
        logger.info('----------------清理环境-----------------------')
        sql_cmd = '''
                     drop user if exists zl cascade ;
                     commit;'''
        excute_cmd = f'''    
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, msg)
        logger.info('----------------------Opengauss_Function_DML_Transaction_Case0110执行完成--------------------')
