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
Case Type   : 基础功能
Case Name   : 修改订阅，验证订阅更改新的所有者
Description :
    1:创建用户，赋予所有权限
    2:在两个集群中创建相同字段表
    3:创建发布端(集群A)
    4.1:创建订阅（集群B）,指定参数enabled为false  expect:创建订阅成功
    4.2:向发布端表中插入数据   expect:成功
    4.3:查询集群B中表中数据是否同步   expect:数据未同步
    4.4:修改订阅，使订阅可用   expect:修改订阅成功
    4.5:再次向发布端表中插入数据   expect:成功
    4.6:查询集群B中表中数据是否同步   expect:再次插入数据后同步
Expect      :
    1：成功
    2：成功
    3：成功
    4.1：成功
    4.2：插入数据成功
    4.3：数据未成功
    4.4：修改订阅成功
    4.5：再次插入数据成功
    4.6：数据同步
History     :
"""
import unittest
import os
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(3 != Primary_SH.get_node_num(), '非1+2环境不执行')
class Pubsubclass(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} start-----")
        self.pri_userdb_pub = Node(node='PrimaryDbUser')
        self.pri_userdb_sub = Node(node='remote1_PrimaryDbUser')
        self.constant = Constant()
        self.commsh_pub = CommonSH('PrimaryDbUser')
        self.commsh_sub = CommonSH('remote1_PrimaryDbUser')
        self.com_pub = Common()
        self.subname1 = "sub_case113_1"
        self.pubname1 = "pub_case113_1"
        self.tb_name1 = "public.t_case113_1"
        self.parent_path_pub = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.parent_path_sub = os.path.dirname(macro.DB_INSTANCE_PATH_REMOTE1)
        self.port = str(int(self.pri_userdb_pub.db_port) + 1)
        self.wal_level = self.com_pub.show_param("wal_level")
        self.user_name = "u_case113_1"
        self.user_param_u = f'-U {self.user_name} ' \
            f'-W {macro.COMMON_PASSWD}'
        self.user_param_pub = f'-U {self.pri_userdb_pub.db_user} ' \
            f'-W {self.pri_userdb_pub.db_password}'
        self.user_param_sub = f'-U {self.pri_userdb_sub.db_user} ' \
            f'-W {self.pri_userdb_sub.db_password}'

        cmd = f"cp " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')} " \
            f"{os.path.join(self.parent_path_pub, 'pg_hba.conf')};"
        self.log.info(cmd)
        result = self.pri_userdb_pub.sh(cmd).result()
        self.log.info(result)
        cmd = f"cp " \
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE1, 'pg_hba.conf')}" \
            f" {os.path.join(self.parent_path_sub, 'pg_hba.conf')};"
        self.log.info(cmd)
        result = self.pri_userdb_sub.sh(cmd).result()
        self.log.info(result)
        self.user_name2 = "u_case113_2"

    def test_pubsub(self):
        text = '--step:预置条件,修改pg_hba expect:成功'
        self.log.info(text)
        self.log.info("#######发布端: ")
        guc_res = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    replication  all '
            f'{self.pri_userdb_sub.db_host}/32 sha256')
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        guc_res = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    {self.pri_userdb_pub.db_name}  {self.user_name} '
            f'{self.pri_userdb_sub.db_host}/32 sha256')
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG, 'wal_level=logical')
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_pub.restart_db_cluster(True)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)
        self.log.info("#######订阅端: ")
        guc_res = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  all '
            f'{self.pri_userdb_pub.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        guc_res = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host {self.pri_userdb_sub.db_name}  {self.user_name} '
            f'{self.pri_userdb_sub.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)

        text = "--step1:创建用户，赋予所有权限 expect:成功--"
        self.log.info(text)
        sql = f"create user {self.user_name} password " \
            f"'{macro.COMMON_PASSWD}';" \
            f"grant all privileges to {self.user_name};"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result,
                      '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result,
                      '执行失败:' + text)

        text = '--step2:在两个集群中创建相同字段表 expect:成功--'
        self.log.info(text)
        create_sql = f'create table {self.tb_name1}' \
            f'(id int primary key,name text);'
        result = self.commsh_pub.execut_db_sql(
            create_sql, sql_type=self.user_param_u)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS,
                      result, '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(create_sql,
                                               self.user_param_u, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS,
                      result, '执行失败:' + text)

        text = "--step3:创建发布端(集群A) expect:成功--"
        self.log.info(text)
        sql = f"CREATE PUBLICATION {self.pubname1} for all tables;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_u)
        self.log.info(result)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)

        text = "--step4.1:创建订阅（集群B）  expect:创建订阅成功--"
        self.log.info(text)
        result = self.commsh_sub.execute_generate(
            macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertIn('', result, '执行失败:' + text)
        sql = f"CREATE SUBSCRIPTION {self.subname1} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.user_name} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={macro.COMMON_PASSWD}' " \
            f"PUBLICATION {self.pubname1} ; "
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_u, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1],
                         result, '执行失败:' + text)
        self.assertIn(self.constant.create_sub_succ_msg, result,
                      '执行失败:' + text)

        text = "--step4.2:修改订阅所属用户为current_user   expect:成功--"
        self.log.info(text)
        sql = f"alter subscription {self.subname1} " \
            f"owner to {self.pri_userdb_sub.db_user};" \
            f"select pg_sleep(10);"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)
        self.assertIn(self.constant.alter_sub_succ_msg,
                      result, '执行失败:' + text)

        text = "--step5.1:创建订阅（集群B）  expect:创建订阅成功--"
        self.log.info(text)
        self.assertIn('', result, '执行失败:' + text)
        sql = f"drop SUBSCRIPTION {self.subname1} ;" \
            f"CREATE SUBSCRIPTION {self.subname1} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.user_name} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={macro.COMMON_PASSWD}' " \
            f"PUBLICATION {self.pubname1} ; "
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_u, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1],
                         result, '执行失败:' + text)
        self.assertIn(self.constant.create_sub_succ_msg, result,
                      '执行失败:' + text)

        text = "--step5.2:修改订阅所属用户为session_user   expect:成功--"
        self.log.info(text)
        sql = f"alter subscription {self.subname1} " \
            f"owner to {self.user_name};" \
            f"select pg_sleep(10);"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_u, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)
        self.assertIn(self.constant.alter_sub_succ_msg,
                      result, '执行失败:' + text)

        text = "--step6.1:创建订阅（集群B）  expect:创建订阅成功--"
        self.log.info(text)
        self.assertIn('', result, '执行失败:' + text)
        sql = f"drop SUBSCRIPTION {self.subname1} ;" \
            f"CREATE SUBSCRIPTION {self.subname1} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.user_name} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={macro.COMMON_PASSWD}' " \
            f"PUBLICATION {self.pubname1} ; "
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_u, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1],
                         result, '执行失败:' + text)
        self.assertIn(self.constant.create_sub_succ_msg, result,
                      '执行失败:' + text)

        text = "--step6.2:创建新用户，赋予所有权限  expect:成功--"
        self.log.info(text)
        sql = f"create user {self.user_name2} " \
            f"with sysadmin password '{macro.COMMON_PASSWD}';"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result,
                      '执行失败:' + text)

        text = "--step6.3:修改订阅所属用户为具有超级用户权限的新用户   expect:成功--"
        self.log.info(text)
        sql = f"alter subscription {self.subname1} " \
            f"owner to {self.user_name2};" \
            f"select pg_sleep(10);"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_u, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)
        self.assertIn(self.constant.alter_sub_succ_msg,
                      result, '执行失败:' + text)

        text = "--step6.4:使用非创建订阅用户连接数据库，修改订阅所属用户为" \
               "current_user:session_user   expect:成功--"
        self.log.info(text)
        sql = f"alter subscription {self.subname1} " \
            f"owner to {self.pri_userdb_sub.db_user};" \
            f"select pg_sleep(10);"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)
        self.assertIn(self.constant.alter_sub_succ_msg,
                      result, '执行失败:' + text)

        text = "--step7.1:创建订阅（集群B）  expect:创建订阅成功--"
        self.log.info(text)
        self.assertIn('', result, '执行失败:' + text)
        sql = f"drop SUBSCRIPTION {self.subname1} ;" \
            f"CREATE SUBSCRIPTION {self.subname1} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.user_name} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={macro.COMMON_PASSWD}' " \
            f"PUBLICATION {self.pubname1} ; "
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_u, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1],
                         result, '执行失败:' + text)
        self.assertIn(self.constant.create_sub_succ_msg, result,
                      '执行失败:' + text)

        text = "--step7.2:创建新用户，赋予create权限   expect:成功--"
        self.log.info(text)
        sql = f"drop user {self.user_name2};" \
            f"create user {self.user_name2} " \
            f"with createrole password '{macro.COMMON_PASSWD}';"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result,
                      '执行失败:' + text)

        text = "--step7.3:修改订阅所属用户为只具有create权限的新用户   expect:失败，权限不够--"
        self.log.info(text)
        sql = f"alter subscription {self.subname1} " \
            f"owner to {self.user_name2};" \
            f"select pg_sleep(10);"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_u, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.PERMISSION_DENIED,
                      result, '执行失败:' + text)

        text = "--step8.1:创建订阅（集群B）   expect:创建订阅成功--"
        self.log.info(text)
        self.assertIn('', result, '执行失败:' + text)
        sql = f"drop SUBSCRIPTION {self.subname1} ;" \
            f"CREATE SUBSCRIPTION {self.subname1} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.user_name} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={macro.COMMON_PASSWD}' " \
            f"PUBLICATION {self.pubname1} ; "
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_u, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1],
                         result, '执行失败:' + text)
        self.assertIn(self.constant.create_sub_succ_msg, result,
                      '执行失败:' + text)

        text = "--step8.2:创建新用户，无create权限   expect:成功--"
        self.log.info(text)
        sql = f"drop user {self.user_name2};" \
            f"create user {self.user_name2} password '{macro.COMMON_PASSWD}';"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result,
                      '执行失败:' + text)

        text = "--step8.3:修改订阅所属用户为无create权限的新用户   expect:失败，权限不够--"
        self.log.info(text)
        sql = f"alter subscription {self.subname1} " \
            f"owner to {self.user_name2};" \
            f"select pg_sleep(10);"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_u, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.PERMISSION_DENIED,
                      result, '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = "--环境清理--"
        self.log.info(text)
        sql = f"DROP SUBSCRIPTION  {self.subname1};"
        drop_sub_result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_u, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)
        sql = f"DROP PUBLICATION  {self.pubname1};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_u)
        self.log.info(drop_pub_result)
        sql = f"DROP table if exists {self.tb_name1};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_u, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_u)
        self.log.info(result)
        sql = f"drop user {self.user_name} cascade;" \
            f"drop user {self.user_name2} cascade;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        cmd = f"mv " \
            f"{os.path.join(self.parent_path_pub, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')};"
        self.log.info(cmd)
        result = self.pri_userdb_pub.sh(cmd).result()
        self.log.info(result)
        cmd = f"mv " \
            f"{os.path.join(self.parent_path_sub, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE1, 'pg_hba.conf')} "
        self.log.info(cmd)
        result = self.pri_userdb_sub.sh(cmd).result()
        self.log.info(result)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'wal_level={self.wal_level}')
        self.assertTrue(result, '执行失败:' + text)
        self.commsh_pub.restart_db_cluster(True)
        self.commsh_sub.restart_db_cluster(True, macro.DB_ENV_PATH_REMOTE1)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")
