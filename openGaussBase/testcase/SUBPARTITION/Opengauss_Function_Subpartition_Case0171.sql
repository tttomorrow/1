-- @testpoint: list_hash二级分区表：序列--分区列序列

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0171;
drop tablespace if exists ts_subpartition_0171;
create tablespace ts_subpartition_0171 relative location 'subpartition_tablespace/subpartition_tablespace_0171';

--test1: 序列--分区列序列
--step2: 创建二级分区表,声明分区键的类型为序列整型; expect:成功
create table if not exists t_subpartition_0171
(
    col_1 serial ,
    col_2 serial, 
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0171
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
--step3: 插入数据; expect:成功
insert into t_subpartition_0171(col_1,col_3,col_4) values(-1,1,1),(-3,1,4),(-15,5,5),(-12,8,8),(-43,9,9);
--step4: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0171 subpartition(p_hash_5_1);
--step5: 清空指定二级分区数据; expect:成功
alter table t_subpartition_0171 truncate subpartition p_hash_5_1;
--step6: 查询指定二级分区数据; expect:成功,无数据
select * from t_subpartition_0171 subpartition(p_hash_5_1);
--step7: 插入数据; expect:成功
insert into t_subpartition_0171(col_1,col_3,col_4) values(-1,1,1),(-3,1,4),(-15,5,5),(-12,8,8),(-43,9,9);
insert into t_subpartition_0171(col_2,col_3,col_4) values(-1,1,1),(-3,1,4),(-15,5,5),(-12,8,8),(-43,9,9);
--step8: 查询数据; expect:成功
select * from t_subpartition_0171;

--step9: 清理环境; expect:成功
drop table if exists t_subpartition_0171;
drop tablespace if exists ts_subpartition_0171;