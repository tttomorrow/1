-- @testpoint: 测试select into语句中带有复杂数学表达式时给int数据类型赋值

declare
  v_int int;
begin
    select 2.147483647e9-0.7483647e7+7*10e5+483600+(10*10-53)+1-1 into v_int from sys_dummy;
    raise info 'result:% ',v_int;
end;
/
