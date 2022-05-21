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
Case Name   : explain使用参数detail,参数默认值为True
Description :
    1.建表
    2.向表中插入数据
    3.explain使用参数detail,参数默认值为True
    4.清理环境
Expect      :
    1.建表成功
    2.向表中插入数据成功
    3.报错提示参数无效
    4.清理环境成功
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
        self.table = 'explain_param_detail_0053'
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

        step = 'step3:explain使用参数detail,参数默认值为True' \
               'expect:报错提示参数无效'
        self.logger.info(step)
        explain = self.primary_sh.execut_db_sql(f'''
            explain (detail True) update {self.table} set col1 = 5;''')
        self.logger.info(explain)
        self.assertIn('ERROR:  unrecognized EXPLAIN option "detail"',
                      explain, "打印信息不正确" + step)

    def tearDown(self):
        step = 'step4:清理环境 expect:清理环境成功'
        self.logger.info(step)
        de_table = self.primary_sh.execut_db_sql(f'''
            drop table {self.table};''')
        self.logger.info(de_table)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, de_table,
                      "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
