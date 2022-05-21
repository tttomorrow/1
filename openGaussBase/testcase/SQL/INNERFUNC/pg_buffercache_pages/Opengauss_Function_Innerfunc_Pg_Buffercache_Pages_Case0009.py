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
Case Type   : pg_buffercache_pages验证
Case Name   : pg_buffercache_pages函数，表对象relblocknumber字段验证
Description :
    1、gsql连接数据库，创建表
    2、初始查询表的缓存信息
    3、表中插入不同量数据
    4、再次查询表的缓存信息
    5、环境清理
Expect      :
    1、gsql连接数据库，创建表成功
    2、初始查询表的缓存信息，为空（查询缓存数据为0行）;
    3、表中插入不同量数据成功
    4、再次查询表的缓存信息，reforknumber不同，relblocknumber字段不重复
    5、环境清理成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class PgBuffercachePagesCase0009(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0009:初始化')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.t_name1 = 't_pg_buffercache_pages_case0009_1'
        self.t_name2 = 't_pg_buffercache_pages_case0009_2'

    def test_main(self):
        step_txt = '----step1:连接数据库，创建表，expect: 创建成功----'
        self.log.info(step_txt)
        create_sql = f'drop table if exists {self.t_name1},{self.t_name2};' \
            f'create table {self.t_name1}(id int,content text);' \
            f'create table {self.t_name2}(id int,content text);'
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertTrue(create_result.count(self.constant.TABLE_CREATE_SUCCESS)
                        == 2, '执行失败:' + step_txt)

        step_txt = '----step2: 初始查询两张表的缓存信息，expect: 均为0行----'
        self.log.info(step_txt)
        select_sql = f"select count(*) from pg_buffercache_pages() where " \
            f"relfilenode in (select relfilenode from pg_class " \
            f"where relname in('{self.t_name1}','{self.t_name2}'));"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        tmp_count = int(select_result.strip().splitlines()[-2])
        self.assertEqual(tmp_count, 0, '执行失败：' + step_txt)

        step_txt = '----step3:两张表中插入不同量数据，expect: 插入成功----'
        self.log.info(step_txt)
        insert_sql = f"insert into {self.t_name1} " \
            f"values(generate_series(1, 1000), 'testtext');" \
            f"insert into {self.t_name2} " \
            f"values(generate_series(1, 10), 'testtext');"
        self.log.info(insert_sql)
        insert_result = self.pri_sh.execut_db_sql(insert_sql)
        self.log.info(insert_result)
        self.assertTrue(insert_result.count(self.constant.INSERT_SUCCESS_MSG)
                        == 2, '执行失败:' + step_txt)

        step_txt = f'----step4: 再次查询两张表的缓存信息，' \
            f'expect: reforknumber不同，relblocknumber字段不重复'
        self.log.info(step_txt)
        select_sql = f"select count(*) from (select 1 from " \
            f"pg_buffercache_pages() where relfilenode " \
            f"in (select relfilenode from pg_class " \
            f"where relname='{self.t_name1}') " \
            f"group by relforknumber,relblocknumber having count(*) >1);" \
            f"select count(*) from (select 1 from " \
            f"pg_buffercache_pages() where relfilenode " \
            f"in (select relfilenode from pg_class " \
            f"where relname='{self.t_name2}') " \
            f"group by relforknumber,relblocknumber having count(*) >1);"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        t_count1 = select_result.strip().splitlines()[2].strip()
        t_count2 = select_result.strip().splitlines()[7].strip()
        self.assertEqual(t_count1, '0', '执行失败，relblocknumber重复'
                         + step_txt)
        self.assertEqual(t_count2, '0', '执行失败，relblocknumber重复'
                         + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----step5: 环境清理，expect: 环境清理成功----'
        self.log.info(step_txt)
        drop_sql = f'drop table if exists {self.t_name1};' \
            f'drop table if exists {self.t_name2}; '
        self.log.info(drop_sql)
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)
        self.assertTrue(drop_result.count(self.constant.TABLE_DROP_SUCCESS)
                        == 2, '执行失败:' + step_txt)
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0009:执行完毕')
