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
Case Type   : 系统信息函数-模式可见性查询函数 
Case Name   : 使用函数pg_type_is_visible(type_oid) ，查看该类型（或域）是否在搜索路径中可见
Description :
    1.创建数据类型
    2.查看数据类型oid
    3.使用函数pg_type_is_visible(type_oid) ，查看该类型（或域）是否在搜索路径中可见
    4.删除数据类型
Expect      :
    1.创建数据类型成功
    2.查看数据类型oid成功
    3.使用函数pg_type_is_visible(type_oid) ，查看该类型（或域）是否在搜索路径中可见成功
    4.删除数据类型成功
History     :
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Functions(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0019开始-')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_info(self):
        LOG.info(f'-步骤1.创建数据类型')
        sql_cmd = self.commonsh.execut_db_sql(
            f'create type test_type AS (f1 int, f2 text);')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.CREATE_TYPE_SUCCESS_MSG, sql_cmd)

        LOG.info(f'-步骤2.查看数据类型oid')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select oid,typname from pg_type where typname =\'test_type\';')
        LOG.info(sql_cmd)
        self.assertIn('test_type', sql_cmd)
        oid = int(sql_cmd.split('\n')[2].split('|')[0])
        LOG.info(oid)
        if oid >= 0:
            LOG.info('查看临时模式的OID成功')
        else:
            raise Exception('查看异常，请检查')

        LOG.info(
            f'-步骤3.使用函数pg_type_is_visible(type_oid) ，'
            f'查看该类型（或域）是否在搜索路径中可见，返回为空')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select pg_type_is_visible({oid});')
        LOG.info(sql_cmd)
        self.assertIn('t', sql_cmd)
        sql_cmd = self.commonsh.execut_db_sql(
            f'select pg_type_is_visible(123);')
        LOG.info(sql_cmd)
        list1 = sql_cmd.split('\n')[2].split()
        LOG.info(list1)
        self.assertEqual(len(list1), 0)

        LOG.info(f'-步骤4.删除数据类型')
        sql_cmd = self.commonsh.execut_db_sql(
            f'drop type test_type;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.DROP_TYPE_SUCCESS_MSG, sql_cmd)

    def tearDown(self):
        LOG.info('-------无需清理环境-------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0019结束-')
