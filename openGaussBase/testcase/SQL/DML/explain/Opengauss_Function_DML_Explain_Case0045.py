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
Case Type   : explain
Case Name   : explain使用参数plan,参数缺省值
Description :
    1.建表
    2.向表中插入数据
    3.explain使用参数plan,参数缺省值
    4.查询系统表plan_table数据
    5.清理环境
Expect      :
    1.建表成功
    2.向表中插入数据成功
    3.不打印执行信息,返回EXPLAIN SUCCESS
    4.表中有本次操作的信息
    5.清理环境成功
History     :
"""

import os
import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class SQL(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.table = 'explain_param_plan_0045'
        self.plan_table = 'plan_table'
        self.Constant = Constant()

    def test_explain(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:建表 expect:建表成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table};
            create table {self.table}(col1 int,col2 int);''')
        self.logger.info(create_table)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, create_table,
                      "建表失败" + step)

        step = 'step2:向表中插入数据 expect:向表中插入数据成功'
        self.logger.info(step)
        insert_data = self.primary_sh.execut_db_sql(f'''
            insert into {self.table} values(1,1),(2,2);''')
        self.logger.info(insert_data)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data,
                      "向表中插入数据失败" + step)

        step = 'step3:explain使用参数plan,参数缺省值' \
               'expect:不打印执行信息,返回EXPLAIN SUCCESS'
        self.logger.info(step)
        explain = self.primary_sh.execut_db_sql(f'''
            explain (plan) update {self.table} set col1 = 5;''')
        self.logger.info(explain)
        self.assertIn('EXPLAIN SUCCESS', explain, "打印信息不正确" + step)

        step = 'step4:查询系统表plan_table数据 expect:表中有本次操作的信息'
        self.logger.info(step)
        select_plan_table = self.primary_sh.execut_db_sql(f'''
            select * from  {self.plan_table};''')
        self.logger.info(select_plan_table)
        self.assertIn(' UPDATE', select_plan_table,
                      "explain使用plan参数执行结果不正确" + step)

    def tearDown(self):
        step = 'step5:清理环境 expect:清理环境成功'
        self.logger.info(step)
        de_table = self.primary_sh.execut_db_sql(f'''
            drop table {self.table};''')
        self.logger.info(de_table)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, de_table,
                      "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
