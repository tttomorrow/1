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
Case Type   : 智能运维snapshot模块
Case Name   : 创建快照后使用linear_regression算子创建model
Description :
    1.建表并插入数据
    2.创建快照
    3.创建训练集与测试集
    4.查看当前数据表快照
    5.查询创建的训练集数据
    6.使用linear_regression算子创建model
    7.查找系统表
    8.预测表数据
    9.清理环境
Expect      :
    1.建表并插入数据成功
    2.创建快照成功
    3.创建训练集与测试集成功
    4.返回当前数据表快照
    5.返回创建的训练集数据
    6.使用linear_regression算子创建model成功
    7.返回创建model的modelname
    8.返回预测的表数据
    9.清理环境成功
History     :
"""

import os
import unittest
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class AI(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Con = Constant()
        self.table = 't_snapshot_tab_0007'
        self.snapshot = 's_snapshot_s1@1.0'
        self.snapshot1 = 's_snapshot_s1_train@1.0'
        self.snapshot2 = 's_snapshot_s1_test@1.0'
        self.model = 'm_model_snapshot_0007'

    def test_ai_snapshot(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:建表并插入数据 expect:建表并插入数据成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(
            f'''drop table if exists {self.table};
            create table {self.table}(id int,tax int,bedroom int ,
            bath float,price int,size int,lot int );
            insert into {self.table} values(1,590,2,1,50000,770,22100),
            (2,1050,3,2 ,85000,1410,2000),(3,20 ,3,1,22500,1060,3500),
            (4,870,2,2,90000,1300,17500),(5,1320,3,2,133000,1500,30000),
            (6,1350,2,1,90500,820,25700),(7,2790,3,2.5,260000,2130,25000),
            (8,680,2,1,142500,1170,22000),(9,1840,3,2,160000,1500,19000),
            (10,3680,4,2,240000,2790,20000),(111,660,3,1,87000,1030,17500);''')
        self.logger.info(create_table)
        self.assertTrue(self.Con.TABLE_CREATE_SUCCESS in create_table
                        and self.Con.INSERT_SUCCESS_MSG in create_table,
                        "建表并插入数据失败" + step)

        step = 'step2:创建快照 expect:创建快照成功'
        self.logger.info(step)
        create_snapshot = self.primary_sh.execut_db_sql(
            f'''create snapshot {self.snapshot} as select * from {self.table};
            ''')
        self.logger.info(create_snapshot)
        self.assertIn(self.snapshot, create_snapshot, "执行失败" + step)

        step = 'step3:创建训练集与测试集 expect:创建训练集与测试集成功'
        self.logger.info(step)
        create_snapshot = self.primary_sh.execut_db_sql(
            f'''sample snapshot {self.snapshot} stratify by price 
            as _test at ratio .2, as _train at ratio .8 comment is 'training';
            ''')
        self.logger.info(create_snapshot)
        self.assertIn(self.snapshot1, create_snapshot, "执行失败" + step)
        self.assertIn(self.snapshot2, create_snapshot, "执行失败" + step)

        step = 'step4:查看当前数据表快照 expect:返回当前数据表快照'
        self.logger.info(step)
        select_snapshot = self.primary_sh.execut_db_sql(
            f'''select * from db4ai.snapshot;''')
        self.logger.info(select_snapshot)
        self.assertIn(self.snapshot, select_snapshot, "执行失败" + step)
        self.assertIn(self.snapshot1, select_snapshot, "执行失败" + step)
        self.assertIn(self.snapshot2, select_snapshot, "执行失败" + step)

        step = 'step5:查询创建的训练集数据 expect:返回创建的训练集数据'
        self.logger.info(step)
        select_snapshot = self.primary_sh.execut_db_sql(
            f'''select * from {self.snapshot1};''')
        self.logger.info(select_snapshot)
        self.assertNotIn('(0 rows)', select_snapshot, "执行失败" + step)

        step = 'step6:使用linear_regression算子创建model;' \
               'expect:使用linear_regression算子创建model成功'
        self.logger.info(step)
        create_model = self.primary_sh.execut_db_sql(
            f'''create model {self.model} using linear_regression features 
            1,tax,bath,size target price from {self.snapshot1};''')
        self.logger.info(create_model)
        self.assertIn('MODEL CREATED. PROCESSED 1', create_model,
                      "执行失败" + step)

        step = 'step7:查找系统表;expect:返回创建model的modelname'
        self.logger.info(step)
        select_model = self.primary_sh.execut_db_sql(
            f'''select modelname from gs_model_warehouse;''')
        self.logger.info(select_model)
        self.assertIn(self.model, select_model, "执行失败" + step)

        step = 'step8:预测表数据;expect:返回预测的表数据'
        self.logger.info(step)
        predict_data = self.primary_sh.execut_db_sql(
            f'''select predict by {self.model} (features 1,tax,bath,size) 
            from {self.snapshot1};''')
        self.logger.info(predict_data)
        self.assertNotIn('(0 rows)', predict_data, "执行失败" + step)

    def tearDown(self):
        step = 'step9:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(f'''
            purge snapshot {self.snapshot1};
            purge snapshot {self.snapshot2};
            purge snapshot {self.snapshot};
            drop table {self.table};
            drop model {self.model}''')
        self.logger.info(clean_environment)
        self.assertIn(self.Con.TABLE_DROP_SUCCESS, clean_environment,
                      "执行失败" + step)
        self.assertIn(f'{self.snapshot}', clean_environment,
                      "执行失败" + step)
        self.assertIn(self.snapshot1, clean_environment,
                      "执行失败" + step)
        self.assertIn(self.snapshot2, clean_environment,
                      "执行失败" + step)
        self.assertIn('DROP MODEL', clean_environment, "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
