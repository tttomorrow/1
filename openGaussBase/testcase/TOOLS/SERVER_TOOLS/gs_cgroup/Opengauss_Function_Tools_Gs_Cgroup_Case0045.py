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
Case Name   : 不设置QualificationTime单独设置CPUSkewPercent为0-100的uint型
Description :
    1.omm用户下执行gs_cgroup -c -S {classname} -G {grpname1}
    创建class及workload控制组
    2.omm用户下执行gs_cgroup -S {classname} -E "CPUSkewPercent={0-100}"
    单独设置CPUSkewPercent为0-100
    3.gs_cgroup --revert清理环境
Expect      :
    1.创建成功
    2.修改失败
    3.环境清理成功
History     :
"""
import unittest
import random
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Gs_Cgroup_Case0045开始执行----')
        self.primary_node = Node('PrimaryDbUser')
        self.Class_Name = 'Cgroup_Case0045_class'
        self.Grp_Name = 'Cgroup_Case0045_grp'

    def test_gs_cgroup(self):
        text = '----step1:创建class及workload控制组 expect:创建成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup --revert;' \
                      f'gs_cgroup -c -S {self.Class_Name} -G {self.Grp_Name};' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.Class_Name, msg, '执行失败' + text)
        self.assertIn(self.Grp_Name, msg, '执行失败' + text)

        text = '----step2:设置异常参数CPUSkewPercent为uint [0-100]，' \
               '不指定异常操作  expect:修改失败----'
        self.log.info(text)
        percent = random.randint(1, 99)
        percent_lis = [0, percent, 100]
        for percent in percent_lis:
            execute_cmd = f'source {macro.DB_ENV_PATH};' \
                          f'gs_cgroup -S {self.Class_Name} ' \
                          f'-E "CPUSkewPercent={percent}";' \
                          f'gs_cgroup -p'
            self.log.info(execute_cmd)
            msg = self.primary_node.sh(execute_cmd).result()
            self.log.info(msg)
            if percent == 0:
                check_msg = f'Type: EXCEPTION Class: {self.Class_Name}'
                self.assertNotIn(check_msg, msg, '执行失败' + text)
            else:
                error_msg = 'ERROR: exception key string \'CPUSkewPercent\' ' \
                            'is invalid, \'CPUSkewPercent\' must be ' \
                            'specified together with \'QualificationTime\'!'
                self.assertIn(error_msg, msg, '执行失败' + text)

    def tearDown(self):
        self.log.info('----step3:清理环境----')
        text = '----gs_cgroup --revert恢复cgroup配置 expect:恢复成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};'\
            f'gs_cgroup --revert'
        msg = self.primary_node.sh(execute_cmd).result()
        self.assertEqual('', msg, '执行失败' + text)
        self.log.info(
            '----Opengauss_Function_Gs_Cgroup_Case0045执行完成----')
