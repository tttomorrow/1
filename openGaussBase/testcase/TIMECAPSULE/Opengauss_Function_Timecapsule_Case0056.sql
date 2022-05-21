-- @testpoint: 不支持对回收站对象执行DML操作MERGE INTO,合理报错

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 如果表存在清除表且清除回收站; expect:表清除成功且回收站清除成功
drop table if exists t_timecapsule_0056_01;
drop table if exists t_timecapsule_0056_02;
purge recyclebin;

--step4: 创建函数; expect:函数创建成功
create or replace function f_timecapsule_0056_01(varchar, char, int8)
  returns varchar
  language plpgsql
as
$body$
declare
  ret varchar;
begin
  ret = (select t.rcyname from gs_recyclebin t where t.rcyoriginname = $1 and t.rcyoperation=$2 order by t.rcychangecsn asc offset ($3 -1 ) limit 1);
  return ret;
end;
$body$;
/
create or replace function f_timecapsule_0056_02(varchar)
  returns varchar
  language plpgsql
as
$body$
declare
  sqltext text;
begin
  sqltext = 'merge into "' || $1 ||'" np
using products p
on (np.product_id = p.product_id )
when matched then
  update set np.product_name = p.product_name, np.category = p.category
when not matched then
  insert values (p.product_id, p.product_name, p.category)';
  execute sqltext;
  return 0;
end;
$body$;
/
--step5: 创建表且插入数据; expect:表创建成功且数据插入成功
drop table if exists t_timecapsule_0056_01;
create table t_timecapsule_0056_01
( product_id integer,
  product_name varchar2(60),
  category varchar2(60) );
insert into t_timecapsule_0056_01 values
(1502, 'olympus camera', 'electrncs'),
(1601, 'lamaze', 'toys'),
(1666, 'harry potter', 'toys'),
(1700, 'wait interface', 'books');
drop table if exists t_timecapsule_0056_02;
create table t_timecapsule_0056_02
( product_id integer,
  product_name varchar2(60),
  category varchar2(60)
);

--step6: 删除表; expect:表删除成功
drop table t_timecapsule_0056_02;

--step7: 调用函数关联表数据; expect:关联失败合理报错
select f_timecapsule_0056_02(f_timecapsule_0056_01('t_timecapsule_0056_02', 'd', 1));

--step8: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0056_02 purge;
drop table if exists t_timecapsule_0056_01 purge;
drop function if exists f_timecapsule_0056_01();
drop function if exists f_timecapsule_0056_02();
purge recyclebin;

--step9: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;