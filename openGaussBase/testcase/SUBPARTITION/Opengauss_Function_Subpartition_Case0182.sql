-- @testpoint: list_hash二级分区表：同义词/主键外键/pg_constraint,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0182;
drop tablespace if exists ts_subpartition_0182;
create tablespace ts_subpartition_0182 relative location 'subpartition_tablespace/subpartition_tablespace_0182';
--test1: 同义词
--step2: 创建二级分区表; expect:成功
create table t_subpartition_0182
(
    col_1 int,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0182
partition by list (col_1) subpartition by hash (col_2)
(
  partition p_list_1 values (-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
    subpartition p_hash_1_3 
  ),
  partition p_list_2 values (1,2,3,4,5,6,7,8,9,10 )
  (
    subpartition p_hash_2_1 ,
    subpartition p_hash_2_2 ,
    subpartition p_hash_2_3 ,
    subpartition p_hash_2_4 ,
    subpartition p_hash_2_5 
  ),
  partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
  partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
  (
    subpartition p_hash_4_1 
  ),
  partition p_list_5 values (default)
  (
    subpartition p_hash_5_1 
  ),
  partition p_list_6 values (31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_hash_6_1 ,
    subpartition p_hash_6_2 ,
    subpartition p_hash_6_3 
  )
) enable row movement ;
--step3: 创建表同义词; expect:成功
drop synonym if exists syn_subpartition_0182_01;
create or replace synonym syn_subpartition_0182_01 for t_subpartition_0182;
--step4: 查询表同义词数据; expect:成功
select * from syn_subpartition_0182_01;

--test2: 使用同义词对数据操作
--step5: 插入数据; expect:成功
insert into syn_subpartition_0182_01 values(0,0,0,0);
insert into syn_subpartition_0182_01 values(1,1,1,1),(4,1,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into syn_subpartition_0182_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into syn_subpartition_0182_01 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
insert into  syn_subpartition_0182_01 values (generate_series(-19, 19),generate_series(-10, 100),generate_series(0, 99));
update syn_subpartition_0182_01 set col_2=8 where col_2=4;
delete syn_subpartition_0182_01 where col_2=8;
select count(*) from syn_subpartition_0182_01;

--step6: 创建视图; expect:成功
drop view if exists t_subpartition_0182_view;
create view t_subpartition_0182_view as select * from t_subpartition_0182;
--step7: 对视图创建同义词; expect:成功
drop synonym if exists syn_subpartition_0182_02;
create synonym syn_subpartition_0182_02 for t_subpartition_0182_view;
--step8: 查看视图同义词数据; expect:成功
select count(*) from syn_subpartition_0182_02;
--step9: 删除视图同义词数据; expect:合理报错
delete syn_subpartition_0182_02 where col_2=8;
--step10: 删除同义词; expect:成功
drop synonym syn_subpartition_0182_02;
drop synonym syn_subpartition_0182_01;

--test3: 主键外键
--step11: 创建普通表,指定主键; expect:成功
drop table if exists t_subpartition_0182_01 cascade;
create table t_subpartition_0182_01
(
    col_1 int primary key,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
);
--step12: 创建二级分区表,指定外键; expect:成功
drop table if exists t_subpartition_0182 cascade;
create table t_subpartition_0182
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int ,
    foreign key(col_1) references t_subpartition_0182_01(col_1)
)
tablespace ts_subpartition_0182
partition by list (col_1) subpartition by hash (col_2)
(
  partition p_list_1 values (-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
    subpartition p_hash_1_3 
  ),
  partition p_list_2 values (1,2,3,4,5,6,7,8,9,10 )
  (
    subpartition p_hash_2_1 ,
    subpartition p_hash_2_2 ,
    subpartition p_hash_2_3 ,
    subpartition p_hash_2_4 ,
    subpartition p_hash_2_5 
  ),
  partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
  partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
  (
    subpartition p_hash_4_1 
  ),
  partition p_list_5 values (default)
  (
    subpartition p_hash_5_1 
  ),
  partition p_list_6 values (31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_hash_6_1 ,
    subpartition p_hash_6_2 ,
    subpartition p_hash_6_3 
  )
) enable row movement ;
--step13: 向二级分区表插入普通表没有的数据; expect:合理报错
insert into t_subpartition_0182 values(0,0,0,0);
--step14: 插入数据; expect:成功
insert into t_subpartition_0182_01 values(0,0,0,0);
insert into t_subpartition_0182 values(0,0,0,0);
--step15: 更新数据; expect:成功
update t_subpartition_0182 set col_2=8 where col_2=0;
--step16: 更新二级分区表数据为普通表没有的数据; expect:合理报错
update t_subpartition_0182 set col_1=8 where col_2=8;
--step17: 删除数据; expect:成功
delete t_subpartition_0182 where col_2=8;
--step18: 更新普通表数据; expect:成功
update t_subpartition_0182_01 set col_1=8 where col_2=0;

--test4: pg_constraint
--step19: 清空普通表数据; expect:合理报错
truncate t_subpartition_0182_01;
--step20: 指定cascade清空普通表数据; expect:成功
truncate t_subpartition_0182_01 cascade;
--step21: 查询pg_constraint数据; expect:成功
select conname,contype,condeferrable,condeferred,convalidated from pg_constraint where conname='t_subpartition_0182_col_1_fkey';

--step22: 清理环境; expect:成功
drop table if exists t_subpartition_0182_01  cascade;
drop table if exists t_subpartition_0182  cascade;
drop tablespace if exists ts_subpartition_0182;