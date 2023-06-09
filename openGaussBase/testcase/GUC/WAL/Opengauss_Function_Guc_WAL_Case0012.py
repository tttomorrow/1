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
Case Type   : GUC
Case Name   : 修改参数wal_sync_method，并校验其预期结果。
Description :
    1、查看wal_sync_method默认值；检查fsync确认为on;
    show wal_sync_method;
    show fsync;
    2、修改wal_sync_method分别为•open_datasync•fdatasync•fsync_writethrough•fsync•open_sync，校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "wal_sync_method=open_datasync";
    gs_guc set -D {cluster/dn1} -c "wal_sync_method=fsync_writethrough";
    gs_guc set -D {cluster/dn1} -c "wal_sync_method=fsync";
    gs_guc set -D {cluster/dn1} -c "wal_sync_method=open_sync";
    3、恢复默认值；
Expect      :
    1、显示默认值；
    3、恢复默认值；
History     :
"""

import sys
import unittest
from yat.test import macro
from yat.test import Node

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('PrimaryDbUser')


class Guctestcase(unittest.TestCase):
    def setUp(self):
        logger.info("------------------------Opengauss_Function_Guc_WAL_Case0012开始执行-----------------------------")
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()
        self.stopstartCmd = f'source {macro.DB_ENV_PATH};gs_om -t stop && gs_om -t start'
        self.statusCmd = f'source {macro.DB_ENV_PATH};gs_om -t status --detail'

    def test_common_user_permission(self):
        logger.info("------------------------查询wal_sync_method 期望：默认值fdatasync---------------------------")
        sql_cmd = commonsh.execut_db_sql(f'''show wal_sync_method;''')
        logger.info(sql_cmd)
        self.assertIn("fdatasync", sql_cmd)

        logger.info("-----------修改wal_sync_method分别为•open_datasync•fsync_writethrough•fsync•open_sync-------------")
        logger.info("-----------修改wal_sync_method为open_datasync，期望：重启生效-------------")
        sql_cmd = '''source ''' + self.DB_ENV_PATH + f''';gs_guc reload -D {self.DB_INSTANCE_PATH} -c "wal_sync_method=open_datasync"'''
        logger.info(sql_cmd)
        msg = self.userNode.sh(sql_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        sql_cmd = commonsh.execut_db_sql(f'''show wal_sync_method;''')
        logger.info(sql_cmd)
        self.assertIn("open_datasync", sql_cmd)
        logger.info("-----------修改wal_sync_method为fsync_writethrough，期望：设置失败-------------")
        sql_cmd = '''source ''' + self.DB_ENV_PATH + f''';gs_guc reload -D {self.DB_INSTANCE_PATH} -c "wal_sync_method=fsync_writethrough"'''
        logger.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql(f'''show wal_sync_method;''')
        logger.info(sql_cmd)
        self.assertNotIn("fsync_writethrough", sql_cmd)
        logger.info("-----------修改wal_sync_method为open_datasync，期望：重启生效-------------")
        sql_cmd = '''source ''' + self.DB_ENV_PATH + f''';gs_guc reload -D {self.DB_INSTANCE_PATH} -c "wal_sync_method=fsync"'''
        logger.info(sql_cmd)
        msg = self.userNode.sh(sql_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        sql_cmd = commonsh.execut_db_sql(f'''show wal_sync_method;''')
        logger.info(sql_cmd)
        self.assertIn("fsync", sql_cmd)
        logger.info("-----------修改wal_sync_method为open_datasync，期望：重启生效-------------")
        sql_cmd = '''source ''' + self.DB_ENV_PATH + f''';gs_guc reload -D {self.DB_INSTANCE_PATH} -c "wal_sync_method=open_sync"'''
        logger.info(sql_cmd)
        msg = self.userNode.sh(sql_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        sql_cmd = commonsh.execut_db_sql(f'''show wal_sync_method;''')
        logger.info(sql_cmd)
        self.assertIn("open_sync", sql_cmd)

        logger.info("--------------------------------恢复默认值-----------------------------------")
        result = commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'wal_sync_method=fdatasync')
        self.assertTrue(result)
        commonsh.restart_db_cluster()
        is_started = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

    def tearDown(self):
        logger.info("--------------------------------恢复默认值-----------------------------------")
        commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'wal_sync_method=fdatasync')
        commonsh.restart_db_cluster()
        is_started = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        logger.info("-------------------------Opengauss_Function_Guc_WAL_Case0012执行结束---------------------------")