-- @testpoint: 测试物化视图对各种数据类型的支持情况

--数据类型
drop table if exists student cascade;
drop procedure if exists insert_student;
create table student
(
    col_tinyint tinyint not null default '3',
    col_smallint smallint not null default '7',
    col_integer integer,
    col_int int,
    col_binary_integer binary_integer,
    col_bigint bigint primary key,
    col_numeric numeric,
    col_numeric1 numeric(38),
    col_numeric2 numeric(38,7),
    col_decimal decimal,
    col_decimal1 decimal(38),
    col_decimal2 decimal(38,7),
    col_number1 number,
    col_number2 number(38),
    col_number5 number(38,7),
    col_real real,
    col_float4 float4,
    col_double_precision double precision,
    col_float8 float8,
    col_float float,
    col_float1 float(38),
    col_binary_double binary_double,
    col_dec dec,
    col_dec1 dec(38),
    col_dec2 dec(38,7),
    col_integer1 integer(38),
    col_integer2 integer(38,7),
    col_money money,
    col_boolean boolean,
    col_char char,
    col_char1 char(200),
    col_character character,
    col_character1 character(200),
    col_nchar nchar,
    col_nchar1 nchar(200),
    col_varchar varchar(200),
    col_character_varying character varying(200),
    col_varchar2 varchar2(200) default 'aaaabbbb',
    col_narchar2 nvarchar2(200) not null default 'aaaabbbb',
    col_clob clob,
    col_text text,
    col_name1 name,
    col_char2 "char",
    col_blob blob,
    col_raw raw,
    col_bytea bytea,
    col_date date not null default '2018-01-07 08:08:08',
    col_time time,
    col_time1 time(6),
    col_time2 time without time zone,
    col_time3 time(6) without time zone,
    col_time4 time with time zone,
    col_time5 time(6) with time zone,
    col_timestamp timestamp,
    col_timestamp1 timestamp(6),
    col_timestamp2 timestamp without time zone,
    col_timestamp3 timestamp(6) without time zone,
    col_timestamp4 timestamp with time zone,
    col_timestamp5 timestamp(6) with time zone,
    col_smalldatetime smalldatetime,
    col_interval interval day (1) to second (6),
    col_interval1 interval,
    col_interval2 interval year,
    col_interval3 interval second (6),
    col_interval4 interval hour to second (6),
    col_cidr cidr,
    col_inet inet,
    col_macaddr macaddr,
    col_bitn bit(10),
    col_bit_varying bit varying(10)
);

