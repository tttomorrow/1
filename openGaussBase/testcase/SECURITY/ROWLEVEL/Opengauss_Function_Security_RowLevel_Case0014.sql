-- @testpoint: 不支持对视图定义行访问控制策略，合理报错
--step1: 创建视图；expect:成功
DROP VIEW IF EXISTS t_security_RowLwvel_0014;
CREATE VIEW t_security_RowLwvel_0014 AS SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
--step3: 创建行级访问策略；expect:失败
CREATE ROW LEVEL SECURITY POLICY rls_security_RowLwvel_0014 ON t_security_RowLwvel_0014 USING(role = CURRENT_USER);
--step4: 清理环境；expect:成功
DROP VIEW IF EXISTS t_security_RowLwvel_0014 CASCADE;