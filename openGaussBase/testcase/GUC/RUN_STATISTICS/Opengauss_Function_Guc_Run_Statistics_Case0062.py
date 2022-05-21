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
Case Name   : 普通用户方式三修改参数track_thread_wait_status_interval为60,合理报错不生效
Description :
    步骤1:查询track_thread_wait_status_interval默认值
    show track_thread_wait_status_interval;
    步骤2:创建用户guser
    create user guser password {password};
    步骤3:普通用户guser方式三修改track_thread_wait_status_interval为60，校验其预期结果
    alter database testdb set track_thread_wait_status_interval to 60;
    show track_thread_wait_status_interval;
    步骤4:做简单DML
    步骤5:恢复默认值,清理环境
    alter database testdb set track_thread_wait_status_interval to 30;
    drop user guser;
Expect      :
    步骤1:显示默认值30min
    步骤2:创建用户成功
    步骤3:参数设置失败合理报错，校验修改后参数值为30min
    步骤4:DML无报错
    步骤5:恢复默认值成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class GucTestCase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0062开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.user_node = Node("PrimaryDbUser")
        self.db_name = "testdb"
        self.param = "track_thread_wait_status_interval"

    def test_guc(self):
        LOGGER.info("步骤1:查询track_thread_wait_status_interval默认值 期望：默认值30min")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.param};")
        LOGGER.info(sql_cmd)
        self.assertEqual("30min", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2:创建用户guser")
        sql_cmd = COMMONSH.execut_db_sql(f'''drop user if exists guser;\
            create user guser password '{macro.COMMON_PASSWD}';\
            drop database if exists {self.db_name};\
            create database {self.db_name};\
            ''')
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd)

        LOGGER.info("步骤3:普通用户方式三修改参数{self.param}为60")
        sql_cmd = (f"alter database {self.db_name} set {self.param} to 60;")
        excute_cmd = f'''source {macro.DB_ENV_PATH};\
            gsql \
            -d {self.db_name} \
            -U guser \
            -p {self.user_node.db_port} \
            -W {macro.COMMON_PASSWD} \
            -c "{sql_cmd}"\
            '''
        LOGGER.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOGGER.info(msg)
        self.assertIn(self.constant.PERMISSION_DENIED, msg)

        sql_cmd = (f"show {self.param};")
        excute_cmd = f'''source {macro.DB_ENV_PATH};\
            gsql \
            -d {self.db_name} \
            -U guser \
            -p {self.user_node.db_port} \
            -W {macro.COMMON_PASSWD} \
            -c "{sql_cmd}"\
            '''
        LOGGER.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOGGER.info(msg)
        self.assertIn("30min\n", msg)

        LOGGER.info("步骤4:恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql(f"drop database {self.db_name};")
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, sql_cmd)
        sql_cmd = COMMONSH.execut_db_sql(f"drop user guser cascade;")
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, sql_cmd)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        COMMONSH.execut_db_sql(f"drop user if exists guser;")
        COMMONSH.execut_db_sql(f"drop database if exists {self.db_name};")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.param};")
        if "30min" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f"{self.param}='30min'")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0062执行结束==")
