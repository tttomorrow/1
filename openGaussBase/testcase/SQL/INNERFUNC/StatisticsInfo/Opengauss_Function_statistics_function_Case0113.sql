-- @testpoint: pg_stat_get_db_numbackends(oid),处理该数据库活跃的服务器进程数目,入参为有效值时

----step1：入参为有效值 expect:成功
select pg_stat_get_db_numbackends(a.oid) from PG_DATABASE a where a.datname = 'postgres';

