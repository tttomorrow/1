-- @testpoint: range_list二级分区表：分区名称为普通字符串/特殊字符串,部分测试点合理报错

--test1: 分区名称-普通字符串
--step1: 创建二级分区表,分区名称为普通字符串; expect:成功
drop table if exists t_subpartition_0201;
drop tablespace if exists ts_subpartition_0201;
drop tablespace if exists ts_subpartition_0201_01;
create tablespace ts_subpartition_0201 relative location 'subpartition_tablespace/subpartition_tablespace_0201';
create tablespace ts_subpartition_0201_01 relative location 'subpartition_tablespace/subpartition_tablespace_0201_01';
create   table if not exists t_subpartition_0201
(
    col_1 int primary key   using index tablespace ts_subpartition_0201_01,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0201
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition aavvvddcs values ( '1','2','3','4','5'),
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
--step2: 查询分区表空间; expect:成功
select p.relname, t.spcname from pg_partition p, pg_tablespace t
where p.reltablespace=t.oid and p.relname='aavvvddcs';
--step3: 查看分区信息; expect:成功
select relname, parttype, partstrategy, boundaries from pg_partition where partstrategy !='n' and parentid = (select oid from pg_class where relname = 't_subpartition_0201') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0201')) b where a.parentid = b.oid order by a.relname;
	
--test2: 分区名称-包含特殊字符
--step4: 创建二级分区表,分区名称包含特殊字符; expect:成功
drop table if exists t_subpartition_0201;
create   table if not exists t_subpartition_0201
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0201
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_list_1_1 values ( '1','2','3','4','5'),
    subpartition "''" values ( default )
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
--step5: 查看分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0201') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0201')) b where a.parentid = b.oid order by a.relname;
--step6: 插入数据; expect:成功
insert into t_subpartition_0201 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step7: 查询分区名包含特殊字符的分区数据; expect:成功
select * from t_subpartition_0201 subpartition("''");
--step8: 查询普通一级分区数据; expect:成功
select * from t_subpartition_0201 partition(p_range_1);
--step9: 查询普通二级分区数据; expect:成功
select * from t_subpartition_0201 subpartition(p_list_1_1);
--step10: 查询不存在的二级分区数据; expect:合理报错
select * from t_subpartition_0201 subpartition(p_range_1_2);
--step11: 使用聚合函数查询一级分区数据; expect:成功
select max(col_4) from t_subpartition_0201 partition(p_range_2);
--step12: 使用聚合函数查询二级分区数据; expect:成功
select count(*) from t_subpartition_0201 subpartition(p_list_2_1);
--step13: 查询二级分区的二级分区键数据; expect:成功
select col_2 from t_subpartition_0201 subpartition(p_list_2_1);

--step14: 清理环境; expect:成功
drop table if exists t_subpartition_0201;
drop tablespace if exists ts_subpartition_0201;
drop tablespace if exists ts_subpartition_0201_01;