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
Case Type   : 拷贝数据
Case Name   : 表字段数多于文件表数据字段数时，多余字段数据是否插入缺省值
Description :
    1.创建测试表并插入数据
    2.构造数据文件(少字段表)
    3.查看数据文件
    4.从文件中拷贝数据到表（多字段表）
    5.进行校验
    6.清理环境
Expect      :
    1.创建测试表并插入数据成功
    2.构造数据文件成功
    3.查看数据文件成功
    4.从文件中拷贝数据到表成功
    5.进行校验成功，多余字段插入缺省值
    6.清理环境成功
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class CopyFile(unittest.TestCase):
    def setUp(self):
        logger.info('----------------------------Opengauss_Function_DML_Copy_Case0014开始执行-----------------------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_copy_file(self):
        logger.info('----------------------------创建测试表并插入数据-----------------------------')
        sql_cmd = '''drop table if exists testzl;
                    CREATE TABLE testzl(SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER default 55);
                    insert into testzl values (001,'sk1','tt',3332);
                    insert into testzl values (001,'sk1','tt',3332);
                    insert into testzl values (001,'sk1','tt',3332);
                    drop table if exists testcopy;
                    CREATE TABLE testcopy(a INTEGER,b CHAR(16),c VARCHAR(20));
                    insert into testcopy values (001,'sk1','tt');
                    insert into testcopy values (001,'sk1','tt');
                    insert into testcopy values (001,'sk1','tt');
                    '''
        excute_cmd = f'''
                    source {self.DB_ENV_PATH} ;
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, msg)

        logger.info('----------------------------构造数据文件-----------------------------')
        sql_cmd = f'''copy testcopy to '{self.DB_INSTANCE_PATH}/pg_copydir/testzl.dat';
                        '''
        excute_cmd = f'''mkdir {self.DB_INSTANCE_PATH}/pg_copydir;
                        touch {self.DB_INSTANCE_PATH}/pg_copydir/testzl.dat;
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('----------------------------查看数据文件-----------------------------')
        excute_cmd = f'''
                        cat {self.DB_INSTANCE_PATH}/pg_copydir/testzl.dat;
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)

        logger.info('--------------------------从文件中拷贝数据到表---------------------------')
        sql_cmd = f'''copy testzl("SK","ID","NAME") from '{self.DB_INSTANCE_PATH}/pg_copydir/testzl.dat';
                      select * from testzl;'''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('---------------------------进行校验---------------------------')
        sql_cmd = f'''select count(*) from testzl ;'''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        res = msg.splitlines()[-2].strip()
        self.assertIn('6', res)
        logger.info(res)

    def tearDown(self):
        logger.info('----------------------------清理环境-----------------------------')
        sql_cmd = '''
                    drop table if exists testcopy;
                    drop table if exists testzl;'''
        excute_cmd = f'''
                        rm -rf {self.DB_INSTANCE_PATH}/pg_copydir
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info('------------------Opengauss_Function_DML_Copy_Case0014执行完成-----------------------------')
