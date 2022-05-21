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
'''
--  Case Type:Cursor
--  testpoint:declare声明游标，游标名为有效参数，符合命名规范；
--  date:2020-11-03
'''

import unittest
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class CURSOR_TEST(unittest.TestCase):

    def setUp(self):
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.constant = Constant()

    def test_cursor_declare(self):
        logger.info("------------------Opengauss_Function_DDL_Cursor_Case0032开始执行-----------------")
        logger.info("======前置条件，创建表======")
        sql_cmd1 = f'''
                    drop table if exists cur_test_32;
                    create table cur_test_32(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
                    insert into cur_test_32 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                    (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                    (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');
                    '''
        msg1 = self.sh_primysh.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, msg1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg1)

        logger.info("======以字母开头======")
        sql_cmd2 = f'''
                    start transaction;
                    declare cursor1 cursor for select * from cur_test_32 order by 1;
                    fetch from cursor1;
                    close cursor1;
                    end;
                    '''
        msg2 = self.sh_primysh.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, msg2)
        self.assertIn(self.constant.DECLEAR_CURSOR_SUCCESS_MSG, msg2)
        self.assertIn('Allen', msg2)
        self.assertIn(self.constant.CLOSE_CURSOR_SUCCESS_MSG, msg2)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, msg2)

        logger.info("======以下划线开头======")
        sql_cmd3 = f'''                 
                    start transaction;
                    declare _curs1 cursor for select * from cur_test_32 order by 1;
                    fetch from _curs1;
                    close _curs1;
                    end;
                   '''
        msg3 = self.sh_primysh.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, msg3)
        self.assertIn(self.constant.DECLEAR_CURSOR_SUCCESS_MSG, msg3)
        self.assertIn('Allen', msg3)
        self.assertIn(self.constant.CLOSE_CURSOR_SUCCESS_MSG, msg3)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, msg3)

        logger.info("======字母数字符号混合======")
        sql_cmd4 = f''' 
                    start transaction;
                    declare cur#1 cursor for select * from cur_test_32 order by 1;
                    fetch from cur#1;
                    close cur#1;
                    end;
                    '''
        msg4 = self.sh_primysh.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, msg4)
        self.assertIn(self.constant.DECLEAR_CURSOR_SUCCESS_MSG, msg4)
        self.assertIn('Allen', msg4)
        self.assertIn(self.constant.CLOSE_CURSOR_SUCCESS_MSG, msg4)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, msg4)

    def tearDown(self):
        logger.info('======清理环境======')
        sql_cmd5 = f'''
                    drop table cur_test_32 cascade;
                   '''
        msg5 = self.sh_primysh.execut_db_sql(sql_cmd5)
        logger.info(msg5)
        logger.info('---------------Opengauss_Function_DDL_Cursor_Case0032执行结束---------------')





