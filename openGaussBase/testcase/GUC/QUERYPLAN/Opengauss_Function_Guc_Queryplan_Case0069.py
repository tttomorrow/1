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
Case Name   : 使用gs_guc set方法设置参数geqo_generations为200,观察预期结果
Description :
        1.查询geqo_generations默认值
        2.修改参数值为200并重启数据库
        3.查询该参数修改后的值
        4.恢复参数默认值
Expect      :
        1.显示默认值为0
        2.修改成功
        3.显示200
        4.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class QueryPlan(unittest.TestCase):

    def setUp(self):
        self.constant = Constant()
        LOG.info(
            '------Opengauss_Function_Guc_Queryplan_Case0069start-----')

    def test_geqo_generations(self):
        LOG.info('--步骤一：查看默认值--')
        sql_cmd = commonsh.execut_db_sql('''show geqo_generations;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤二：gs_guc set设置geqo_generations为200并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'geqo_generations =200')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤三：查询该参数修改后的值--')
        sql_cmd = commonsh.execut_db_sql('''show geqo_generations;''')
        LOG.info(sql_cmd)
        self.assertEqual('200', sql_cmd.split('\n')[2].strip())

    def tearDown(self):
        LOG.info('--步骤四：恢复默认值--')
        sql_cmd = commonsh.execut_db_sql('''show geqo_generations;''')
        LOG.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"geqo_generations={self.res}")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show geqo_generations;''')
        LOG.info(sql_cmd)
        LOG.info(
            '-------Opengauss_Function_Guc_Queryplan_Case0069执行完成-----')
