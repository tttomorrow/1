-- @testpoint: Hash分区表结合LIKE参数

--step1：创建hash分区表 expect：成功
drop table if exists partition_hash_tab;
create table partition_hash_tab
(id                         number(7)
   constraint partition_hash_tab_id_nn not null,
 use_filename               varchar2(20),
 filename                   varchar2(255),
 text                       varchar2(2000))
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入数据 expect：成功
insert into partition_hash_tab values(1,'李','李四','数学老师');
insert into partition_hash_tab values(2,'王','王五','化学老师');

--step3：查询数据 expect：成功
select * from partition_hash_tab;

--step4：结合like参数建表 expect：成功
create table partition_hash_tab1 (like  partition_hash_tab);

--step5：查询数据 expect：成功
select * from partition_hash_tab1;

--step6：清理环境 expect：成功
drop table if exists partition_hash_tab1;
drop table if exists partition_hash_tab;