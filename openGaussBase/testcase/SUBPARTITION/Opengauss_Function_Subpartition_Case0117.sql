-- @testpoint: list_range二级分区表：执行算子

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0117;
drop tablespace if exists ts_subpartition_0117;
create tablespace ts_subpartition_0117 relative location 'subpartition_tablespace/subpartition_tablespace_0117';

--test1: 执行算子--seq scan
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0117
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0117
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
--step3: 插入数据; expect:成功
insert into t_subpartition_0117 values(0,0,0,0);
insert into t_subpartition_0117 values(-11,1,1,1),(-14,1,4,4),(-25,15,5,5),(-808,8,8,8),(-9,9,9,9);
insert into t_subpartition_0117 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0117 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step4: 查看执行计划; expect:成功,有seq scan执行算子
explain analyze select * from t_subpartition_0117;

--test2: 执行算子--index  scan
--step5: 二级分区键创建索引; expect:成功
drop index if exists i_subpartition_0117;
create index i_subpartition_0117 on t_subpartition_0117(col_2) local ;
--step6: 插入数据; expect:成功
insert into t_subpartition_0117 values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));
--step7: 查看执行计划; expect:成功,有index scan执行算子
explain analyze select * from t_subpartition_0117 where col_2 in
(select col_1 from t_subpartition_0117 subpartition(p_list_2_subpartdefault1) where col_1 >10);

--test3: 执行算子--bitmap index scan/bitmap heap scan
--step8: 查看执行计划; expect:成功,有bitmap heap scan执行算子
explain analyze select *  from t_subpartition_0117 where col_2 >500 and col_2 <8000 order by col_1;

--test4: 执行算子--支持plan hint调优
--step9: 查看执行计划; expect:成功,指定index scan
explain analyze select /*+ indexscan(t_subpartition_0117 index_01)*/ *  from t_subpartition_0117 where col_2 >500 and col_2 <8000 order by col_1;

--step10: 清理环境; expect:成功
drop index if exists i_subpartition_0060;
drop table if exists t_subpartition_0117;
drop tablespace if exists ts_subpartition_0117;