-- @testpoint: 支持行存表创建行级访问策略
--step1: 创建行存表；expect:成功
DROP TABLE IF EXISTS t_security_RowLwvel_0008;
CREATE TABLE t_security_RowLwvel_0008(id int, role varchar(10), data varchar(10)) WITH (ORIENTATION = ROW);
--step2: 创建行级访问策略；expect:成功
ALTER TABLE t_security_RowLwvel_0008 ENABLE ROW LEVEL SECURITY;
CREATE ROW LEVEL SECURITY POLICY rls_security_RowLwvel_0008 ON t_security_RowLwvel_0008 USING(role = CURRENT_USER);
--step3: 清理环境；expect:成功
DROP TABLE t_security_RowLwvel_0008 CASCADE;