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
Case Type   : security-permission
Case Name   : 授予用户alter权限
Description :
    1.初始用户执行：create user wf with password '******';
            create table security_table(id1 int,id2 int, id3 int);
            grant alter on security_table to wf;
Expect      :
    1.CREATE ROLE
    CREATE TABLE
    GRANT
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
common = Common()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info(
            '----Opengauss_Function_Security_Permission_Case0012 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.constant = Constant()

    def test_default_permission(self):
        logger.info('-------create user || table-------')
        sql_cmd1 = f'create user wf with password \'{macro.COMMON_PASSWD}\';' \
                   f'create table security_table(id1 int,id2 int, id3 int);' \
                   f'grant alter on security_table to wf;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, msg1)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, msg1)
        self.assertIn(self.constant.GRANT_SUCCESS_MSG, msg1)

    def tearDown(self):
        sql_cmd1 = 'drop table security_table;' \
                   'drop user if exists wf cascade;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info(
            '----Opengauss_Function_Security_Permission_Case0012 finish----')
