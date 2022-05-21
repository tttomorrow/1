-- @testpoint: 创建普通hash分区表，验证不支持的数据类型（money货币类型） 合理报错

--step1：不支持的数据类型，money货币类型 expect：合理报错
drop table if exists partition_hash_tab_t1;
create table partition_hash_tab_t1(p_id int,p_money money)
partition by hash(p_money)
(partition part_1,
 partition part_2);

--step2：清理环境 expect：成功
--No need to clean