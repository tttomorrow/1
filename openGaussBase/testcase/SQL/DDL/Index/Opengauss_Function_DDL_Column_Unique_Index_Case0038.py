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
Case Type   : 列存表支持主键、唯一索引
Case Name   : 执行vacuum后，再次插入数据
Description :
    1、创建普通列存表，指定主键约束;
    2、创建列存分区表，指定唯一约束
    3、两个表反复清除插入数据，数据唯一且非空值;
    4、普通列存表执行vacuum，列存分区表执行vacuum partition;
    5、两个表再次插入数据，数据唯一且非空;
    6、清理环境;
Expect      :
    1、创建普通列存表，指定主键约束成功;
    2、创建列存分区表，指定唯一约束成功;
    3、两个表插入数据均成功;
    4、执行vacuum成功，执行vacuum partition成功;
    5、再次插入数据成功;
    6、清理环境成功;
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant

logger = Logger()
primary_sh = CommonSH('PrimaryDbUser')


class DdlTestCase(unittest.TestCase):
    def setUp(self):
        self.constant = Constant()
        self.table = 'column_tab38'
        self.part_table = 'column_part_tab38'
        logger.info("======SetUp:检查数据库状态是否正常======")
        status = primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_column_unique_index(self):
        logger.info("Opengauss_Function_DDL_Column_Unique_Index_Case0038开始执行")
        logger.info("====步骤1:创建普通列存表，指定主键约束====")
        sql_cmd1 = f'''drop table if exists {self.table};
            create table {self.table}(id int primary key) 
            with(orientation=column);
            insert into {self.table} values(generate_series(1,10000));
            '''
        logger.info(sql_cmd1)
        sql_res1 = primary_sh.execut_db_sql(sql_cmd1)
        logger.info(sql_res1)
        self.assertTrue(self.constant.CREATE_TABLE_SUCCESS in sql_res1
                        and self.constant.INSERT_SUCCESS_MSG in sql_res1)

        logger.info("====步骤2:创建列存分区表，指定唯一约束====")
        sql_cmd2 = f'''drop table if exists {self.part_table};
            create table {self.part_table}(id int unique) 
            with(orientation=column)
            partition by range(id)
            (partition part_1 values less than(1000),
             partition part_2 values less than(5000),
             partition part_3 values less than(maxvalue));;
            insert into {self.part_table} values(generate_series(1,10000));
            '''
        logger.info(sql_cmd2)
        sql_res2 = primary_sh.execut_db_sql(sql_cmd2)
        logger.info(sql_res2)
        self.assertTrue(self.constant.CREATE_TABLE_SUCCESS in sql_res2
                        and self.constant.INSERT_SUCCESS_MSG in sql_res2)

        logger.info("======步骤3:反复插入数据，数据唯一且非空======")
        sql_cmd3 = f'''delete from {self.table};
            insert into {self.table} values(generate_series(1,10000));'''
        logger.info(sql_cmd3)

        for i in range(10):
            sql_res3 = primary_sh.execut_db_sql(sql_cmd3)
            logger.info(sql_res3)
            self.assertTrue(self.constant.INSERT_SUCCESS_MSG in sql_res3)

        sql_cmd4 = f'''delete from {self.part_table};
            insert into {self.part_table} values(generate_series(1,999));'''
        logger.info(sql_cmd4)

        for i in range(10):
            sql_res4 = primary_sh.execut_db_sql(sql_cmd4)
            logger.info(sql_res4)
            self.assertTrue(self.constant.INSERT_SUCCESS_MSG in sql_res4)

        logger.info("======步骤4:执行vacuum && vacuum partition======")
        sql_cmd5 = f'''vacuum {self.table};
            vacuum {self.part_table} partition(part_1);'''
        logger.info(sql_cmd5)
        sql_res5 = primary_sh.execut_db_sql(sql_cmd5)
        logger.info(sql_res5)
        self.assertIn(self.constant.VACUUM_SUCCESS_MSG, sql_res5)

        logger.info("======步骤5:再次插入数据======")
        sql_cmd6 = f'''delete from {self.table};
            delete from {self.part_table};
            insert into {self.table} values(generate_series(1,10000));
            insert into {self.part_table} values(generate_series(1,10000));
            '''
        logger.info(sql_cmd6)
        sql_res6 = primary_sh.execut_db_sql(sql_cmd6)
        logger.info(sql_res6)
        self.assertTrue(self.constant.INSERT_SUCCESS_MSG in sql_res6)

    def tearDown(self):
        logger.info("======步驟6:清理环境======")
        drop_cmd = f'''drop table {self.table} cascade;
            drop table {self.part_table} cascade;'''
        logger.info(drop_cmd)
        drop_res = primary_sh.execut_db_sql(drop_cmd)
        logger.info(drop_res)
        logger.info("Opengauss_Function_DDL_Column_Unique_Index_Case0038执行结束")
