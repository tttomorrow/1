-- @testpoint: 更新时，使用offset列
drop table if exists zsharding_tbl;
create table zsharding_tbl(
c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
c_real real, c_double real,
c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
c_date date, c_datetime date, c_timestamp timestamp,
"offset" varchar(100) default 'offset'
)
PARTITION BY RANGE (c_integer)
(
partition P_20180121 values less than (0),
partition P_20190122 values less than (50000),
partition P_20200123 values less than (100000),
partition P_max values less than (maxvalue)
);

insert into zsharding_tbl(c_id,"offset") values(1,'wangsi');
update zsharding_tbl set "offset"=100;
--清理环境
drop table if exists zsharding_tbl;