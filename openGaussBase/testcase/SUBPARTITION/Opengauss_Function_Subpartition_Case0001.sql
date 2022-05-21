-- @testpoint: hash_hash二级分区表基本功能测试：create/insert/updata/truncate/split,部分测试点合理报错

--step1: 创建hash_hash二级分区表; expect:成功
drop table if exists t_subpartition_0001 cascade;
create table  t_subpartition_0001(hjid int,rjid int,jname varchar2)partition by hash (hjid) subpartition by hash(rjid)
(
  partition hhp1(
    subpartition hhp1_1,
    subpartition hhp1_2),
  partition hhp2(
    subpartition hhp2_1,
    subpartition hhp2_2),
  partition hhp3(
    subpartition hhp3_1,
    subpartition hhp3_2),
  partition hhp4(
    subpartition hhp4_1,
    subpartition hhp4_2)
);
--step2: 插入数据; expect:成功
insert into  t_subpartition_0001(hjid,rjid,jname)values(1,1,'jade'),(2,8,'twojade'),(2,16,'twojade'),(3,36,'twojade');
--step3: 查询所有数据; expect:成功
select * from  t_subpartition_0001;
--step4: 根据一级分区key查询数据; expect:成功
select * from  t_subpartition_0001 partition(hhp2);
--step5: 根据二级分区key; expect:成功
select * from  t_subpartition_0001 subpartition(hhp2_2);
--step6: 根据一级分区key的值查询数据; expect:成功
select * from  t_subpartition_0001 partition for(1);
--step7: 根据二级分区key的值查询数据; expect:成功
select * from  t_subpartition_0001 subpartition for(1,16);
--step8: 使用聚合函数查询数据; expect:成功
select count(*) from  t_subpartition_0001;
--step9: 使用聚合函数查询一级分区数据; expect:成功
select count(*) from  t_subpartition_0001 partition(hhp2);
--step10: 使用聚合函数查询二级分区数据; expect:成功
select count(*) from  t_subpartition_0001 subpartition(hhp2_2);
--step11: 使用正确的数据更新表数据; expect:成功
update  t_subpartition_0001 set hjid =2  where jname= 'jade';
--step12: 使用错误的类型更新表数据; expect:合理报错
update  t_subpartition_0001 set hjid ='a'  where jname= 'jade';
--step13: 删除指定行的数据; expect:成功
delete from  t_subpartition_0001 where jname='jade';
--step14: 删除表中所有的行; expect:成功
delete from  t_subpartition_0001;
--step15: 清理表一级分区的数据(无数据); expect:成功
alter table if exists  t_subpartition_0001 truncate partition hhp1;
--step16: 清理表二级分区的数据(无数据); expect:成功
alter table if exists  t_subpartition_0001 truncate subpartition hhp1_2;
--step17: 清理表一级分区的数据 ; expect:成功
alter table if exists  t_subpartition_0001 truncate partition hhp2;
--step18: 清理表二级分区的数据; expect:成功
alter table if exists  t_subpartition_0001 truncate subpartition hhp2_2;
--step19: 清理表数据 expect:成功
truncate  t_subpartition_0001;
--step20: split拆分hash二级分区; expect:合理报错
alter table if exists  t_subpartition_0001 split subpartition hhp1_1 at(8) into(subpartition hhp1_01,subpartition hhp1_02);

--step21: 删除表; expect:成功
drop table if exists t_subpartition_0001 cascade;
