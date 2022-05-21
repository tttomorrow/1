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
Case Type   : 工具-GS_BASEBACKUP
Case Name   : 不自定义表空间，默认参数进行本地备份
Description :
    1.创建备份目录
    2.创建测试表
    create table testzl(a int);
    3.执行备份
    gs_basebackup -D /opt/openGauss_lu1208/bak -Fp
        -Xstream -p 18333 -l gauss_8.bak -U sysadmin -W
    4.停止数据库
    gs_ctl stop -D /opt/openGauss_lu1208/cluster/dn1
    5.使用备份目录启动数据库
    gs_ctl start -D /opt/openGauss_lu1208/bak -M primary
    6.查询数据库状态确认是否启动成功
    gs_ctl query -D /opt/openGauss_lu1208/bak
    7.查询测试表是否存在
    select * from testzl;
Expect      :
    1.创建备份目录成功
    2.创建测试表成功
    3.备份提示成功，备份目录下生成备份文件
    4.停止成功
    5.使用备份目录启动数据库成功
    6.查询数据库状态，数据库启动成功
    7.测试表存在，数据与备份前一致
History     :
"""

import os
import time
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '需主备环境，若为单机环境则不执行')
class GsBaseBackUpCase7(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.Primary_Root_Node = Node('PrimaryRoot')
        self.LOG = Logger()
        self.Constant = Constant()

        self.T_NAME = 't_basebackup_7'
        self.backup_bak_path = os.path.join(macro.DB_BACKUP_PATH,
                                            'gs_basebackup')
        self.gs_basebackup_bak_name = 'gs_basebackup_Case0007.bak'
        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0007 start----')

        text = '----获取主机hostname值----'
        self.LOG.info(text)
        self.host_name = self.Primary_User_Node.sh(
            'hostname').result().strip()

    def test_server_tools(self):
        text = '----step1: 创建备份目录 expect: 成功----'
        self.LOG.info(text)
        is_dir_exists_cmd = f'''if [ ! -d "{self.backup_bak_path}" ]
                                then
                                    mkdir -p {self.backup_bak_path}
                                fi'''
        result = self.Primary_User_Node.sh(is_dir_exists_cmd).result()
        self.LOG.info(result)
        self.assertEqual(result, '', '执行失败:' + text)

        text = '----step1.1: 修改备份目录权限700，以免权限有误 expect: 成功----'
        self.LOG.info(text)
        chmod_cmd = f"chmod 700 -R {self.backup_bak_path}"
        self.LOG.info(chmod_cmd)
        chmod_msg = self.Primary_Root_Node.sh(chmod_cmd).result()
        self.LOG.info(chmod_msg)
        self.assertEqual(chmod_msg, '', '执行失败:' + text)

        text = '----step1.2: 查看备份目录 expect: 成功----'
        self.LOG.info(text)
        ls_cmd = f"ls -l {os.path.dirname(self.backup_bak_path)}"
        self.LOG.info(ls_cmd)
        ls_msg = self.Primary_User_Node.sh(ls_cmd).result()
        self.LOG.info(ls_msg)

        text = '----step2: 创建测试表 expect: 成功----'
        self.LOG.info(text)
        sql_cmd = f"drop table if exists {self.T_NAME}; " \
            f"create table {self.T_NAME}(a int); " \
            f"insert into  {self.T_NAME} select generate_series(1,1000);"
        self.LOG.info(sql_cmd)
        sql_result = Primary_SH.execut_db_sql(sql_cmd)
        self.LOG.info(sql_result)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS,
                      sql_result,
                      '执行失败:' + text)

        text = '----step3: 执行备份 expect: 成功----'
        self.LOG.info(text)
        gs_basebackup_cmd = f"gs_basebackup " \
            f"-D {self.backup_bak_path} " \
            f"-Fp " \
            f"-Xstream " \
            f"-p {self.Primary_User_Node.db_port} " \
            f"-l {self.gs_basebackup_bak_name} " \
            f"-U {self.Primary_User_Node.ssh_user} " \
            f"-W "

        backup_cmd = f'''source {macro.DB_ENV_PATH}
            expect <<EOF
            set timeout 1200
            spawn {gs_basebackup_cmd}
            expect {{{{
                "*assword:" {{{{ send "{self.Primary_User_Node.ssh_password}\
                \\n";exp_continue }}}}
                "{self.Constant.gs_basebackup_success_msg}" \
                {{{{ send_user "执行成功\\n" }}}}
            }}}}
            expect eof\n''' + "EOF"
        self.LOG.info(backup_cmd)
        backup_msg = self.Primary_User_Node.sh(backup_cmd).result()
        self.LOG.info(backup_msg)
        self.assertIn("执行成功", backup_msg, '执行失败:' + text)

        text = '----step4: 停止数据库 expect: 成功----'
        self.LOG.info(text)
        is_stopped = Primary_SH.execute_gsctl(
            'stop', self.Constant.GS_CTL_STOP_SUCCESS_MSG)
        self.assertTrue(is_stopped, '执行失败:' + text)

        time.sleep(5)

        text = '----step5: 修改参数data_directory expect: 成功----'
        self.LOG.info(text)
        msg = Primary_SH.execute_gsguc(
            command='set',
            assert_flag=self.Constant.GSGUC_SUCCESS_MSG,
            param=f"data_directory='{self.backup_bak_path}'",
            node_name=self.host_name,
            dn_path=self.backup_bak_path)
        self.assertTrue(msg, '执行失败:' + text)

        text = '----step5.1: 使用备份目录启动数据库 expect: 成功----'
        self.LOG.info(text)
        start_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_ctl start -D {self.backup_bak_path} -M primary"
        self.LOG.info(start_cmd)
        start_msg = self.Primary_User_Node.sh(start_cmd).result()
        self.LOG.info(start_msg)
        self.assertIn(self.Constant.RESTART_SUCCESS_MSG,
                      start_msg,
                      '执行失败:' + text)

        text = '----step5.2: 重建备机需主备连接正常 expect: 成功----'
        self.LOG.info(text)
        result = Primary_SH.wait_cluster_connected(self.backup_bak_path)
        self.assertTrue(result, '执行失败:' + text)

        text = '----step5.3: 重建备机 expect: 成功----'
        self.LOG.info(text)
        build_msg_list = Primary_SH.get_standby_and_build()
        for msg in build_msg_list:
            self.assertIn(self.Constant.BUILD_SUCCESS_MSG,
                          msg,
                          '执行失败:' + text)

        text = '----step6: 查询数据库状态确认是否启动成功 expect: 成功----'
        self.LOG.info(text)
        query_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_ctl query -D {self.backup_bak_path}"
        self.LOG.info(query_cmd)
        query_msg = self.Primary_User_Node.sh(query_cmd).result()
        self.LOG.info(query_msg)
        self.assertIn('db_state', query_msg, '执行失败:' + text)
        for arg in query_msg.splitlines():
            if 'db_state' in arg:
                self.assertIn('Normal', arg, '执行失败:' + text)

        text = '----step7: 查询测试表是否存在 expect: 成功----'
        self.LOG.info(text)
        sql_cmd = f"select * from {self.T_NAME};"
        self.LOG.info(sql_cmd)
        sql_msg = Primary_SH.execut_db_sql(sql_cmd)
        self.LOG.info(sql_msg)
        self.assertIn('1000 rows', sql_msg, '执行失败:' + text)

    def tearDown(self):
        self.LOG.info('----step8: run_teardown expect: 成功----')
        self.LOG.info('----停止数据库----')
        stop_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_ctl stop -D {self.backup_bak_path}"
        self.LOG.info(stop_cmd)
        stop_msg = self.Primary_User_Node.sh(stop_cmd).result()
        self.LOG.info(stop_msg)

        self.LOG.info('----修改参数data_directory----')
        msg = Primary_SH.execute_gsguc(
            command='set',
            assert_flag=self.Constant.GSGUC_SUCCESS_MSG,
            param=f"data_directory='{macro.DB_INSTANCE_PATH}'")
        self.LOG.info(msg)

        self.LOG.info('----使用原目录启动数据库----')
        start_flag = Primary_SH.execute_gsctl(
            'start',
            self.Constant.RESTART_SUCCESS_MSG,
            '-M primary')
        self.LOG.info(start_flag)

        self.LOG.info('----重建备机需主备连接正常----')
        result = Primary_SH.wait_cluster_connected()
        self.LOG.info(result)

        self.LOG.info('----重建备机----')
        build_msg_list = Primary_SH.get_standby_and_build()
        self.LOG.info(build_msg_list)

        self.LOG.info('----删除测试表----')
        sql_cmd = f"drop table if exists {self.T_NAME}"
        self.LOG.info(sql_cmd)
        sql_msg = Primary_SH.execut_db_sql(sql_cmd)
        self.LOG.info(sql_msg)

        self.LOG.info('----删除备份文件----')
        is_dir_exists_cmd = f'''rm -rf {self.backup_bak_path}'''
        result = self.Primary_User_Node.sh(is_dir_exists_cmd).result()
        self.LOG.info(result)

        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0007 end----')
