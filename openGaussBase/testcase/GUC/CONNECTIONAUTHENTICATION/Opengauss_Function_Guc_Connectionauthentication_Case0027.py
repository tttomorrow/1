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
Case Type   : GUC
Case Name   : 使用ALTER SYSTEM SET修改数据库参数listen_addresses为空值
Description :
    1、查看listen_addresses默认值
        source [环境变量路径]
        gs_guc check -D [数据库实例路径] -c listen_addresses
    2、使用ALTER SYSTEM SET修改数据库参数listen_addresses为''
        gsql -d [数据库名] -p [端口号]
        alter system set listen_addresses to ''；
    3、重启数据库使其生效
        gs_om -t stop && gs_om -t start
    4、恢复默认值并重启数据库
        gs_guc set -D [数据库实例路径] -c "listen_addresses=[各节点默认值]"
        gs_om -t stop && gs_om -t start | gs_om -t restart
Expect      :
    1、查看listen_addresses默认值成功；
    2、ALTER SYSTEM SET设置listen_addresses成功；
    3、重启数据库成功；
    4、恢复默认值，重启数据库成功
History     : 2021/8/18 为适配listen_addresses默认值变更，修改正则写法
"""
import re
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import macro

logger = Logger()
primary_commonsh = CommonSH("PrimaryDbUser")


class GucSetListenAddresses(unittest.TestCase):
    def setUp(self):
        logger.info(
            "Opengauss_Function_Guc_Connectionauthentication_Case0027开始执行"
        )
        # 查看数据库状态是否正常
        db_status = primary_commonsh.get_db_cluster_status("status")
        if not db_status:
            logger.info("The status of db cluster is abnormal. Please check! \
                                db_status: {}".format(db_status))
            self.assertTrue(db_status)

        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.constant = Constant()
        # 1、查看listen_addresses默认值，获取默认值
        logger.info("在当前节点查看listen_addresses默认值")
        parameter = "listen_addresses"
        strs = primary_commonsh.execute_gsguc(command="check",
                                              assert_flag="",
                                              param=parameter,
                                              get_detail=True,
                                              single=True)
        str_list = strs.split("\n")
        logger.info(str_list)
        self.default_ip = ""
        # 举个例子listen_addresses='localhost,192.168.0.100'
        reg1 = re.compile(r"(?<=listen_addresses=')\w{9},\d+\.\d+\.\d+\.\d+|$")
        for string in str_list:
            default_ip_list = reg1.findall(string)
            if default_ip_list and default_ip_list[0]:
                self.default_ip = "\'{}\'".format(default_ip_list[0])
                break
        if not self.default_ip:
            raise Exception("listen_addresses默认值获取为空，请检查")
        logger.info(f"当前节点listen_addresses默认值为:{self.default_ip}")

    def test_guc_set_listen_addresses(self):
        # 2、使用ALTER SYSTEM SET修改数据库参数listen_addresses为空
        logger.info("使用ALTER SYSTEM SET修改数据库参数listen_addresses为空值")
        sql1 = "alter system set listen_addresses to ''"
        logger.info(sql1)
        body1 = primary_commonsh.execut_db_sql(sql1)
        logger.info(body1)
        self.assertIn(self.constant.ALTER_SYSTEM_SUCCESS_MSG, body1)
        # 3、重启数据库
        if primary_commonsh.restart_db_cluster():
            logger.info("修改默认值为''后，重启数据库成功，符合预期")
        logger.info("使用ALTER SYSTEM SET设置listen_addresses完成")

    def tearDown(self):
        logger.info("---------------------无需清理环境--------------------------")
        if self.default_ip:
            logger.info("将listen_addresses还原为默认ip")
            sql2 = f"alter system set listen_addresses to {self.default_ip}"
            logger.info(sql2)
            body2 = primary_commonsh.execut_db_sql(sql2)
            logger.info(body2)
            self.assertIn(self.constant.ALTER_SYSTEM_SUCCESS_MSG, body2)
            # 3、重启数据库
            if not primary_commonsh.restart_db_cluster():
                raise Exception("恢复默认值后，数据库重启失败，请检查！")
            else:
                logger.info("数据库重启成功")
        logger.info(
            "Opengauss_Function_Guc_Connectionauthentication_Case0027执行结束"
        )
