-- @testpoint: Hash分区表结合关键字NOCOMPRESS则不对表进行压缩

--step1：创建hash分区表 expect：成功
drop table if exists t_partition_hash_0068_01;
create table t_partition_hash_0068_01(
id int,
name varchar(100),
age int
)nocompress
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入数据 expect：成功插入1000条数据
begin
	for i in 1..1000 loop
insert into t_partition_hash_0068_01 values(1,'张三',26);
    end loop;
end;
/

--step3：查询数据 expect：成功展示数据数量为1000
select count(*) from t_partition_hash_0068_01;

--step4：清理环境 expect：成功
drop table if exists t_partition_hash_0068_01;