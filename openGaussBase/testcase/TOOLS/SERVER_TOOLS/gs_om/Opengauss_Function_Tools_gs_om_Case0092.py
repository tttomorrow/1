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
Case Name   : 开启集群内kerberos认证时不指定是客户端还是服务端
Description :
    1.开启集群内安装kerberos认证时不指定是客户端还是服务端
    2.查看数据库状态：gs_om -t status
Expect      :
    1.开启失败
    2.数据库状态正常
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0092start--')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.logger.info('------开启集群内安装kerberos认证时不指定\
        是客户端还是服务端--------')
        check_cmd1 = f'''
        source {macro.DB_ENV_PATH}; 
        gs_om -t kerberos -m install -U {self.dbuser_node.ssh_user};'''
        self.logger.info(check_cmd1)
        msg1 = self.dbuser_node.sh(check_cmd1).result()
        self.logger.info(msg1)
        self.assertIn(self.constant.GS_TOOLS_ERROR_MSG1, msg1)

        self.logger.info('--------------查询数据库状态----------------')
        check_cmd2 = self.commonsh.get_db_cluster_status()
        self.logger.info(check_cmd2)
        self.assertTrue(check_cmd2)

    def tearDown(self):
        self.logger.info('--------------无需清理环境-------------------')
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0092finish--')
