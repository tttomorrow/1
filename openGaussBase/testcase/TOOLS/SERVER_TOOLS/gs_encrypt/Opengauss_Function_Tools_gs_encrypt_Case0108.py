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
Case Type   : 服务端工具
Case Name   : gs_encrypt工具使用参数--key-base64，--vector-base64加明文字符串，
              --key-base64后输入只包含特殊字符的口令
Description :
    1.生成8位纯特殊字符的口令以base64方式编码后的密钥；
      base64.b64encode([用户输入的口令].encode(encoding='utf-8'))
    2.生成16位字符串以base64方式编码后的密文；
      base64.b64encode([用户输入的16位字符串].encode(encoding='utf-8'))
    3.执行命令，使用--key-base64，--vector-base64参数加密明文字符串
      gs_encrypt --key-base64=[用户输入口令加密的密文]
      --vector-base64=[用户输入字符串加密的密文] [待加密明文字符串]
Expect      :
    1.成功生成密钥；
    2.成功生成随机数密文；
    3.执行失败，报错提示口令至少包含3种类型字符
History     :
"""

import os
import base64
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant


class GsEncrypt60(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.dbuserNode = Node('PrimaryDbUser')
        self.con = Constant()
        self.common = Common()

    def test_gs_encrypt(self):
        self.logger.info('------------------进行加密操作------------------')
        step = "step1-2:生成8位纯生成以base64方式编码后的密钥,生成以base64方" \
               "式编码的16位字符串密文  except:成功生成密钥，成功生成密文"
        self.logger.info(step)
        str1 = 'test'
        encrypt = '&&&&&&&&'
        rand = '123456789123456l'
        enc = encrypt.encode(encoding='utf-8')
        enc1 = rand.encode(encoding='utf-8')
        key = base64.b64encode(enc)
        vec = base64.b64encode(enc1)
        self.assertEqual(type(key), bytes, step)
        self.assertEqual(type(vec), bytes, step)

        step = "step3:执行命令，使用--key-base64，--vector-base64参数加密明文" \
               "字符串 except:执行失败，报错提示口令至少包含3种类型字符"
        self.logger.info(step)
        key_spl = str(key).split("'")[1]
        vec_spl = str(vec).split("'")[1]
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_encrypt --key-base64={key_spl} \
            --vector-base64={vec_spl}  {str1}'''
        self.logger.info(check_cmd1)
        self.logger.info("------------加密结果-----------")
        msg1 = self.common.get_sh_result(self.dbuserNode, check_cmd1)
        self.assertIn(self.con.encrypted_fail_msg, msg1, "执行失败" + step)

    def tearDown(self):
        self.logger.info('--------------无需清理环境-------------------')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
