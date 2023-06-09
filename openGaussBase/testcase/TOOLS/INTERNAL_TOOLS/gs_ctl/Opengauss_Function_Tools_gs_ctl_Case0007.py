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
Case Name   : gs_ctl start指定-t的值过小，启动备机
Description :
    1.关闭正在运行的备机
    2.指定-t的值足够小启动备机
    3.查看集群状态
Expect      :
    1.关闭正在运行的备机成功
    2.指定-t的值足够小启动备机成功
    3.查看集群状态成功
History     :
"""

import unittest
import time

from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class LogicalReplication(unittest.TestCase):
    def setUp(self):
        LOG.info('----------------this is setup-----------------------')
        LOG.info(
            '---Opengauss_Function_Tools_gs_ctl_Case0007开始执行-----')
        self.constant = Constant()
        self.env_path = macro.DB_ENV_PATH
        self.instance_path = macro.DB_INSTANCE_PATH
        self.PrimaryNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info(
            '------------若为单机环境，后续不执行，直接通过------------')
        excute_cmd = f''' source {self.env_path}
                                  gs_om -t status --detail
                                 '''
        LOG.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        LOG.info(msg)
        if 'Standby' not in msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.user_node = Node('Standby1DbUser')

        LOG.info('---------关闭正在运行的备机------------')
        excute_cmd = f'''
                    source {self.env_path};
                    gs_ctl stop -D {self.instance_path} 
                '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn(self.constant.GS_CTL_STOP_SUCCESS_MSG, msg)

        LOG.info('----------------开启备机-------------------')
        excute_cmd = f'''
                    source {self.env_path};
                    gs_ctl start -D {self.instance_path} -M standby -t 1; 
                        '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn(self.constant.could_not_start_sever, msg)

        time.sleep(10)

        LOG.info('----------------查看集群状态-------------------')
        status = self.sh_primary.get_db_cluster_status()
        self.assertTrue(status)

    def tearDown(self):
        LOG.info('----------------this is tearDown-----------------------')
        excute_cmd = f''' source {self.env_path}
                                  gs_om -t status --detail
                                 '''
        LOG.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        LOG.info(msg)
        if 'Standby' not in msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.user_node = Node('Standby1DbUser')
        LOG.info('----------------开启备机-------------------')
        excute_cmd = f'''
                        source {self.env_path};
                        gs_ctl start -D {self.instance_path} -M standby; 
                    '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        LOG.info(
            '-----Opengauss_Function_Tools_gs_ctl_Case0007执行完成---')
