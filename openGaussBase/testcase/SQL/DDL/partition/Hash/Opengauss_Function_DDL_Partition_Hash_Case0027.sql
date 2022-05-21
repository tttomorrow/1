-- @testpoint: Hash分区表上以concurrently方式创建索引，合理报错

--step1：创建hash分区表 expect：成功
drop table if exists partition_hash_tab;
create table partition_hash_tab(p_id int)
partition by hash(p_id)
(partition p1,
 partition p2,
 partition p3,
 partition p4);

--step2：插入数据 expect：成功
BEGIN
  for i in 1..2000 LOOP
    insert into partition_hash_tab values(i);
  end LOOP;
end;
/

--step3：创建concurrently索引 expect：合理报错
create index concurrently partition_index_1 on partition_hash_tab(p_id);

--step4：清理环境 expect：成功
drop index if exists partition_index_1;
drop table if exists partition_hash_tab cascade;