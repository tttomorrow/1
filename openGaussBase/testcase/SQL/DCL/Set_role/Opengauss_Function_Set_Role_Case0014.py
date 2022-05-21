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
Case Type   : 功能测试
Case Name   : 在事务中加session设置
Description :
    1.使用初始用户连gsql，创建用户，给用户赋权为sysadmin，期望:创建赋权成功
    2.使用role14_001连接gsql，查看当前会话用户，当前用户。期望:SESSION_USER, CURRENT_USER均为role14_001
    3.使用role14_001连接gsql，执行set role语句，加session 期望:CURRENT_USER为role14_002
    4.查询表的属主 期望:table_set_role14_001和table_set_role14_001属主均为role14_002
    5.使用初始用户连gsql，清理环境。期望:删除用户成功
Expect      :
History     :
"""


import sys
import unittest
from yat.test import macro
from yat.test import Node
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_Set_Role_Case0014开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_common_user_permission(self):
        logger.info('------------------------创建用户，给用户赋权为sysadmin，期望:创建赋权成功-----------------------------')
        sql_cmd = commonsh.execut_db_sql(f'''
                                        drop table if exists table_set_role14_001;
                                        drop table if exists table_set_role14_002;
                                        drop role if exists role14_001;
                                        drop role if exists role14_002;
                                        create role role14_001 password '{macro.COMMON_PASSWD}';
                                        create role role14_002 password '{macro.COMMON_PASSWD}';
                                        alter role role14_001 with login;
                                        alter role role14_002 with login;
                                        grant all privileges to  role14_001;
                                        grant all privileges to  role14_002;
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)

        logger.info('-----------使用role14_001连接gsql，查看当前会话用户，当前用户。期望:SESSION_USER, CURRENT_USER均为role14_001-------------')
        sql_cmd = ('''
                    SELECT SESSION_USER, CURRENT_USER;
                    ''')
        excute_cmd = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role14_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                            '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("role14_001", msg)
        
        logger.info('-----------使用role14_001连接gsql，执行set role语句，加session 期望:CURRENT_USER为role14_002-------------')
        sql_cmd = (f'''
                    START TRANSACTION;
                        SET session ROLE role14_002 password '{macro.COMMON_PASSWD}';
                        drop table if exists table_set_role14_001;
                        create table table_set_role14_001(id int);
                    end;
                    
                    SELECT SESSION_USER, CURRENT_USER;
                    drop table if exists table_set_role14_002;
                    create table table_set_role14_002(id int);
                    ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role14_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("role14_001", msg)

        logger.info('----------查询表的属主 期望:table_set_role14_001和table_set_role14_001属主均为role14_002---------')
        sql_cmd = ('''
                    select tableowner from pg_tables where tablename ='table_set_role14_001';
                    select tableowner from pg_tables where tablename ='table_set_role14_002';
                    ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role14_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn("role14_001", msg)
        self.assertIn("role14_002", msg)

    def tearDown(self):
        logger.info('---------------------------------清理环境。期望:删除用户成功-----------------------------------')
        sql_cmd = commonsh.execut_db_sql('''
                                        drop table if exists table_set_role14_001;
                                        drop table if exists table_set_role14_002;
                                        drop role if exists role14_001;
                                        drop role if exists role14_002;
                                        ''')
        logger.info(sql_cmd)
        logger.info('-------------------------Opengauss_Function_Set_Role_Case0014执行结束---------------------------')
