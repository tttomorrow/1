-- @testpoint: range_list二级分区表：相关系统表pg_partition/pg_depend,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0226_01 cascade;
drop table if exists t_subpartition_0226 cascade;
drop tablespace if exists ts_subpartition_0226;
create tablespace ts_subpartition_0226 relative location 'subpartition_tablespace/subpartition_tablespace_0226';

--test1: 相关系统表 --pg_partition
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0226
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0226
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0226 values(-1,1,1,1),(-4,1,4,4),(-5,5,5,5),(-8,8,8,8),(-19,9,9,9);
insert into t_subpartition_0226 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0226 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step14: 查询分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0226') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0226')) b where a.parentid = b.oid order by a.relname;
--step6: 分区键创建本地索引; expect:成功
drop index if exists index_01;
create index index_01 on t_subpartition_0226(col_2) local ;
--step7: 系统表查看索引信息 expect:成功
select relname, parttype, partstrategy, boundaries, indisusable from pg_partition where relname = 'p_list_1_1_col_2_idx';
--step8: 设置分区索引不可用 expect:成功
alter index  index_01 modify partition p_list_1_1_col_2_idx  unusable;
--step14: 查询分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0226') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0226')) b where a.parentid = b.oid order by a.relname;

--step9: 重命名分区索引 expect:成功
alter index index_01 rename partition p_list_2_2_col_2_idx to  aaaaaaa;
--step10: 设置分区索引不可用 expect:成功
alter index  index_01 modify partition aaaaaaa  unusable;
--step11: 重置分区索引可用 expect:成功
alter index index_01 rebuild  partition aaaaaaa ;
--step12: 设置分区内索引不可用 expect:合理报错
alter table t_subpartition_0226 modify partition p_range_2  unusable local indexes;

--test2: 相关系统表 --pg_depend
--step13: 创建普通表; expect:成功
drop table if exists t_subpartition_0226_01 cascade;
create table if not exists t_subpartition_0226_01
(
    col_1 int ,
    col_2 int unique ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0226;
--step14: 插入数据; expect:成功
insert into t_subpartition_0226_01 values(-1,1,1,1),(-4,4,4,4),(-5,5,5,5),(-8,8,8,8),(-19,9,9,9);
insert into t_subpartition_0226_01 values(1,12,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0226_01 values(11,13,1,1),(14,14,4,4),(15,15,5,5),(18,81,8,8),(19,91,9,9);

--step15: 创建二级分区表,指定外键; expect:成功
drop table if exists t_subpartition_0226 cascade;
create table if not exists t_subpartition_0226
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int ,
    foreign key (col_2) references  t_subpartition_0226_01(col_2)
)tablespace ts_subpartition_0226
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step16: 插入数据; expect:成功
insert into t_subpartition_0226 values(11,13,1,1),(14,14,4,4),(15,15,5,5),(18,81,8,8),(19,91,9,9);

--step17: 查询系统表pg_depend的数据; expect:成功
select objsubid,refobjsubid,deptype from pg_depend  where refobjid = (select oid from pg_class where relname = 't_subpartition_0226') ;

--step18: 清理环境; expect:成功
drop table if exists t_subpartition_0226_01 cascade;
drop table if exists t_subpartition_0226 cascade;
drop tablespace if exists ts_subpartition_0226;