-- @testpoint: reset_unique_sql(text, text, bigint),入参为有效值

----step1：入参为有效值; expect:成功
select reset_unique_sql('global','all',1);
select reset_unique_sql('local','all',1);
select reset_unique_sql('local','by_userid',1);
select reset_unique_sql('local','by_cnid',1);
select reset_unique_sql('global','all','');
