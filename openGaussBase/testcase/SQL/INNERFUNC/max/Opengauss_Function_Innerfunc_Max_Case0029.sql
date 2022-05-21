-- @testpoint: 函数调用max结合group by--cidr

--step1:创建表; expect:成功
drop table if exists t_max_case0029;
create table t_max_case0029(id int, i cidr);

--step2:创建函数; expect:成功
create or replace function f_max_case0029(out max_id int, out max_c cidr)
returns setof record
as $$
begin
return query select id as max_id, max(i)::cidr as max_c from t_max_case0029 group by id order by id;
end;
$$language plpgsql;/

--step3:调用函数; expect:空
select f_max_case0029();

--step4:插入空值; expect:空 ::
insert into t_max_case0029 values(1, NULL);
select f_max_case0029();
insert into t_max_case0029 values(1, '::');
select f_max_case0029();

--step5:插入数据; expect:(1,::ffff) (2,::255.255.0.0/120)
insert into t_max_case0029 values(1, '::ffff/128'),(2, '::ffff:0/120');
select f_max_case0029();

--tearDown
drop function f_max_case0029;
drop table if exists t_max_case0029;