create or replace procedure insert_student() is
V_tinyint tinyint;
V_smallint smallint;
V_integer integer;
V_int int;
V_binary_integer binary_integer;
V_bigint bigint;
V_numeric numeric;
V_numeric1 numeric(38);
V_numeric2 numeric(38,7);
V_decimal decimal;
V_decimal1 decimal(38);
V_decimal2 decimal(38,7);
V_number1 number;
V_number2 number(38);
V_number5 number(38,7);
V_real real;
V_float4 float4;
V_double_precision double precision;
V_float8 float8;
V_float float;
V_float1 float(38);
V_binary_double binary_double;
V_dec dec;
V_dec1 dec(38);
V_dec2 dec(38,7);
V_integer1 integer(38);
V_integer2 integer(38,7);
V_money money;
V_boolean boolean;
V_char char;
V_char1 char(200);
V_character character;
V_character1 character(200);
V_nchar nchar;
V_nchar1 nchar(200);
V_varchar varchar(200);
V_character_varying character varying(200);
V_varchar2 varchar2(200);
V_narchar2 nvarchar2(200);
V_clob clob;
V_text text;
V_name1 name;
V_char2 "char";
V_blob blob;
V_raw raw;
V_bytea bytea;
V_date date;
V_time time;
V_time1 time(6);
V_time2 time without time zone;
V_time3 time(6) without time zone;
V_time4 time with time zone;
V_time5 time(6) with time zone;
V_timestamp timestamp;
V_timestamp1 timestamp(6);
V_timestamp2 timestamp without time zone;
V_timestamp3 timestamp(6) without time zone;
V_timestamp4 timestamp with time zone;
V_timestamp5 timestamp(6) with time zone;
V_smalldatetime smalldatetime;
V_interval interval day (1) to second (6);
V_interval1 interval;
V_interval2 interval year;
V_interval3 interval second (6);
V_interval4 interval hour to second (6);
V_cidr cidr;
V_inet inet;
V_macaddr macaddr;
V_bitn bit(10);
V_bit_varying bit varying(10);
begin                                         
for i in 1..1000
loop
V_tinyint :=mod(i,256);
V_smallint :=i+1;
V_integer :=i+2;
V_int :=i+3;
V_binary_integer :=i+4;
V_bigint :=i+5;
V_numeric :=i+1.11;
V_numeric1 :=i+2.22;
V_numeric2 :=i+3.333;
V_decimal :=i+4.44;
V_decimal1 :=i+5.55;
V_decimal2 :=i+6.666;
V_number1 :=i+7.77;
V_number2 :=i+8.88;
V_number5 :=i+9.999;
V_real :=i*1.11;
V_float4 :=i*2.22;
V_double_precision :=i*3.33;
V_float8 :=i*4.44;
V_float :=i*5.55;
V_float1 :=i*6.66;
V_binary_double :=i*7.77;
V_dec :=i*8.88;
V_dec1 :=i*9.99;
V_dec2 :=i*1.11;
V_integer1 :=i*2.22;
V_integer2 :=i*3.33;
V_money :=i*2;
V_boolean :='t';
V_char :='x';
V_char1 :='wxwhlayyawajbcqzhrctszhddqrwkyzjdwbygz';
V_character :='f';
V_character1 :='V_character1';
V_nchar :='w';
V_nchar1 :='V_nchar1';
V_varchar :='V_varchar';
V_character_varying :='V_character_varying';
V_varchar2 :='V_varchar2';
V_narchar2 :='V_narchar2';
V_clob :='V_clob';
V_text :='V_text';
V_name1 :='wxwhlayyawajbcqzhrctszhddqrwkyzjdwbygz';
V_char2 :='m';
V_blob :='110101010101';
V_raw :='110101010101';
V_bytea :='110101010101';
V_date :='1999-01-08';
V_time :='19:41:20';
V_time1 :='20:41:40';
V_time2 :='21:21:21 pst';
V_time3 :='22:22:22';
V_time4 :='21:21:21 pst';
V_time5 :='22:22:22';
V_timestamp :='2020-4-22';
V_timestamp1 :='2020-4-22 pst';
V_timestamp2 :='2020-4-22 21:22:23';
V_timestamp3 :='2020-4-22 21:22:23.333333';
V_timestamp4 :='2020-4-22 pst';
V_timestamp5 :='2020-4-22 pst';
V_smalldatetime :='2020-4-22 21:22:23';
V_interval :=INTERVAL '1' DAY;
V_interval1 :=INTERVAL '1' DAY;
V_interval2 :=INTERVAL '1' year;
V_interval3 :=INTERVAL '2333' second;
V_interval4 :=INTERVAL '5:23:35.5555' hour to second;
V_cidr :='192.168.100.128/25';
V_inet :='10.244.56.202';
V_macaddr :='08:00:2b:01:02:03';
V_bitn :=B'1011011011';
V_bit_varying :=B'111100';
execute immediate 'insert into student values
(:p1,:p2,:p3,:p4,:p5,:p6,:p7,:p8,:p9,:p10,:p11,:p12,:p13,:p14,:p15,:p16,:p17,:p18,:p19,:p20,:p21,:p22,:p23,:p24,:p25,:p26,:p27,:p28,:p29,:p30,:p31,:p32,:p33,:p34,:p35,:p36,:p37,:p38,:p39,:p40,:p41,:p42,:p43,:p44,:p45,:p46,:p47,:p48,:p49,:p50,:p51,:p52,:p53,:p54,:p55,:p56,:p57,:p58,:p59,:p60,:p61,:p62,:p63,:p64,:p65,:p66,:p67,:p68,:p69,:p70)
'using V_tinyint,V_smallint,V_integer,V_int,V_binary_integer,V_bigint,V_numeric,V_numeric1,V_numeric2,V_decimal,V_decimal1,V_decimal2,V_number1,V_number2,V_number5,V_real,V_float4,V_double_precision,V_float8,V_float,V_float1,V_binary_double,V_dec,V_dec1,V_dec2,V_integer1,V_integer2,V_money,V_boolean,V_char,V_char1,V_character,V_character1,V_nchar,V_nchar1,V_varchar,V_character_varying,V_varchar2,V_narchar2,V_clob,V_text,V_name1,V_char2,V_blob,V_raw,V_bytea,V_date,V_time,V_time1,V_time2,V_time3,V_time4,V_time5,V_timestamp,V_timestamp1,V_timestamp2,V_timestamp3,V_timestamp4,V_timestamp5,V_smalldatetime,V_interval,V_interval1,V_interval2,V_interval3,V_interval4,V_cidr,V_inet,V_macaddr,V_bitn,V_bit_varying;
end loop;
end;
/

create materialized view student_mv as table student;
call insert_student();
refresh materialized view student_mv;
select count(*) from student_mv;
drop table student cascade;
drop procedure insert_student;