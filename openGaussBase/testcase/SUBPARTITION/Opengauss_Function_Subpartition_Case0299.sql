-- @testpoint: range_range二级分区表：analyze/vacuum

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0299;
drop tablespace if exists ts_subpartition_0299;
create tablespace ts_subpartition_0299 relative location 'subpartition_tablespace/subpartition_tablespace_0299';
--test1: analyze--收集分区表的统计信息。
--step2: 创建二级分区表; expect:成功
create table t_subpartition_0299
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 50 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 80 )
  (
    subpartition p_range_2_1 values less than( 50 ),
    subpartition p_range_2_2 values less than( maxvalue )
  )
);
--step3: 插入数据; expect:成功
insert into  t_subpartition_0299 values (generate_series(0, 79),generate_series(0, 79),generate_series(0, 79));
--step4: 收集指定分区的统计信息; expect:成功,只支持语法,不收集统计信息
analyze t_subpartition_0299 partition(p_range_2);
select pg_sleep(2);
--step5: 查询pg_statistic数据; expect:成功,0条数据
select starelkind,stainherit from pg_statistic where starelid=(select oid from pg_class where relname='t_subpartition_0299');
--step6: 查询pg_stats数据; expect:成功,0条数据
select tablename,attname from pg_stats  where tablename='t_subpartition_0299';

--test2: analyze--收集多列统计信息(包含分区列)
--step7: 收集2个分区列统计信息; expect:成功
analyze t_subpartition_0299 (col_1,col_2);
select pg_sleep(2);
--step8: 查询pg_statistic数据; expect:成功,2条数据
select starelkind,stainherit from pg_statistic where starelid=(select oid from pg_class where relname='t_subpartition_0299');
--step9: 查询pg_stats数据; expect:成功,2条数据
select tablename,attname from pg_stats  where tablename='t_subpartition_0299';
--step10: 查询pg_stat_all_tables数据; expect:成功
select schemaname,relname,analyze_count from pg_stat_all_tables where relname='t_subpartition_0299';

--test3: analyze--收集多列统计信息(不包含分区列)
--step11: 收集2个普通列统计信息; expect:成功
analyze t_subpartition_0299 (col_3,col_4);
select pg_sleep(2);
--step12: 查询pg_statistic数据; expect:成功,4条数据
select starelkind,stainherit from pg_statistic where starelid=(select oid from pg_class where relname='t_subpartition_0299');
--step13: 查询pg_stats数据; expect:成功,4条数据
select tablename,attname from pg_stats  where tablename='t_subpartition_0299';
--step14: 查询pg_stat_all_tables数据; expect:成功
select schemaname,relname,analyze_count from pg_stat_all_tables where relname='t_subpartition_0299';

--test4: analyze--检测表数据文件
--step15: 检测表数据文件; expect:成功
analyze  verify fast;
analyze  verify complete;

--test5: analyze--检测表和索引的数据文件
--step16: 二级分区键创建唯一索引; expect:成功
drop index if exists i_subpartition_0299;
create index i_subpartition_0299 on t_subpartition_0299(col_2);
--step17: 检测表和索引的数据文件; expect:成功
analyze verify fast t_subpartition_0299 ;
analyse verify complete t_subpartition_0299 cascade;

--test6: analyze--检测表分区的数据文件
--step18: 检测表分区的数据文件; expect:成功
analyze  verify fast t_subpartition_0299 partition (p_range_1);
analyze  verify complete t_subpartition_0299 partition (p_range_2) cascade;

--test7: vacuum--仅回收空间,不更新统计信息
--step19: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0299 cascade;
create table t_subpartition_0299
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0299
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 50 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 80 )
  (
    subpartition p_range_2_1 values less than( 50 ),
    subpartition p_range_2_2 values less than( maxvalue )
  )
);
--step20: 插入数据; expect:成功
insert into  t_subpartition_0299 values (generate_series(0, 79),generate_series(0, 79),generate_series(0, 79));
--step21: vacuum回收空间; expect:成功
vacuum  full freeze  verbose  t_subpartition_0299 partition(p_range_2);
select pg_sleep(2);
--step22: 查询pg_stat_all_tables数据; expect:成功,vacuum信息没更新
select schemaname,relname,vacuum_count from pg_stat_all_tables where relname='t_subpartition_0299';

--test8: vacuum--回收空间并更新统计信息,对关键字顺序无要求
--step23: vacuum回收空间; expect:成功
vacuum  full freeze  verbose analyze t_subpartition_0299 partition(p_range_2);

--test9: vacuum--回收空间并更新统计信息,且对关键字顺序有要求。
--step24: vacuum回收空间; expect:成功
vacuum   freeze  verbose analyze verbose t_subpartition_0299 partition(p_range_2);

--step25: 清理环境; expect:成功
drop table if exists t_subpartition_0299;
drop tablespace if exists ts_subpartition_0299;