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
Case Name   : 逻辑复制pg_recvlogical 行为参数指定多个 --create --start，
              创建启动复制流成功
Description :
        1.修改参数wal_level为logical;enable_slot_log为on
        2.主机pg_hba.conf文件中配置逻辑复制的用户白名单
        3.逻辑复制pg_recvlogical 行为参数指定多个 --create --start
        4.删除复制槽
        5.清理环境
Expect      :
        1.修改参数wal_level为logical;enable_slot_log为on成功
        2.pg_hba.conf 配置逻辑复制的用户白名单成功
        3.创建逻辑复制槽成功，启动流复制
        4.删除复制槽成功
        5.清理环境完成
History     :
"""
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Tools_pg_recvlogical_Case0014 start-')
        self.constant = Constant()
        self.common = Common()
        self.primary_node = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.default_value1 = self.common.show_param('wal_level')
        self.default_value2 = self.common.show_param('enable_slot_log')
        self.u_name = 'u_pg_recvlogical_0014'
        self.slot_name = 'solt_pg_recvlogical_case0014'

    def test_standby(self):
        text = '----step1:修改wal_level为logical;enable_slot_log为on;' \
               'expect: 修改成功----'
        self.log.info(text)
        mod_msg = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'wal_level =logical')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        mod_msg = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'enable_slot_log =on')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        self.assertTrue(restart_msg, '执行失败:' + text)

        text = '----step2:主机配置逻辑复制的用户;expect:配置成功----'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f"drop user if exists "
                                            f"{self.u_name};"
                                            f"create user {self.u_name} "
                                            f"replication password "
                                            f"'{macro.COMMON_PASSWD}';")
        self.log.info(sql_cmd)

        guc_cmd = f'source {macro.DB_ENV_PATH}; ' \
                  f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
                  f'-h "host  replication  {self.u_name}  ' \
                  f'{self.primary_node.db_host}/32  sha256"'
        self.log.info(guc_cmd)
        guc_res = self.primary_node.sh(guc_cmd).result()
        self.log.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res,
                      '执行失败：' + text)

        text = '--step3:逻辑复制pg_recvlogical 行为参数指定多个 --create ' \
               '--start;expect:成功--'
        self.log.info(text)
        create_cmd = f"pg_recvlogical " \
                     f"-d {self.primary_node.db_name} " \
                     f"-U {self.u_name} " \
                     f"-h {self.primary_node.db_host} " \
                     f"-S {self.slot_name} " \
                     f"-p {str(int(self.primary_node.db_port)+1)} " \
                     f"--create --start " \
                     f"-W " \
                     f"-v -f - -s 2 -n "
        execute_cmd = f'''source {macro.DB_ENV_PATH}
                   expect <<EOF
                   set timeout 30
                   spawn {create_cmd}
                   expect "Password:"
                   send "{macro.COMMON_PASSWD}\\n"
                   expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        exec_msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(exec_msg)
        self.assertIn(f'initializing replication slot "{self.slot_name}"',
                      exec_msg, '执行失败：' + text)
        self.assertIn('confirming write up to', exec_msg, '执行失败：' + text)

        text = '--step4:删除复制槽;expect:成功--'
        self.log.info(text)
        del_cmd = f"pg_recvlogical " \
                  f"-d {self.primary_node.db_name} " \
                  f"-U {self.u_name} " \
                  f"-h {self.primary_node.db_host} " \
                  f"-S {self.slot_name} " \
                  f"-p {self.primary_node.db_port} " \
                  f" --drop " \
                  f"-v "
        self.log.info(del_cmd)
        execute_cmd = f'''source {macro.DB_ENV_PATH}
                          expect <<EOF
                          set timeout 300
                          spawn {del_cmd}
                          expect "Password:"
                          send "{macro.COMMON_PASSWD}\\n"
                          expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        exec_msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(exec_msg)
        self.assertIn(f'freeing replication slot "{self.slot_name}"', exec_msg,
                      '执行失败：' + text)

    def tearDown(self):
        text = '--step4:清理环境;expect:清理环境完成--'
        self.log.info(text)
        self.log.info('--删除用户--')
        drop_cmd = self.pri_sh.execut_db_sql(f"drop user {self.u_name};")
        self.log.info(drop_cmd)

        self.log.info('----主机pg_hba.conf文件恢复----')
        guc_cmd = f'source {macro.DB_ENV_PATH}; ' \
                  f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
                  f'-h "host  replication  {self.u_name}  ' \
                  f'{self.primary_node.db_host}/32"'
        self.log.info(guc_cmd)
        guc_res = self.primary_node.sh(guc_cmd).result()
        self.log.info(guc_res)

        self.log.info('--修改参数wal_level为logical;enable_slot_log为on--')
        res_cmd1 = self.pri_sh.execute_gsguc('set',
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             f'wal_level='
                                             f'{self.default_value1}')
        self.log.info(res_cmd1)
        res_cmd2 = self.pri_sh.execute_gsguc('set',
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             f'enable_slot_log='
                                             f'{self.default_value2}')
        self.log.info(res_cmd2)
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('----断言tearDown执行成功----')
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, drop_cmd,
                      '执行失败:' + text)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res,
                      '执行失败：' + text)
        self.assertTrue(res_cmd1, '执行失败:' + text)
        self.assertTrue(res_cmd2, '执行失败:' + text)
        self.assertTrue(restart_msg, '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Tools_pg_recvlogical_Case0014 finish--')
