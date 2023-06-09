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
Case Type   : 事务控制
Case Name   : 匿名块中的自定义函数名称为唯一存在的函数名称，匿名块提交后备机数据是否同步
Description :
    1.创建测试表与函数，且该函数的名称为唯一存在的函数名称
    2.在匿名块中调用该函数
    3.查看备机事务数据是否同步
Expect      :
    1.创建测试表与函数成功
    2.在匿名块中调用该函数成功
    3.备机事务数据同步成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
primary_sh = CommonSH('PrimaryDbUser')


class TransactionFile(unittest.TestCase):
    def setUp(self):
        logger.info('----Opengauss_Function_DML_Transaction_Case0033开始执行----')
        self.PrimaryNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()
        self.Common = Common()

    def test_transaction_file(self):
        logger.info('------若为单机环境，后续不执行，直接通过------')
        excute_cmd = f''' source {self.DB_ENV_PATH}
            gs_om -t status --detail'''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        if 'Standby' not in msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.StandbyNode = Node('Standby1DbUser')
            logger.info('------创建测试表与函数，且该函数的名称为唯一存在的函数名称------')
            vars = '\$$'
            sql_cmd = f'''drop table if exists testzl;
                create table testzl (sk integer,id char(16),\
                name varchar(20),sq_ft integer);
                create or replace function get_transaction(i integer) \
                returns integer as {vars}
                    begin
                        return i+1;
                    end;
                    {vars} language plpgsql; '''
            excute_cmd = f'''source {self.DB_ENV_PATH} ;
                gsql -d {self.PrimaryNode.db_name} \
                -p {self.PrimaryNode.db_port} \
                -c "{sql_cmd}"'''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.CREATE_FUNCTION_SUCCESS_MSG, msg)

            logger.info('------在匿名块中调用该函数------')
            sql_cmd = f'''
                BEGIN
                    insert into testzl values
                    (get_transaction(1),'rr','sk',11);
                END;'''
            excute_cmd = f'''source {self.DB_ENV_PATH} ;
                gsql -d {self.PrimaryNode.db_name} \
                -p {self.PrimaryNode.db_port} \
                -c "{sql_cmd}"'''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG,
                          msg)

            logger.info('----等待备机完成数据同步----')
            node_num = self.Common.get_node_num(self.PrimaryNode)
            logger.info(node_num)
            consistency_flag = primary_sh.check_location_consistency('primary',
                                                                     node_num,
                                                                     300)
            self.assertTrue(consistency_flag)

            logger.info('------查看备机数据------')
            sql_cmd = f'''select count(*) from testzl;'''
            excute_cmd = f'''source {self.DB_ENV_PATH} ;
                gsql -d {self.StandbyNode.db_name} \
                -p {self.StandbyNode.db_port} \
                -c "{sql_cmd}"'''
            logger.info(excute_cmd)
            msg = self.StandbyNode.sh(excute_cmd).result()
            logger.info(msg)
            res = msg.splitlines()[-2].strip()
            self.assertIn('1', res)

    def tearDown(self):
        logger.info('------清理环境------')
        sql_cmd = '''drop table if exists testzl;
            drop function if exists get_transaction(i integer);'''
        excute_cmd = f'''source {self.DB_ENV_PATH} ;
            gsql -d {self.PrimaryNode.db_name} \
            -p {self.PrimaryNode.db_port} \
            -c "{sql_cmd}"'''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        self.assertIn(self.Constant.DROP_FUNCTION_SUCCESS_MSG, msg)
        logger.info('----Opengauss_Function_DML_Transaction_Case0033执行完成----')
