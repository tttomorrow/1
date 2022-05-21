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
Case Name   : gs_cgroup --revert 恢复控制组为初始状态
Description :
    1.omm用户下执行gs_cgroup -c -S {classname} -G {grpname}  创建控制组
    2.omm用户下执行gs_cgroup --revert恢复控制组为初始状态
Expect      :
    1.创建成功
    2.恢复成功
History     :
"""
import unittest

from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Gs_Cgroup_Case0002开始执行----')
        self.primary_node = Node('PrimaryDbUser')
        self.Class_Name = 'Gs_Cgroup_Case0002_class'
        self.Grp_Name = 'Gs_Cgroup_Case0002_grp'

    def test_gs_cgroup(self):
        text_1 = '----step1:创建控制组 expect:创建成功----'
        self.log.info(text_1)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup --revert;' \
            f'gs_cgroup -c -S {self.Class_Name} -G {self.Grp_Name};' \
            f'gs_cgroup -p'
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.Class_Name, msg, '执行失败' + text_1)
        self.assertIn(self.Grp_Name, msg, '执行失败' + text_1)

        text_2 = '----step2:恢复控制组状态 expect:恢复成功----'
        self.log.info(text_2)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup --revert;' \
                      f'gs_cgroup -p'
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        self.assertNotIn(self.Class_Name, msg, '执行失败' + text_2)
        self.assertNotIn(self.Grp_Name, msg, '执行失败' + text_2)

    def tearDown(self):
        self.log.info('----No Need To Clean----')
        self.log.info(
            '----Opengauss_Function_Gs_Cgroup_Case0002执行完成----')
