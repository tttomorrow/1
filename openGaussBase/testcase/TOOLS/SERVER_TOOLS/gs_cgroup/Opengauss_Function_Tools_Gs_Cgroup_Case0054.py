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
Case Name   : 修改Class组资源占用为!=[1,99]
Description :
    1.omm用户下执行gs_cgroup -u -T Class -t n 修改Class组资源占用为!=[1,99]
Expect      :
    1.修改失败
History     :
"""
import unittest
import random
import os
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)[:-3]}开始执行----')
        self.primary_node = Node('PrimaryDbUser')

    def test_gs_cgroup(self):
        text = '----step1:修改Class组资源占用为!=[1,99] expect:修改失败----'
        self.log.info(text)
        percent1 = random.randint(-65535, 0)
        percent2 = random.randint(100, 65535)
        percent_lis = [percent1, percent2]
        for percent in percent_lis:
            execute_cmd = f'source {macro.DB_ENV_PATH};' \
                          f'gs_cgroup --revert;' \
                          f'gs_cgroup -u -T Class -t {percent};' \
                          f'gs_cgroup -p'
            self.log.info(execute_cmd)
            msg = self.primary_node.sh(execute_cmd).result()
            self.log.info(msg)
            error_msg = 'ERROR: invalid value for top group dynamic ' \
                        'percentage. its range should be 1 ~ 99!'
            self.assertIn(error_msg, msg, '执行失败' + text)

    def tearDown(self):
        self.log.info('----No Need To Clean----')
        self.log.info(f'----{os.path.basename(__file__)[:-3]}执行完成----')
