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
Case Type   : GUC
Case Name   : 修改指定数据库，用户，会话级别的参数session_timeout为其他数据类型
Description : 1、查看session_timeout默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c session_timeout
              2、在gsql中分别设置数据库、用户、会话、级别session_timeout；
              alter database postgres set session_timeout to 'test';
              alter user env109 set session_timeout to 'test';
              set session_timeout to 'test';
Expect      : 1、显示默认值；
              2、参数修改失败；
History     :
"""

import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

COMMONSH = CommonSH('PrimaryDbUser')


class GucTest(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Guc_Connectionauthentication_Case0159开始==')
        self.db_user_node = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        showcmd = '''source ''' + macro.DB_ENV_PATH \
                  + ''';gs_guc check -D ''' + macro.DB_INSTANCE_PATH \
                  + ''' -c session_timeout'''
        self.log.info(showcmd)
        check = self.db_user_node.sh(showcmd).result()
        self.log.info(check)
        self.assertIn('10min', check)
        self.log.info("设置session_timeout为其他数据类型，校验预期结果")
        sql_cmd = COMMONSH.execut_db_sql(
            f'''alter database postgres 
            set session_timeout to 'test';''')
        self.log.info(sql_cmd)
        self.assertIn("ERROR", sql_cmd)
        sql_cmd1 = COMMONSH.execut_db_sql(
            f'''alter user {self.db_user_node.db_user} 
            set session_timeout to 'test';''')
        self.log.info(sql_cmd1)
        self.assertIn("ERROR", sql_cmd1)
        sql_cmd2 = COMMONSH.execut_db_sql(
            f'''set session_timeout to 'test';''')
        self.log.info(sql_cmd2)
        self.assertIn("ERROR", sql_cmd2)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                        f"session_timeout=10min")
        self.log.info(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info('==Guc_Connectionauthentication_Case0159完成==')
