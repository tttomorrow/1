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
Case Type   : 功能测试
Case Name   : 使用gs_guc set方式设置参数enable_access_server_directory
Description :
    1. 检查默认值off,
    使用gs_guc set方式设置参数enable_access_server_directory为on并重启检查生效
    2. 使用gs_guc set方式恢复参数enable_access_server_directory为0ff并重启检查生效
Expect      : 
    1.默认值是off,设置成功
    2.设置成功，恢复为off
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.log.info('''Opengauss_Function_DDL_Create_Directory_Case0003开始''')

    def test_test_directory(self):

        def check_value():
            sql_cmd = '''show enable_access_server_directory;'''
            msg = self.commonsh.execut_db_sql(sql_cmd)
            self.log.info(msg)
            value = msg.splitlines()[-2].strip()
            return value

        def modify_para(para):
            cmd = f'''source {self.DB_ENV_PATH}; gs_guc set -N all -I all \
                    -c "enable_access_server_directory = '{para}'"'''
            self.log.info(cmd)
            msg1 = self.userNode.sh(cmd).result()
            self.log.info(msg1)
            self.assertIn('Success to perform gs_guc!', msg1)

        def restart():
            self.commonsh.restart_db_cluster()
            status = self.commonsh.get_db_cluster_status()
            self.assertTrue("Normal" in status or 'Degraded' in status)

        before = ['off', 'on']  # 默认是off
        after = ['on', 'off']
        flag = True  # 恢复的标志位
        try:
            for i in range(len(before)):
                self.assertTrue(check_value() == before[i])  # 查询参数值
                modify_para(after[i])  # gs_guc set方式修改参数值
                restart()  # 重启检查配置生效
                self.assertEqual(check_value(), after[i])
                if i == 1:  # 第二次循环执行到此即不用恢复了
                    flag = False
        finally:  # 判断是否需要恢复
            if flag:
                modify_para('off')
                restart()
                self.assertTrue(check_value() == 'off')

    def tearDown(self):
        self.log.info('Opengauss_Function_DDL_Create_Directory_Case0003执行结束')
