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
Case Type   : 备机支持逻辑复制
Case Name   : 备机执行switchover后，备机执行逻辑复制
Description :
        1.备机上执行switchover，将备机升为主机
        2.修改参数wal_level为logical;enable_slot_log为on
        3.重启数据库
        4.主备机pg_hba.conf文件中配置逻辑复制的用户白名单
        5.主机创建逻辑复制槽
        6.主机上查询逻辑复制槽
        7.备机执行逻辑解码
        8.主机建表并执行DML操作
        9.查看指定解码文件
        10.清理环境
Expect      :
        1.备机升为主机成功
        2.修改参数wal_level为logical;enable_slot_log为on成功
        3.重启数据库成功，数据库状态正常
        4.pg_hba.conf 配置逻辑复制的用户白名单成功
        5.主机创建逻辑复制槽成功
        6.显示slot_test022复制槽信息
        7.解码命令执行成功，显示解码过程
        8.主机建表并执行DML操作成功
        9.解码文件解析DML操作成功
        10.清理环境完成
"""
import os
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_SH = CommonSH('PrimaryDbUser')
constant = Constant()


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')
class LogicalReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.Standby_SH = CommonSH('Standby1DbUser')
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.root_node = Node('PrimaryRoot')
        self.decode_file = os.path.join(macro.DB_INSTANCE_PATH,
                                        'logical22.txt')
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)

    def test_standby(self):
        self.log.info('--执行switchover--')
        excute_cmd = f'''source {macro.DB_ENV_PATH};
                    gs_ctl switchover -D {macro.DB_INSTANCE_PATH} -m fast ;
                    '''
        self.log.info(excute_cmd)
        excute_msg = self.standby_node.sh(excute_cmd).result()
        self.log.info(excute_msg)
        self.assertIn(constant.SWITCHOVER_SUCCESS_MSG, excute_msg)
        self.log.info('--进行refreshconf--')
        excute_cmd = f'''source {macro.DB_ENV_PATH};
                    gs_om -t refreshconf;
                    '''
        self.log.info(excute_cmd)
        excute_msg = self.standby_node.sh(excute_cmd).result()
        self.log.info(excute_msg)
        self.assertIn(constant.REFRESHCONF_SUCCESS_MSG, excute_msg)
        self.log.info('---重启数据库--')
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        self.log.info('---查看主备状态----')
        status_cmd = f'''source {macro.DB_ENV_PATH};
                    gs_om -t status --detail;
                    '''
        self.log.info(status_cmd)
        status_msg = self.primary_node.sh(status_cmd).result()
        self.log.info(status_msg)
        self.node_msg = status_msg.splitlines()[10].strip()
        self.log.info(self.node_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)
        self.assertIn('Standby', self.node_msg)
        self.log.info('--修改wal_level为logical;enable_slot_log为on--')
        mod_msg = self.Standby_SH.execute_gsguc('set',
                                                constant.GSGUC_SUCCESS_MSG,
                                                'wal_level =logical')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        mod_msg = self.Standby_SH.execute_gsguc('set',
                                                constant.GSGUC_SUCCESS_MSG,
                                                'enable_slot_log =on')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        self.log.info('--重启数据库--')
        restart_msg = self.Standby_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.Standby_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--主备均配置逻辑复制的用户--')
        sql_cmd = self.Standby_SH.execut_db_sql(f'''drop role if exists rep;
            create role rep with login password '{macro.COMMON_PASSWD}';
            alter role rep with replication sysadmin;''')
        self.log.info(sql_cmd)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)
        mod_msg = f"sed -i '$a\local    replication     rep      trust' " \
                  f"{self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host    replication     rep   127.0.0.1/32   " \
                  f"trust' {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host   replication     rep   ::1/128    " \
                  f"trust'  {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\local    replication     rep      trust' " \
                  f"{self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.standby_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host    replication     rep   127.0.0.1/32   " \
                  f"trust' {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.standby_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host    replication     rep   ::1/128  " \
                  f"trust' {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.standby_node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--备升主后创建逻辑复制槽--')
        check_res = self.Standby_SH.execut_db_sql('select slot_name from '
                                                  'pg_replication_slots;')
        self.log.info(check_res)
        if 'slot_test022' in check_res.split('\n')[-2].strip():
            del_cmd = self.Standby_SH.execut_db_sql("select * from "
                                                    "pg_drop_replication_slot"
                                                    "('slot_test022');")
            self.log.info(del_cmd)
        cre_cmd = self.Standby_SH.execut_db_sql("select * from "
                                                "pg_create_logical_"
                                                "replication_slot"
                                                "('slot_test022', "
                                                "'mppdb_decoding');")
        self.log.info(cre_cmd)
        self.log.info('--查询复制槽--')
        query_cmd = self.Standby_SH.execut_db_sql(
            'select slot_name,plugin from'
            ' pg_get_replication_slots();')
        self.log.info(query_cmd)
        self.assertIn('slot_test022', query_cmd)
        self.log.info('--备机创建解码文件--')
        touch_cmd = f'''touch {self.decode_file};'''
        self.log.info(touch_cmd)
        result = self.primary_node.sh(touch_cmd).result()
        self.log.info(result)
        self.assertNotIn(constant.SQL_WRONG_MSG[1], result)
        self.log.info('--备机执行逻辑复制槽流式解码--')
        decode_cmd = f"pg_recvlogical " \
                     f"-d {self.primary_node.db_name} " \
                     f"-S slot_test022 " \
                     f"-p {self.primary_node.db_port} " \
                     f"--start " \
                     f"-f {self.decode_file} " \
                     f"-s 2 " \
                     f"-v " \
                     f"-P mppdb_decoding " \
                     f"-U rep"
        execute_cmd = f'''source {macro.DB_ENV_PATH}
                          expect <<EOF
                          set timeout 300
                          spawn {decode_cmd}
                          expect "Password:"
                          send "{macro.COMMON_PASSWD}\\n"
                          expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        thread_2 = ComThread(self.primary_node.sh, args=(execute_cmd,))
        thread_2.setDaemon(True)
        thread_2.start()
        thread_2.join(10)
        msg_result_2 = thread_2.get_result()
        self.log.info(msg_result_2)
        self.log.info('创建表并进行DML操作')
        sql_cmd = self.Standby_SH.execut_db_sql('''drop table if exists 
        test022;
            create table test022(c_1 integer,
                    c_2 bigint,
                    c_3 smallint,
                    c_4 tinyint,
                    c_5 serial,
                    c_6 smallserial,
                    c_7 bigserial,
                    c_8 float,
                    c_9 double precision,
                    c_10 date,
                    c_11 time without time zone,
                    c_12 timestamp without time zone,
                    c_13 char(10),
                    c_14 varchar(20),
                    c_15 text,
                    c_16 blob,
                    c_17 bytea);
            insert into test022 values(1,10,5,25,default,default,default,\
            1237.127,123456.1234,date '12-10-2010','21:21:21','2010-12-12',\
            '测试','测试工程师','西安',empty_blob(),E'\\xDEADBEEF');
            update test022 set c_15 = '数据库';
            delete from test022 where c_16 = empty_blob();''')
        self.log.info(sql_cmd)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd)
        time.sleep(3)
        self.log.info('停止解码')
        stop_cmd = "ps -ef |  grep  pg_recvlogical | grep -v grep | " \
                   "awk '{{print $2}}' | xargs sudo kill -9"
        self.log.info(stop_cmd)
        result = self.root_node.sh(stop_cmd).result()
        self.log.info(result)
        time.sleep(3)
        self.log.info('备机查看解码文件')
        cat_cmd = f"cat {self.decode_file};"
        self.log.info(cat_cmd)
        result = self.primary_node.sh(cat_cmd).result()
        self.log.info(result)
        du_cmd = f"du -h {self.decode_file};"
        self.log.info(du_cmd)
        du_msg = self.primary_node.sh(du_cmd).result()
        self.log.info(du_msg)
        dumsg_list = du_msg.split()[0]
        self.log.info(dumsg_list)
        self.assertTrue(float(dumsg_list[:-1]) > 0)

        self.log.info('--主机删除复制槽--')
        del_cmd = self.Standby_SH.execut_db_sql("select * from "
                                                "pg_drop_replication_slot"
                                                "('slot_test022');")
        self.log.info(del_cmd)
        self.assertIn('', del_cmd)

    def tearDown(self):
        self.log.info('--步骤12:清理环境--')
        sql_cmd = self.Standby_SH.execut_db_sql('''drop role if exists rep;
                    drop table if exists test022;''')
        self.log.info(sql_cmd)
        del_msg = f"sed -i '/replication     rep/d' {self.pg_hba}"
        self.log.info(del_msg)
        msg = self.primary_node.sh(del_msg).result()
        self.log.info(msg)
        del_msg = f"sed -i '/replication     rep/d' {self.pg_hba}"
        self.log.info(del_msg)
        msg = self.standby_node.sh(del_msg).result()
        self.log.info(msg)
        rm_cmd = f"rm -rf {self.decode_file};"
        result = self.primary_node.sh(rm_cmd).result()
        self.log.info(result)
        restore_cmd = self.Standby_SH.execute_gsguc('set',
                                                    constant.GSGUC_SUCCESS_MSG,
                                                    'wal_level=hot_standby')
        self.log.info(restore_cmd)
        restore_cmd = self.Standby_SH.execute_gsguc('set',
                                                    constant.GSGUC_SUCCESS_MSG,
                                                    'enable_slot_log=off')
        self.log.info(restore_cmd)
        restart_msg = self.Standby_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        query_cmd = f'''source {macro.DB_ENV_PATH};
                   gs_om -t status --detail;
                   '''
        self.log.info(query_cmd)
        status_msg = self.primary_node.sh(query_cmd).result()
        self.log.info(status_msg)
        self.node_msg = status_msg.splitlines()[10].strip()
        self.log.info(self.node_msg)
        if 'Standby' in self.node_msg:
            self.log.info('--------------恢复主备状态--------------')
            recover_cmd = f'''source {macro.DB_ENV_PATH};
                             gs_ctl switchover -D {macro.DB_INSTANCE_PATH};
                             gs_om -t refreshconf;
                                    '''
            self.log.info(recover_cmd)
            recover_msg = self.primary_node.sh(recover_cmd).result()
            self.log.info(recover_msg)
        else:
            return '主备节点正常'
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
