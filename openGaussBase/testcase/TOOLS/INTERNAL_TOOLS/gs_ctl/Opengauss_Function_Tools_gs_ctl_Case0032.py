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
Case Type   : 系统内部使用工具
Case Name   : gs_ctl restart指定-m的值为smart，重新启动时是否会报错
Description :
    1.查看集群状态是否正常
    2.restart启动主机
    3.查看集群状态主机是否正常
Expect      :
    1.查看集群状态正常成功
    2.restart失败
    3.查看集群状态主机状态为正常
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class LogicalReplication(unittest.TestCase):
    def setUp(self):
        LOG.info('----this is setup------')
        LOG.info(
            '---Opengauss_Function_Tools_gs_ctl_Case0032开始执行-----')
        self.constant = Constant()
        self.env_path = macro.DB_ENV_PATH
        self.instance_path = macro.DB_INSTANCE_PATH
        self.user_node = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('----查看集群状态-------')
        status = self.sh_primary.get_db_cluster_status()
        self.assertTrue(status)

        LOG.info('----重启数据库主机-------')
        excute_cmd = f'''
                source {self.env_path};
                gs_ctl restart -D {self.instance_path} -M primary -m smart ;
                    '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn(self.constant.UNRECOGNIZED_SHUTDOWN_MSG, msg)

        LOG.info('----查看集群状态-------')
        status = self.sh_primary.get_db_cluster_status()
        self.assertTrue(status)

    def tearDown(self):
        LOG.info('----this is tearDown------')
        LOG.info('----恢复集群状态------')
        is_start = self.sh_primary.start_db_cluster()
        LOG.info(is_start)
        LOG.info(
            '-----Opengauss_Function_Tools_gs_ctl_Case0032执行完成---')
