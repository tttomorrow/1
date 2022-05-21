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
Case Type   : GUC参数
Case Name   : 使用gs_guc set方法设置参数current_schema,观察预期结果
Description :
    1.查询search_path默认值
    2.创建模式
    3.修改参数值为自定义schema
    4.重启数据库
    5.show参数值
    6.恢复参数默认值
    7.重启数据库
    8.查询参数值
    9.清理环境
Expect      :
    1.参数默认值"$user",public
    2.创建模式成功
    3.修改参数值成功
    4.重启数据库成功
    5.参数值修改成功
    6.恢复参数默认值成功
    7.重启成功
    8.恢复默认值"$user",public
    9.清理环境完成
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Guc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_Guc_ClientConnection_Case0017开始')
        self.dbuser = Node('PrimaryDbUser')
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')
        self.sc_name = "sc_guc_0017"

    def test_current_schema(self):
        text = '--step1:查询参数默认值; expect:参数默认值"$user",public--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'show current_schema;')
        self.log.info(sql_cmd)
        default_value1 = sql_cmd.splitlines()[2].strip()
        self.log.info(default_value1)

        text = '--step2:创建模式; expect:创建模式成功--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'drop schema if exists '
                                              f'{self.sc_name} cascade;'
                                              f'create schema {self.sc_name};')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)

        text = '--step3:修改参数默认值为自定义模式;expect:修改成功--'
        self.log.info(text)
        mod_msg = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"search_path='{self.sc_name}'")
        self.log.info(mod_msg)
        self.assertTrue(mod_msg,  '执行失败:' + text)

        text = '--step4:重启数据库;expect:重启数据库成功--'
        self.log.info(text)
        restart_msg = self.commonsh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.commonsh.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step5:show参数值;expect:参数值修改成功--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'show search_path;')
        self.log.info(sql_cmd)
        self.assertIn(f'{self.sc_name}', sql_cmd, '执行失败:' + text)

        text = '--step6.恢复参数默认值;expect:参数默认值恢复成功--'
        self.log.info(text)
        restore_cmd = f"sed -i 's/{self.sc_name}/\"$user\",public/g'  " \
                      f"{macro.DB_INSTANCE_PATH}/postgresql.conf"
        self.log.info(restore_cmd)
        find_msg = self.dbuser.sh(restore_cmd).result()
        self.log.info(find_msg)
        text = '--step7:重启数据库;expect:数据库重启成功--'
        self.log.info(text)
        restart_msg = self.commonsh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.commonsh.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step8:show参数默认值;expect:参数值恢复成功--'
        sql_cmd = self.commonsh.execut_db_sql(f'show search_path;')
        self.log.info(sql_cmd)
        self.assertIn(default_value1, sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '--step9:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'drop schema {self.sc_name}'
                                              f' cascade; ')
        self.log.info(sql_cmd)
        self.log.info('Opengauss_Function_Guc_ClientConnection_Case0017结束')
