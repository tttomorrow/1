-- @testpoint: insert语句绑定blob类型的参数

--创建测试表
drop table if exists all_datatype_tbl;
create table all_datatype_tbl(
	c_id integer,
	c_boolean boolean,
	c_integer integer, c_bigint bigint,
	c_real real,
	c_decimal decimal(38), c_number number(38),
	c_char char(50) default null, c_varchar varchar(50), c_clob clob,
    c_blob blob,
	 c_timestamp timestamp, c_interval interval day to second);

--创建存储过程
create or replace procedure pro_014()
as
    sqlstat varchar(500);
	v1 blob;
begin
    v1 := '10101111111111';
    sqlstat := 'insert into all_datatype_tbl(c_blob) select :p1 ';
    execute immediate sqlstat using v1;
end;
/
--调用存储过程
call pro_014();

--查看表数据
select c_blob from all_datatype_tbl;

--清理环境
drop procedure pro_014;