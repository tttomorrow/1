-- @testpoint: list_range二级分区表：表空间

--test1: tablespace
--step1: 创建二级分区表，指定表空间，一级分区主键using index tablespace; expect:成功
drop table if exists t_subpartition_0086;
drop tablespace if exists ts_subpartition_0086;
create tablespace ts_subpartition_0086 relative location 'subpartition_tablespace/subpartition_tablespace_0086';
drop tablespace if exists ts_subpartition_0086_01;
create tablespace ts_subpartition_0086_01 relative location 'subpartition_tablespace/subpartition_tablespace_0086_01';
create   table if not exists t_subpartition_0086
(
    col_1 int primary key   using index tablespace ts_subpartition_0086_01,
    col_2 int  ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0086
partition by list (col_1) subpartition by range (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_range_1_1 values less than( -10 ),
    subpartition p_range_1_2 values less than( 0 ),
    subpartition p_range_1_3 values less than( 10 ),
    subpartition p_range_1_4 values less than( 20 ),
    subpartition p_range_1_5 values less than( 50 )
  ),
  partition p_list_2 values(1,2,3,4,5,6,7,8,9,10 ),
  partition p_list_3 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_range_3_1 values less than( 15 ),
    subpartition p_range_3_2 values less than( maxvalue )
  ),
    partition p_list_4 values(21,22,23,24,25,26,27,28,29,30)
  (
    subpartition p_range_4_1 values less than( -10 ),
    subpartition p_range_4_2 values less than( 0 ),
    subpartition p_range_4_3 values less than( 10 ),
    subpartition p_range_4_4 values less than( 20 ),
    subpartition p_range_4_5 values less than( 50 )
  ),
   partition p_list_5 values(31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_range_5_1 values less than( maxvalue )
  ),
   partition p_list_6 values(41,42,43,44,45,46,47,48,49,50)
   (
    subpartition p_range_6_1 values less than( -10 ),
    subpartition p_range_6_2 values less than( 0 ),
    subpartition p_range_6_3 values less than( 10 ),
    subpartition p_range_6_4 values less than( 20 ),
    subpartition p_range_6_5 values less than( 50 )
   ),
   partition p_list_7 values(default)
) enable row movement;
--step2: 查询指定二级分区表空间; expect:成功
select p.relname, t.spcname from pg_partition p, pg_tablespace t where p.reltablespace=t.oid and p.relname='p_range_4_5';
--step3: 查询指定一级分区表空间; expect:成功
select p.relname, t.spcname from pg_partition p, pg_tablespace t where p.reltablespace=t.oid and p.relname='p_list_6';

--step4: 清理环境; expect:成功
drop table if exists t_subpartition_0086;
drop tablespace if exists ts_subpartition_0086;
drop tablespace if exists ts_subpartition_0086_01;