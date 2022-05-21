-- @testpoint: list_hash二级分区表：分区键为表达式/分区数0,测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0151;
drop tablespace if exists ts_subpartition_0151;
create tablespace ts_subpartition_0151 relative location 'subpartition_tablespace/subpartition_tablespace_0151';
drop tablespace if exists ts_subpartition_0151_01;
create tablespace ts_subpartition_0151_01 relative location 'subpartition_tablespace/subpartition_tablespace_0151_01';

--test1: 分区键 --分区键为表达式--不支持
--step2: 创建二级分区表,二级分区键为表达式; expect:合理报错
create table if not exists t_subpartition_0151
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0151
partition by list (col_1) subpartition by hash (upper(col_2))
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

--test2: 分区数--0个
--step3: 创建二级分区表,一级分区与二级分区数都为0; expect:合理报错
drop table if exists t_subpartition_0151;
create table if not exists t_subpartition_0151
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0151
partition by list (col_1) subpartition by hash (col_2)()
 enable row movement;

--step4: 创建二级分区表，二级分区数都为0; expect:成功
drop table if exists t_subpartition_0151;
create table if not exists t_subpartition_0151
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0151
partition by list (col_1) subpartition by hash (col_2)
(
  partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 ),
  partition p_list_2 values(0,1,2,3,4,5,6,7,8,9),
  partition p_list_3 values(10,11,12,13,14,15,16,17,18,19),
  partition p_list_4 values(default ),
  partition p_list_5 values(20,21,22,23,24,25,26,27,28,29),
  partition p_list_6 values(30,31,32,33,34,35,36,37,38,39) tablespace ts_subpartition_0151_01
) enable row movement;
--step5: 查看分区信息; expect:成功
select relname, parttype, partstrategy, indisusable from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0151') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0151')) b where a.parentid = b.oid order by a.relname;

--step6: 清理环境; expect:成功
drop table if exists t_subpartition_0151;
drop tablespace if exists ts_subpartition_0151;
drop tablespace if exists ts_subpartition_0151_01;