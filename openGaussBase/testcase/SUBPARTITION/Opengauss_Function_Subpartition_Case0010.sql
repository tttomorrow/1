-- @testpoint: hash_range二级分区表基本功能测试：create/insert/updata/truncate/split,部分测试点合理报错

--step1: 创建hash_hash二级分区表; expect:成功
drop table if exists t_subpartition_0010 cascade;
create table t_subpartition_0010(hjid int,rjid int,jname varchar2)partition by hash (hjid) subpartition by range(rjid)
(
  partition hrp1(
    subpartition hrp1_1 values less than(36),
    subpartition hrp1_2 values less than(maxvalue)),
  partition hrp2(
    subpartition hrp2_1 values less than(36),
    subpartition hrp2_2 values less than(maxvalue)),
  partition hrp3(
    subpartition hrp3_1 values less than(36),
    subpartition hrp3_2 values less than(maxvalue)),
  partition hrp4(
    subpartition hrp4_1 values less than(36),
    subpartition hrp4_2 values less than(maxvalue))
);
--step2: 插入数据; expect:成功
insert into t_subpartition_0010(hjid,rjid,jname)values(1,1,'jade'),(1,2,'jade'),(2,8,'twojade'),(2,16,'twojade'),(2,26,'twojade'),(2,33,'twojade');
--step3: 查询所有数据; expect:成功
select * from t_subpartition_0010;
--step4: 根据一级分区key查询数据; expect:成功
select * from t_subpartition_0010 partition(hrp2);
--step5: 根据二级分区key; expect:成功
select * from t_subpartition_0010 subpartition(hrp2_2);
--step6: 根据一级分区key的值查询数据; expect:成功
select * from t_subpartition_0010 partition for(1);
--step7: 根据二级分区key的值查询数据; expect:成功
select * from t_subpartition_0010 subpartition for(1,16);
--step8: 使用聚合函数查询数据; expect:成功
select count(*) from t_subpartition_0010;
--step9: 使用聚合函数查询一级分区数据; expect:成功
select count(*) from t_subpartition_0010 partition(hrp2);
--step10: 使用聚合函数查询二级分区数据; expect:成功
select count(*) from t_subpartition_0010 subpartition(hrp2_2);
--step11: 使用正确的数据更新表数据; expect:成功
update t_subpartition_0010 set hjid =2  where jname= 'jade';
--step12: 使用错误的类型更新表数据; expect:合理报错
update t_subpartition_0010 set hjid ='a'  where jname= 'jade';
--step13: 删除指定行的数据; expect:成功
delete from t_subpartition_0010 where jname='jade';
--step14: 删除表中所有的行; expect:成功
delete from t_subpartition_0010;
--step15: 清理表一级分区的数据(无数据); expect:成功
alter table if exists t_subpartition_0010 truncate partition hrp1;
--step16: 清理表二级分区的数据(无数据); expect:成功
alter table if exists t_subpartition_0010 truncate subpartition hrp1_2;
--step17: 清理表一级分区的数据 ; expect:成功
alter table if exists t_subpartition_0010 truncate partition hrp2;
--step18: 清理表二级分区的数据; expect:成功
alter table if exists t_subpartition_0010 truncate subpartition hrp2_2;
--step19: 清理表数据 expect:成功
truncate t_subpartition_0010;
--step20: split拆分range二级分区; expect:成功
alter table if exists t_subpartition_0010 split subpartition hrp1_1 at(3) into(subpartition hrp1_1_01,subpartition hrp1_1_02);

--step21: 删除表; expect:成功
drop table if exists t_subpartition_0010 cascade;
