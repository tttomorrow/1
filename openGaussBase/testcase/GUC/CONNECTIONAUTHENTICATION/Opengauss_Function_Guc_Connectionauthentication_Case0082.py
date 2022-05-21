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
Case Name   : 修改指定数据库，用户，会话级别的参数unix_socket_directory
Description : 
              1、查看unix_socket_directory默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c unix_socket_directory
              2、使用数据库用户在有权限的目录下创建测试目录；
              mkdir -p /home/testdn/cluster/tmp
              3、在gsql中分别设置数据库、用户、会话、级别unix_socket_directory；
              alter database postgres
              set unix_socket_directory to '/home/testdn/cluster/tmp';
              alter user env109
              set unix_socket_directory to '/home/testdn/cluster/tmp';
              set unix_socket_directory to '/home/testdn/cluster/tmp';
Expect      : 
              1、显示默认值；
              2、创建成功；
              3、参数修改失败；
History     :
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

COMMONSH = CommonSH('PrimaryDbUser')


class GucTest(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Guc_Connectionauthentication_Case0082开始==')
        self.db_user_node = Node(node='PrimaryDbUser')
        self.newpath = os.path.join(macro.DB_INSTANCE_PATH, 'pathTemp')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_startdb(self):
        self.log.info("获取默认值")
        getcmd = f"source {macro.DB_ENV_PATH};" \
                 f"gsql -d {self.db_user_node.db_name} " \
                 f"-p {self.db_user_node.db_port} " \
                 f"-c \"show unix_socket_directory;\" | grep \/"
        self.log.info(getcmd)
        self.res11 = self.db_user_node.sh(getcmd).result()
        self.log.info(self.res11)

        self.log.info("使用数据库用户在有权限的目录下创建测试目录")
        sql_cmd = self.db_user_node.sh(f'''source {macro.DB_ENV_PATH};
        gs_ssh -c "rm -rf {self.newpath};
        mkdir {self.newpath};ls {self.newpath}"''').result()
        self.log.info(sql_cmd)
        self.assertIn(self.constant.gs_ssh_success_msg, sql_cmd)

        self.log.info("设置unix_socket_directory，校验预期结果")
        sql_cmd = COMMONSH.execut_db_sql(
            f'''alter database postgres 
            set unix_socket_directory to '{self.newpath}';''')
        self.log.info(sql_cmd)
        self.assertIn("ERROR", sql_cmd)

        sql_cmd1 = COMMONSH.execut_db_sql(
            f'''alter user {self.db_user_node.db_user} 
            set unix_socket_directory to '{self.newpath}';''')
        self.log.info(sql_cmd1)
        self.assertIn("ERROR", sql_cmd1)

        sql_cmd2 = COMMONSH.execut_db_sql(
            f'''set unix_socket_directory to '{self.newpath}';''')
        self.log.info(sql_cmd2)
        self.assertIn("ERROR", sql_cmd2)

        self.log.info("校验参数是否修改成功")
        result = COMMONSH.execute_gsguc('check', self.newpath,
                                       'unix_socket_directory')
        self.log.info(result)
        self.assertFalse(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'unix_socket_directory=\'{self.res11}\'')
        self.log.info(result)
        COMMONSH.restart_db_cluster()
        result = self.db_user_node.sh(f'''source {macro.DB_ENV_PATH};
        gs_ssh -c "rm -rf {self.newpath};
        ls {self.newpath}"''').result()
        self.log.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.assertIn(self.constant.NO_FILE_MSG, result)
        self.log.info('==Guc_Connectionauthentication_Case0082完成==')
