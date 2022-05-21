-- @testpoint: 测试select into语句中给int数据类型赋值，测试real隐式转换为bigint 合理报错

declare
   v_real real;
   v_bigint bigint;
begin
    v_real:=9223372036854775800.7898765;
    select v_real into v_bigint from sys_dummy;
    raise info 'result:% ',v_bigint;
end;
/