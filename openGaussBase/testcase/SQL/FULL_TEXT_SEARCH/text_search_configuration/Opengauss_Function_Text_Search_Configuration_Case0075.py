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
Case Type   : 全文检索
Case Name   : 文本搜索配置语法中token_type（alnum）参数测试（解析器为pg_catalog.ngram）
Description :
    1.创建数据库编码为UTF8
    2.切换至test_db_075数据库,创建文本搜索配置;创建simple字典
    3.增加文本搜索配置字串类型映射，token为alnum
    4.使用文本检索函数对所创建的词典配置test_ngram进行测试
    5.删除文本搜索配置
    6.删除词典
    7.删除test_db_075数据库
Expect      :
    1.创建数据库成功
    2.创建文本搜索配置成功；创建simple字典成功
    3.增加文本搜索配置字串类型映射成功
    4.检索成功
    5.删除成功
    6.删除成功
    7.删除数据库成功
History     :
"""
import unittest
import time
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class FullTextSearch(unittest.TestCase):

    def setUp(self):
        logger.info("------------------------Opengauss_Function_Text_Search_Configuration_Case0075开始执行--------------------------")
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_dictionary(self):
        logger.info('-------------创建数据库----------------')
        sql_cmd1 = commonsh.execut_db_sql('''drop database if exists test_db_075;
                                           create database test_db_075 encoding 'utf8' template = template0;''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_DATABASE_SUCCESS, sql_cmd1)
        logger.info('-------------创建文本搜索配置和词典----------------')
        sql_cmd2 = '''drop text search configuration if exists test_ngram cascade;
                     create text search configuration test_ngram (parser=pg_catalog.ngram);
                      drop text search dictionary if exists pg_dict cascade;
                      create text search dictionary pg_dict (template = simple);'''
        excute_cmd1 = f'''
                                    source {self.DB_ENV_PATH};
                                    gsql -d test_db_075 -p {self.userNode.db_port} -c "{sql_cmd2}"
                                        '''
        logger.info(sql_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(constant.CREATE_TEXT_SEARCH_CONFIGURATION, msg1)
        self.assertIn(constant.CREATE_DICTIONARY_SUCCESS_MSG, msg1)
        logger.info('-------------修改文本搜索配置----------------')
        sql_cmd3 = '''alter text search configuration test_ngram add mapping for alnum with pg_dict;
                      select ts_debug('ngram','%a');
                      select to_tsvector('fat cats ate fat rats') @@ to_tsquery('c% & a%') as result;'''
        excute_cmd1 = f'''
                                  source {self.DB_ENV_PATH};
                                  gsql -d test_db_075 -p {self.userNode.db_port} -c "{sql_cmd3}"
                                  '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(constant.ALTER_TEXT_SEARCH_CONFIGURATION, msg1)
        flag = (constant.NGRAM_VALUES_ALNUM[0] in msg1 or constant.NGRAM_VALUES_ALNUM[1] in msg1)
        self.assertTrue(flag)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd4 = commonsh.execut_db_sql('''drop database test_db_075;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_Text_Search_Configuration_Case0075执行结束--------------------------')

