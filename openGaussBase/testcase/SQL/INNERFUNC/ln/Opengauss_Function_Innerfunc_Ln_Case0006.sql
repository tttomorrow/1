-- @testpoint: 自然对数lnx输入为比较表达式
select ln(2<3) as result;
select ln(2!=3) as result;
select ln(2<>3) as result;