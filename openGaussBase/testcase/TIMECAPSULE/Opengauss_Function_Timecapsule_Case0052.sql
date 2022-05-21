-- @testpoint: 修改表结构后执行闪回,合理报错

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 如果表存在清除表且清除回收站; expect:表清除成功且回收站清除成功
drop table if exists t_timecapsule_0052 purge;
purge recyclebin;

--step4: 创建表且插入数据; expect:表创建成功且数据插入成功
create table t_timecapsule_0052 (col_1 varchar(255) null default '',col_2 clob default '');
insert into t_timecapsule_0052 values ('ddd',null);

--step5: 清空表; expect:表清空成功
truncate table t_timecapsule_0052;

--step6: 改变表结构; expect:改变成功
alter table t_timecapsule_0052 add col_3 varchar(255) default '';

--step7: 执行闪回; expect:闪回失败合理报错
timecapsule table t_timecapsule_0052 to before truncate;

--step8: 清理环境; expect:清理成功
drop table  if exists t_timecapsule_0052 purge;
purge recyclebin;

--step9: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;
