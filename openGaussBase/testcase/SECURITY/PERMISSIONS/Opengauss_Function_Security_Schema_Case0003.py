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
Case Type   : security-schema
Case Name   : 普通用户授予数据库的CREATE权限创建Schema
Description :
    1.初始用户执行：create user wf with password '******';
                create database wfdb;
                GRANT CREATE ON DATABASE wfdb TO wf;
    2.wf用户执行：CREATE SCHEMA schema01;
Expect      :
    1.CREATE SCHEMA1.CREATE ROLE
    2.PERMISSION DENIED
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('----------------Opengauss_Function_Security_Schema_Case0003 start-----------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_schema(self):
        logger.info('----------------------------create user || table-----------------------------')
        sql_cmd1 = f'''create user wf with password '{macro.COMMON_PASSWD}';
                    create database wfdb;
                    GRANT CREATE ON DATABASE wfdb TO wf;
                    '''
        sql_cmd2 = '''CREATE SCHEMA schema01;'''
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"
                    '''
        # 登录自定义数据库
        excute_cmd2 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d wfdb -p {self.userNode.db_port} -U  wf -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                    '''
        logger.info(excute_cmd1)
        logger.info(excute_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, msg1)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.assertIn(self.Constant.CREATE_SCHEMA_SUCCESS_MSG, msg2)

    def tearDown(self):
        sql_cmd1 = '''drop database wfdb;
                    drop user if exists wf cascade;
                    '''
        excute_cmd1 = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"'''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        logger.info('-------------Opengauss_Function_Security_Schema_Case0003 finish------------------')
