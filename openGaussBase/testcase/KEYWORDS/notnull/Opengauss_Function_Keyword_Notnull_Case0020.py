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
Case Type   : 关键字
Case Name   : opengauss关键字notnull(保留)，作为目录对象名（默认只允许初始化用户创建）
Description :
    1.统计所有节点命名空间中用户表的事务状态信息，以系统用户执行
    2.统计所有节点命名空间中用户表的事务状态信息，以非系统用户执行
Expect      :
    1.统计所有节点命名空间中用户表的事务状态信息，以系统用户执行
    2.统计所有节点命名空间中用户表的事务状态信息，以非系统用户执行，合理报错
History     :
"""
import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


class Keyword(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Keyword_Notnull_Case0020 开始执行---')
        self.commonsh = CommonSH('dbuser')
        self.constant = Constant()

    def test_keyword(self):
        self.log.info('---关键字作为目录对象名不带引号-合理报错---')
        sql_cmd = self.commonsh.execut_db_sql('''create directory \
            notnull as '/tmp/';drop directory notnull;''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG, sql_cmd)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG, sql_cmd)

        self.log.info("---关键字作为目录对象名带双引号-成功---")
        sql_cmd = self.commonsh.execut_db_sql('create directory \\\"natu'
                                              'ral\\\" as \'/tmp/\';'
                                              'drop directory \\\"natu'
                                              'ral\\\"; ')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.DROP_DIRECTORY_SUCCESS_MSG, sql_cmd)
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.DROP_DIRECTORY_SUCCESS_MSG, sql_cmd)

        self.log.info('---关键字作为目录对象名带单引号 - 合理报错---')
        sql_cmd = self.commonsh.execut_db_sql('drop directory '
                                             'if exists \'notnull\';')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG, sql_cmd)
        sql_cmd = self.commonsh.execut_db_sql(
            ''' create directory 'notnull' as '/tmp/';''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG, sql_cmd)

        self.log.info('---关键字作为目录对象名带反引号 - 合理报错---')
        sql_cmd = self.commonsh.execut_db_sql('drop directory '
                                             'if exists \`notnull\`;')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG, sql_cmd)
        sql_cmd = self.commonsh.execut_db_sql('''create directory `notnull`\
            as ' / tmp / ';''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG, sql_cmd)

    def tearDown(self):
        self.log.info('---Opengauss_Function_Keyword_Notnull_Case0020 执行结束---')
