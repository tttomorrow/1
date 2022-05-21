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
Case Type   : DDL_Drop_Directory
Case Name   : enable_access_server_directory=on时，有gs_role_directory_drop权限
              的非初始用户删除目录对象
Description :
    1.创建目录
    2.修改guc参数enable_access_server_directory=on
    3.初始用户创建目录对象，创建用户并赋予gs_role_directory_drop权限
    4.有gs_role_directory_drop权限的非初始用户删除目录对象
    5.删除用户，删除目录
    6.恢复参数
Expect      :
    1.创建目录成功
    2.修改guc参数成功
    3.创建成功，赋权成功
    4.删除成功
    5.删除成功
    6.恢复参数成功
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common


class DropDirectory(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f"-----{os.path.basename(__file__)} start-----")
        self.userNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.dir_name = 'dir_object_drop_directory_0006'
        self.dir_path = os.path.join('/tmp', 'dir_drop_directory_0006')
        self.guc_result = ''
        self.user_name = 'u_object_drop_directory_0006'

        text = '-----step1:创建目录,expect:创建目录成功-----'
        self.logger.info(text)
        mkdir_cmd = f"mkdir {self.dir_path} && ls -ld {self.dir_path}"
        self.logger.info(mkdir_cmd)
        mkdir_msg = self.userNode.sh(mkdir_cmd).result()
        self.logger.info(mkdir_msg)
        check_dir_cmd = f'''if [ -d {self.dir_path} ]; 
                    then echo "exists"; 
                    else echo "not exists"; fi'''
        self.logger.info(check_dir_cmd)
        mkdir_result = self.userNode.sh(check_dir_cmd).result()
        self.logger.info(mkdir_result)
        self.assertEquals("exists", mkdir_result, '执行失败' + text)

        text = '-----step2:修改guc参数enable_access_server_directory=on;' \
               'expect:修改guc参数成功-----'
        self.logger.info(text)
        self.config_directory = 'enable_access_server_directory'
        self.check_default = self.common.show_param(self.config_directory)
        if 'on' != self.check_default:
            result = self.sh_primary.execute_gsguc(
                'reload', self.constant.GSGUC_SUCCESS_MSG,
                f'{self.config_directory}=on')
            self.assertTrue(result, '执行失败' + text)
        show_msg = self.common.show_param(self.config_directory)
        self.assertEquals(show_msg, 'on', '执行失败' + text)

    def test_drop_directory(self):
        text = "-----step3:初始用户创建目录对象，创建用户并赋予" \
               "gs_role_directory_drop权限，expect:创建成功，赋权成功-----"
        self.logger.info(text)
        create_cmd = f"create or replace directory {self.dir_name} " \
            f"as '{self.dir_path}';" \
            f"drop user if exists {self.user_name};" \
            f"create user {self.user_name} with " \
            f"password '{macro.COMMON_PASSWD}';" \
            f"grant gs_role_directory_drop to {self.user_name};"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG and
                      self.constant.DROP_ROLE_SUCCESS_MSG and
                      self.constant.CREATE_ROLE_SUCCESS_MSG and
                      self.constant.GRANT_SUCCESS_MSG,
                      create_msg, '执行失败' + text)
        sql_cmd = f"select * from pg_directory " \
            f"where dirname like '{self.dir_name}';"
        sql_msg = self.sh_primary.execut_db_sql(sql_cmd)
        self.logger.info(sql_msg)
        self.assertIn(self.dir_name and '10' and self.dir_path,
                      sql_msg, '执行失败' + text)

        text = "-----step4:有gs_role_directory_drop权限的非初始用户" \
               "删除目录对象，expect:删除成功-----"
        self.logger.info(text)
        drop_cmd = f"drop directory {self.dir_name};"
        drop_msg = self.sh_primary.execut_db_sql(
            drop_cmd,
            sql_type=f"-U {self.user_name} -W '{macro.COMMON_PASSWD}'")
        self.logger.info(drop_msg)
        self.assertIn(self.constant.DROP_DIRECTORY_SUCCESS_MSG,
                      drop_msg, '执行失败' + text)

    def tearDown(self):
        text_5 = "-----step5:删除用户，删除目录，expect:删除成功-----"
        self.logger.info(text_5)
        drop_cmd = f"drop user {self.user_name};"
        drop_msg = self.sh_primary.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        del_cmd = f"rm -rf {self.dir_path}"
        self.logger.info(del_cmd)
        del_msg = self.userNode.sh(del_cmd).result()
        self.logger.info(del_msg)
        check_dir_cmd = f'''if [ -d {self.dir_path} ]; 
                            then echo "exists"; 
                            else echo "not exists"; fi'''
        self.logger.info(check_dir_cmd)
        del_result = self.userNode.sh(check_dir_cmd).result()
        self.logger.info(del_result)

        text_6 = "-----step6:恢复参数;expect:恢复参数成功-----"
        self.logger.info(text_6)
        current = self.common.show_param(self.config_directory)
        if self.check_default != current:
            self.guc_result = self.sh_primary.execute_gsguc(
                'reload', self.constant.GSGUC_SUCCESS_MSG,
                f'{self.config_directory}={self.check_default}')
        show_msg = self.common.show_param(self.config_directory)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG,
                      drop_msg, '执行失败' + text_5)
        self.assertEquals("not exists", del_result, '执行失败' + text_5)
        self.assertTrue(self.guc_result, '执行失败' + text_6)
        self.assertEquals(show_msg, self.check_default, '执行失败' + text_6)
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")