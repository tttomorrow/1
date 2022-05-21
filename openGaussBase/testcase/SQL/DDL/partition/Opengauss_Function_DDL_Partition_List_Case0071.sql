-- @testpoint: List分区表结合表约束unique,部分测试点合理报错

--step1:创建list分区表,结合表约束;expect:成功
drop table if exists t_partition_list_0071;
create table t_partition_list_0071
(id                int,
age                int ,
number             int,
text               VARCHAR2(2000),
unique(age,number))
partition by list(id)
(partition p1 values(10),
 partition p2 values(20));

--step2:插入数据;expect:合理报错
insert into  t_partition_list_0071 values(10,10,10,'hahahahah');
insert into  t_partition_list_0071 values(20,10,-10,'hahahahah');
insert into  t_partition_list_0071 values(20,10,10,'hahahahah');

--step3:查看数据;expect:成功
select * from t_partition_list_0071 order by id desc;

--step4:清理环境
drop table if exists t_partition_list_0071;

