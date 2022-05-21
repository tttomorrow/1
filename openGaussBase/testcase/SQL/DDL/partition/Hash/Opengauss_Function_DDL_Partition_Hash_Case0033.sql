-- @testpoint: Hash分区表上以truncate方式创建触发器

--step1：创建hash分区表、触发表 expect：成功
drop table if exists partition_hash_tab;
create table partition_hash_tab(p_id int,p_name varchar)
partition by hash(p_id)
(partition p1,
 partition p2,
 partition p3,
 partition p4);
drop table if exists partition_hash_des_tab;
create table partition_hash_des_tab(p_id int);

--step2：插入数据 expect：成功
BEGIN
  for i in 1..20 LOOP
    insert into partition_hash_tab values(i);
  end LOOP;
end;
/

--step3：创建触发器函数 expect：成功
CREATE OR REPLACE FUNCTION truncate_func() RETURNS TRIGGER AS
           $$
           DECLARE
           BEGIN
                   insert into partition_hash_des_tab values(1);
                   RETURN NULL;
           END
           $$ LANGUAGE PLPGSQL;
/

--step4：创建truncate触发器 expect：成功
CREATE TRIGGER truncate_trigger
           before truncate on partition_hash_tab
           FOR EACH STATEMENT
           EXECUTE PROCEDURE truncate_func();
/

--step5：truncate数据 expect：成功
truncate table partition_hash_tab;

--step6：查看触发器是否生效 expect：成功
SELECT * FROM partition_hash_des_tab;

--step7：清理环境 expect：成功
DROP TRIGGER truncate_trigger on partition_hash_tab;
drop table if exists partition_hash_tab;
drop table if exists partition_hash_des_tab;
drop FUNCTION truncate_func() ;