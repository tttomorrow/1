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
Case Type   : 功能
Case Name   : 在事务中修改hash索引，未提交之前以及提交后观察事务隔离性是否正确
Description :
    1.创建表、插入数据；创建hash索引
    2.session1开启事务，修改hash索引，不提交并查询
    3.session1未提交前在session2中查询索引;待session1提交后，session2查询
    4.清理环境
Expect      :
    1.创建成功
    2.开启事务成功,修改索引成功，未提交session1查询索引已修改
    3.索引未修改;索引已修改
    4.清理环境完成
History     :
"""
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DmlTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_DML_Lock_Case0014开始')
        self.constant = Constant()
        self.commonsh1 = CommonSH('PrimaryDbUser')
        self.commonsh2 = CommonSH('PrimaryDbUser')
        self.tb_name = "t_hash_index_0014"
        self.id_name = "i_hash_index_0014"
        self.id_name_01 = "i_hash_index_0014_01"
        self.db_name = "db_hash_index_0014"

    def test_dml_lock(self):
        text = '-----step1:创建表并创建索引;expect:创建成功-----'
        self.log.info(text)
        sql_cmd = self.commonsh1.execut_db_sql(f'''
            drop table if exists {self.tb_name};
            create table {self.tb_name} (id int, num int, sex varchar 
            default 'male');
            insert into {self.tb_name} select random()*10, random()*3, 'XXX' \
            from generate_series(1,5000);
            drop index if exists {self.id_name};
            create index {self.id_name} on {self.tb_name} using hash (id);''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)

        text = 'step2:session1开启事务，修改hash索引，不提交并查询' \
               'expect:开启事务成功,修改索引成功，未提交session1查询索引已修改'
        self.log.info(text)
        sql = f'''begin;
            alter index {self.id_name} rename to {self.id_name_01};
            select relname from pg_class where  relname ='{self.id_name_01}';
            select pg_sleep(10);
            commit;'''
        thread_1 = ComThread(self.commonsh1.execut_db_sql, args=(sql, ''))
        thread_1.setDaemon(True)
        thread_1.start()
        time.sleep(3)

        text = 'step3:session1未提交前在session2中查询索引;待session1' \
               '提交后，session2查询;expect:索引名未修改;索引名已修改'
        self.log.info(text)
        sql = f'''select relname from pg_class where relname \
            ='{self.id_name_01}';
            select pg_sleep(15);
            select relname from pg_class where  relname \
            ='{self.id_name_01}';'''
        thread_2 = ComThread(self.commonsh2.execut_db_sql, args=(sql, ''))
        thread_2.setDaemon(True)
        thread_2.start()

        self.log.info('获取session1结果')
        thread_1.join(20)
        msg_result_1 = thread_1.get_result()
        self.log.info(msg_result_1)
        self.assertIn('BEGIN', msg_result_1, '执行失败:' + text)
        self.assertIn(f'{self.id_name_01}', msg_result_1, '执行失败:' + text)

        self.log.info('获取session2结果')
        thread_2.join(30)
        msg_result_2 = thread_2.get_result()
        self.log.info(msg_result_2)
        self.assertEqual('(0 rows)', msg_result_2.splitlines()[2].strip(),
                         '执行失败:' + text)
        self.assertEqual(f'{self.id_name_01}',
                         msg_result_2.splitlines()[-2].strip(),
                         '执行失败:' + text)

    def tearDown(self):
        self.log.info('--步骤4:清理环境--')
        sql_cmd = self.commonsh1.execut_db_sql(f'''drop table if exists \
            {self.tb_name};''')
        self.log.info(sql_cmd)
        self.log.info(
            '-Opengauss_Function_DDL_Hash_Index_Case0014finish--')
