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
Case Name   : 修改参数track_counts为其他数据类型及超边界值，并校验其预期结果。
Description :
    1、查看track_counts默认值 期望：on；
    show track_counts;
    2、修改track_counts为123等，期望：合理报错
    gs_guc set -D {cluster/dn1} -c "track_counts=123";
    3、恢复默认值 无需恢复
Expect      :
    1、查看track_counts默认值 期望：on；
    2、修改track_counts为123等，期望：合理报错
    3、恢复默认值 无需恢复
History     :
"""

import sys
import unittest
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('PrimaryDbUser')

class Guctestcase(unittest.TestCase):
    def setUp(self):
        logger.info("------------------------Opengauss_Function_Guc_Run_Statistics_Case0004开始执行-----------------------------")
        self.Constant = Constant()

    def test_guc(self):
        logger.info("------------------------查询track_counts 期望：默认值on---------------------------")
        sql_cmd = commonsh.execut_db_sql('''show track_counts;''')
        logger.info(sql_cmd)
        self.assertEqual("on", sql_cmd.split("\n")[-2].strip())

        logger.info("-----------修改track_counts为123，期望：合理报错-------------")
        logger.info("-----------修改track_counts为123，期望：修改失败，show参数为默认值-------------")
        result = commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, "track_counts=123")
        self.assertFalse(result)
        sql_cmd = commonsh.execut_db_sql('''show track_counts;''')
        logger.info(sql_cmd)
        self.assertEqual("on", sql_cmd.split("\n")[-2].strip())

    def tearDown(self):
        logger.info("--------------------------------恢复默认值-----------------------------------")
        logger.info("恢复默认值")
        sql_cmd = commonsh.execut_db_sql('''show track_counts;''')
        if "on" not in sql_cmd:
            commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'track_counts=on')
            commonsh.restart_db_cluster()
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        logger.info("-------------------------Opengauss_Function_Guc_Run_Statistics_Case0004执行结束---------------------------")