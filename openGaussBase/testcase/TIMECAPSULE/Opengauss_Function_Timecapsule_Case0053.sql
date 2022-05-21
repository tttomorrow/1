-- @testpoint: vacuum full表后执行闪回

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 如果表存在清除表且清除回收站; expect:表清除成功且回收站清除成功
drop table if exists t_timecapsule_0053 purge;
purge recyclebin;

--step4: 创建表且插入数据; expect:表创建成功且数据插入成功
create table t_timecapsule_0053
(
   stuno     int,
   classno   int
);
insert into t_timecapsule_0053 values(1,1);
insert into t_timecapsule_0053 values(2,2);
insert into t_timecapsule_0053 values(3,3);

--step5: 更新表数据后再次插入数据; expect:表数据更新成功且数据插入成功
update t_timecapsule_0053 set classno = classno*2;
update t_timecapsule_0053 set classno = classno*2;
update t_timecapsule_0053 set classno = classno*2;
insert into t_timecapsule_0053 values(1,1);
insert into t_timecapsule_0053 values(2,2);
insert into t_timecapsule_0053 values(3,3);

--step6: 清空表数据后再次插入数据; expect:清数据清空成功且数据插入成功
delete from t_timecapsule_0053 where stuno = 1;
delete from t_timecapsule_0053 where stuno = 2;
delete from t_timecapsule_0053 where stuno = 3;
insert into t_timecapsule_0053 values(1,1);
insert into t_timecapsule_0053 values(2,2);
insert into t_timecapsule_0053 values(3,3);

--step7: 更新表数据; expect:表数据更新成功
update t_timecapsule_0053 set classno = classno*2;

--step8: 对表进行清理; expect:表清理成功
vacuum full t_timecapsule_0053;

--step9: 查询表数据; expect:表数据查询成功
select * from t_timecapsule_0053;

--step10: 删除表; expect:表删除成功
drop table  t_timecapsule_0053;

--step11: 执行drop闪回; expect:闪回成功
timecapsule table t_timecapsule_0053 to before drop;

--step12: 查询闪回后的表; expect:查询结果与预期结果一致
select * from t_timecapsule_0053;

--step13: 清理环境; expect:清理成功
drop table  if exists t_timecapsule_0053;
purge recyclebin;

--step14: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;