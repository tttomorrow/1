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
Case Type   : go驱动
Case Name   : 连接数据库，非数值类型校验
Description :
    1.新建用户并赋权
    2.配置pg_hba入口, sha256认证方法
    3.连接数据库，非数值类型校验
    4.还原pg_hba文件
    5.删除用户
    6.刪除go_conn.go
Expect      :
    1.执行成功
    2.执行成功
    3.执行成功，回显无panic提示
    4.执行成功
    5.执行成功
    6.执行成功
History     :
"""
import os
import re
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.ComGo import ComGo
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnGO51(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_root = Node('PrimaryRoot')
        self.log = Logger()
        self.go = ComGo()
        self.cons = Constant()
        self.db_user = 'go_user_51'
        self.go_file = 'go_conn.go'
        self.table_name = 't_go_51'
        self.cur_os = self.pri_root.sh('cat /etc/system-release').result()
        self.pg_hba_path = os.path.join(macro.DB_INSTANCE_PATH,
                                        macro.PG_HBA_FILE_NAME)
        text = f'-----{os.path.basename(__file__)} start-----'
        self.log.info(text)

        text = f'----前置检查：已安装golang1.11.1以上版本----'
        self.log.info(text)
        res = self.go.check_install_go(self.pri_user, '1.11.1')
        self.assertTrue(res, f'执行失败: {text}')

    def test_1(self):
        text = '----step1: 新建用户并赋权 expect: 成功----'
        self.log.info(text)
        sql = f"drop user if exists {self.db_user} cascade;" \
            f"create user {self.db_user} with password " \
            f"'{macro.COMMON_PASSWD}';" \
            f"grant all privileges to {self.db_user};"
        self.log.info(sql)
        res = self.pri_sh.execut_db_sql(sql)
        self.log.info(res)
        expect = f'{self.cons.DROP_ROLE_SUCCESS_MSG}.*' \
            f'{self.cons.CREATE_ROLE_SUCCESS_MSG}.*' \
            f'{self.cons.ALTER_ROLE_SUCCESS_MSG}'
        reg_res = re.search(expect, res, re.S)
        self.assertIsNotNone(reg_res, f'执行失败: {text}')

        text = '----step2: 配置pg_hba入口 expect: 成功----'
        self.log.info(text)
        cmd = f'cp {self.pg_hba_path} {self.pg_hba_path}_bak && ' \
            f'source {macro.DB_ENV_PATH} && ' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
            f'-h "host {self.pri_user.db_name} {self.db_user} ' \
            f'{self.pri_user.ssh_host}/32 sha256"'
        self.log.info(cmd)
        res = self.pri_user.sh(cmd).result()
        self.log.info(res)
        self.assertIn(self.cons.GSGUC_SUCCESS_MSG, res, f'执行失败: {text}')

        text = '----step3: 连接数据库，数值类型校验 expect: 成功----'
        self.log.info(text)
        conn_str = f'connStr := "host={self.pri_user.db_host} ' \
            f'port={self.pri_user.db_port} ' \
            f'user={self.db_user} ' \
            f'password={macro.COMMON_PASSWD} ' \
            f'dbname={self.pri_user.db_name} ' \
            f'sslmode=disable"'

        clean_sql = f"drop table if exists {self.table_name} cascade;"
        s_sql = f"{clean_sql}" \
            f"create table {self.table_name}" \
            f"(" \
            f"col1 money," \
            f"col2 boolean," \
            f"col3 CHAR(4)," \
            f"col4 CHARACTER(4)," \
            f"col5 NCHAR(4)," \
            f"col6 VARCHAR(10)," \
            f"col7 CHARACTER VARYING(10)," \
            f"col8 VARCHAR2(10)," \
            f"col9 NVARCHAR2(10)," \
            f"col10 TEXT," \
            f"col11 CLOB," \
            f"col12 BLOB," \
            f"col13 RAW," \
            f"col14 BYTEA," \
            f"col15 DATE," \
            f"col16 TIME," \
            f"col17 time with time zone," \
            f"col18 timestamp," \
            f"col19 timestamp with time zone," \
            f"col20 SMALLDATETIME," \
            f"col21 abstime," \
            f"col22 cidr," \
            f"col23 inet," \
            f"col24 macaddr," \
            f"col25 BIT(3)," \
            f"col26 BIT VARYING(5)," \
            f"col27 UUID," \
            f"col28 tsvector," \
            f"col29 tsquery," \
            f"col30 json," \
            f"col31 jsonb," \
            f"col32 hll(14)," \
            f"col33 int4range," \
            f"col34 int8range," \
            f"col35 numrange," \
            f"col36 tsrange," \
            f"col37 tstzrange," \
            f"col38 daterange," \
            f"col39 HASH16," \
            f"col40 HASH32" \
            f");"
        s_sq11 = f"insert into {self.table_name} values ('52093.89'::money," \
            f" true, 'aa', 'aa', 'aa', 'aa', 'aa', 'aa', 'aa', 'aa', " \
            f"'aa', empty_blob(), HEXTORAW('DEADBEEF'), " \
            f"E'\\\\\\\\\\\\\\xDEADBEEF'," \
            f" '1900-01-01 00:00:00', '1900-01-01 00:00:00 pst', " \
            f"'1900-01-01 00:00:00', '1900-01-01 00:00:00 pst', " \
            f"'1900-01-01 00:00:00', '1900-01-01 00:00:00', " \
            f"'1910-01-01 00:00:00', '10.10.10.10', '10.10.10.10', " \
            f"'08002b010203', B'10'::bit(3), B'00', " \
            f"'a0eebc999c0b4ef8bb6d6bb9bd380a11', 'test', 'test', " \
            f"'{{\\\"aa\\\":1}}'::json, '{{\\\"bb\\\":2}}'::jsonb, " \
            f"hll_empty(14,-1), '[1,10]', '[1,10]', '[0.00, 10.00]', " \
            f"'[1900-01-01 00:00:00, 2020-01-01 00:00:00]', " \
            f"'[1900-01-01 00:00:00 pst, 2020-01-01 00:00:00 pst]', " \
            f"'(1900-01-01, 2020-01-01)','ffff', " \
            f"'ffffffffffffffffffffffffffffffff');"
        col_list = [f"col{i}::text" for i in range(1, 41)]
        q_sql = f"select {','.join(col_list)} from {self.table_name};"
        params = {f"col{i}": "string" for i in range(1, 41)}
        f_contant = f'{self.go.get_head()}\n\n' \
            f'func cleanup(db *sql.DB) {{\n' \
            f'    {self.go.exec_sql(clean_sql)}' \
            f'\n\n    db.Close()\n' \
            f'}}\n\n' \
            f'func main() {{\n' \
            f'    {conn_str}\n' \
            f'    {self.go.conndb("connStr")}\n\n' \
            f'    defer cleanup(db)\n\n' \
            f'    {self.go.exec_sql(s_sql)}\n\n' \
            f'    {self.go.exec_sql(s_sq11, False)}\n\n' \
            f'    {self.go.query_row(q_sql, **params)}\n' \
            f'}}'
        cmd = f'cat > {self.go_file} <<EOF\n' \
            f'{f_contant}\n' \
            f'EOF\n'
        if 'CentOS' in self.cur_os:
            cmd += f'source /etc/profile; go run {self.go_file}'
        else:
            cmd += f'go run {self.go_file}'
        cmd = cmd.replace('{', '{{')
        cmd = cmd.replace('}', '}}')
        self.log.info(cmd)
        res = self.pri_root.sh(cmd).result()
        self.log.info(res)
        self.assertNotIn('panic: pq: ', res, f'执行失败: {text}')
        expect = '$52,093.89 true aa aa aa aa aa aa aa aa aa  DEADBEEF ' \
                 '\\xdeadbeef 1900-01-01 00:00:00 00:00:00 ' \
                 '00:00:00+08:05:43 1900-01-01 00:00:00 1900-01-01 ' \
                 '00:00:00+08:05:43 1900-01-01 00:00:00 1910-01-01 ' \
                 '00:00:00+08 10.10.10.10/32 10.10.10.10/32 ' \
                 '08:00:2b:01:02:03 100 00 ' \
                 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11 ' \
                 '\'test\' \'test\' {"aa":1} {"bb": 2} ' \
                 ' [1,11) [1,11) [0.00,10.00] ["1900-01-01 00:00:00",' \
                 '"2020-01-01 00:00:00"] ["1900-01-01 16:05:43+08:05:43",' \
                 '"2020-01-01 16:00:00+08"] [1900-01-02,2020-01-01)' \
        self.assertIn(expect, res, f'执行失败: {text}')

    def tearDown(self):
        text = '----run teardown----'
        self.log.info(text)

        s4_text = '----step4: 还原pg_hba文件  expect: 成功----'
        self.log.info(s4_text)
        cmd = f'mv {self.pg_hba_path}_bak {self.pg_hba_path}'
        self.log.info(cmd)
        cmd_res = self.pri_user.sh(cmd).result()
        self.log.info(cmd_res)

        is_restart = self.pri_sh.restart_db_cluster()

        s5_text = '----step5: 删除用户  expect: 成功----'
        self.log.info(s5_text)
        sql = f'drop user if exists {self.db_user} cascade;'
        sql_res = self.pri_sh.execut_db_sql(sql)
        self.log.info(sql_res)

        s6_text = '----step6: 刪除go_conn.go expect: 成功----'
        self.log.info(s6_text)
        rm_cmd = f'rm -rf {self.go_file}'
        self.log.info(rm_cmd)
        rm_res = self.pri_root.sh(rm_cmd).result()
        self.log.info(rm_res)

        self.assertEqual(len(cmd_res), 0, f'执行失败: {s4_text}')
        self.assertTrue(is_restart, f'执行失败: {s4_text}')
        self.assertIn(self.cons.DROP_ROLE_SUCCESS_MSG,
                      sql_res,
                      f'执行失败: {s5_text}')
        self.assertIs(rm_res, '', f'执行失败: {s6_text}')

        text = f'-----{os.path.basename(__file__)} end-----'
        self.log.info(text)
