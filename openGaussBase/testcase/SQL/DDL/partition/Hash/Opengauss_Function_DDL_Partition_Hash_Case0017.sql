-- @testpoint: 创建普通hash分区表，验证不支持的数据类型（网络地址类型） 合理报错

--step1：不支持的数据类型，网络地址类型的cidr类型 expect：合理报错
drop table if exists partition_hash_tab_t1;
create table partition_hash_tab_t1(p_id int,p_cidr cidr)
partition by hash(p_cidr)
(partition part_1,
 partition part_2);

--step2：不支持的数据类型，网络地址类型的inet类型 expect：合理报错
drop table if exists partition_hash_tab_t2;
create table partition_hash_tab_t2(p_id int,p_inet inet)
partition by hash(p_inet)
(partition part_1,
 partition part_2);

--step2：不支持的数据类型，网络地址类型的macaddr类型 expect：合理报错
drop table if exists partition_hash_tab_t3;
create table partition_hash_tab_t3(p_id int,p_macaddr macaddr)
partition by hash(p_macaddr)
(partition part_1,
 partition part_2);

--step3：清理环境 expect：成功
--No need to clean