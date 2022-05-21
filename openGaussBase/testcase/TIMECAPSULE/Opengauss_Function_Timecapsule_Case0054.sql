-- @testpoint: 不支持对回收站对象执行DML操作insert,合理报错

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 如果表存在清除表且清除回收站; expect:表清除成功且回收站清除成功
drop table if exists t_timecapsule_0054 purge;
purge recyclebin;

--step4: 创建函数; expect:函数创建成功
CREATE OR REPLACE FUNCTION f_timecapsule_0054_01(varchar, char, int8)
  RETURNS varchar
  LANGUAGE plpgsql
AS
$BODY$
declare
  ret varchar;
begin
  ret = (select t.rcyname from gs_recyclebin t where t.rcyoriginname = $1 and t.rcyoperation=$2 order by t.rcychangecsn asc offset ($3 -1 ) limit 1);
  return ret;
end;
$BODY$;
/
CREATE OR REPLACE FUNCTION f_timecapsule_0054_02(varchar)
  RETURNS varchar
  LANGUAGE plpgsql
AS
$BODY$
declare
  sqlText text;
begin
  sqlText = 'insert into "' || $1 ||'" values (1,1)';
  execute sqlText;
  return 0;
end;
$BODY$;
/
--step5: 创建表; expect:表创建成功
create table t_timecapsule_0054(a int, b int);

--step6: 删除表; expect:表删除成功
drop table t_timecapsule_0054;

--step7: 调用函数向表中插入数据; expect:插入失败合理报错
select f_timecapsule_0054_02(f_timecapsule_0054_01('t_timecapsule_0054', 'd', 1));

--step8: 清理环境; expect:清理成功
drop table  if exists t_timecapsule_0054 purge;
drop function if exists f_timecapsule_0054_01();
drop function if exists f_timecapsule_0054_02();

--step9: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;