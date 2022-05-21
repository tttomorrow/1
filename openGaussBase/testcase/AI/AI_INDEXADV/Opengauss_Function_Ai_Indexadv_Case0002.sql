-- @testpoint: 大数据量查询索引推荐

--test1:大数据量查询索引推荐
--step1:建表1;expect:建表1成功
drop table if exists t_table_ai_indexadv_0002 cascade;
create table t_table_ai_indexadv_0002 (col_int int,col_numeric numeric,
col_float float,col_char char(10),col_text text,col_time time);

--step2:建存储过程;expect:建存储过程成功
create or replace procedure p_procedure_insert_0002 (a int) is
V_int int;
V_numeric numeric;
V_float float;
V_char char(10);
V_text text;
V_time time;
begin
for i in 1..a
loop
V_int :=i;
V_numeric :=i+1.11;
V_float :=i*5.55;
V_char :='x_'|| i;
V_text :='V_text_'|| i;
V_time :='19:41:20';
execute immediate 'insert into t_table_ai_indexadv_0002 values
(:p1,:p2,:p3,:p4,:p5,:p6)
'using V_int,V_numeric,V_float,V_char,V_text,V_time;
end loop;
end;
/

--step3:向表中插入100000条数据并统计数据的数量;expec:向表中插入数据成功,返回表数据的数量;
call p_procedure_insert_0002(100000);
select count(*) from t_table_ai_indexadv_0002;

--step4:查询单索引推荐;expect:返回推荐的索引列为空
select * from gs_index_advise('select * from t_table_ai_indexadv_0002;');

--step5:清理环境;expect:清理环境成功
drop table t_table_ai_indexadv_0002;
drop procedure p_procedure_insert_0002;