-- @testpoint: 验证uuid,varchar,numeric,date数据类型(合理)的应用

--step1:创建表和函数   expect:成功
drop table if exists t_postgis_0002 cascade;
drop function if exists uuid_generate_v4() cascade;

create or replace function uuid_generate_v4()
returns uuid
as
'select md5(random()::text || clock_timestamp()::text)::uuid;'
language sql;
/

create table t_postgis_0002 (
    id uuid default uuid_generate_v4() not null,
    ad_code character varying(5000),
    obj_code character varying(5000),
    obj_name character varying(5000),
    center_x numeric(11,8),
    center_y numeric(11,8),
    eng_type character varying(5000),
    cws_loc character varying(5000),
    wasu_rang character varying(1024),
    des_wasu_scal numeric(16,0),
    des_wasu_pop numeric(8,4),
    eng_stat character varying(5000),
    start_date date,
    comp_date date,
    ad_name character varying(5000),
    obj_source character varying(5000),
    prov_name character varying(5000),
    city_name character varying(5000),
    coun_name character varying(5000),
    prov_code character varying(5000),
    city_code character varying(5000),
    coun_code character varying(5000));

--step2:插入数据    expect:成功
insert into t_postgis_0002 values('954b6c34-4602-4c52-87d9-9a680d6d2941','7101','2012001','集中供水工程1','102.20509161544537','26.626168293153466','1','天津市','200平方公里','1000000','300.25','2',date '05-08-2010',date '10-31-2012','a区','规划文档','a','b','c','d','e','f');
insert into t_postgis_0002 values(default,'7101','2012001','集中供水工程2','102.20509','26.62616','2','北京市','500平方公里','1000000.23','300.25235','2',date '05-08-2010',date '10-31-2012','b区','规划文档','a','b','c','d','e','f');

--step3:查看数据   expect:成功
select * from t_postgis_0002;

--step4:清理环境   expect:成功
drop table t_postgis_0002;
drop function uuid_generate_v4;
