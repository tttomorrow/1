-- @testpoint: 类型转换函数，to_char将浮点类型的值转换为指定格式的字符串(double precision/real, text)

-- real 整数位>=6按整数位来
select to_char(123456.12345678::real, '999999d9999999999');
select to_char(1234567.12345678::real, '9999999d9999999999');

-- real 整数位<6，有效数字6位，多余部分四舍五入
select to_char(12345.12345678::real, '99999d9999999999');
select to_char(12.12345678::real, '999d9999999999');
select to_char(2.12345678::real, '999d9999999999');
select to_char(0.12345678::real, '999d9999999999');

-- real 模式串短，显示#
select to_char(1234567.12345678::real, '0000d00');
select to_char(1234567.12345678::real, '99d9999999999');

-- real 模式串长，9补空格，0补0
select to_char(7.12345678::real, '0000000d00');
select to_char(1234567.12345678::real, '9999999999d9999999999');


-- double 整数位>=15按整数位来
select to_char(123456789123456.12345678::double precision, '9999999999999999d9999999999');
select to_char(1234567891234567.12345678::double precision, '9999999999999999d9999999999');

-- double 整数位<15，有效数字15位，多余部分四舍五入
select to_char(12345678912345.12345678::double precision, '9999999999999999d9999999999');
select to_char(1234567891234.12345678::double precision, '9999999999999999d9999999999');
select to_char(1234567891234.129::double precision, '9999999999999999d9999999999');

-- double 模式串长，9在前补空格在后补0，0补0
select to_char(2.12345678::double precision, '999d9999999999999999');
select to_char(0.12345678::double precision, '999d9999999999999999');


-- clob转换为varchar
select char_length(to_char(lpad('abccc',1024*1024*11,'x')::clob));

-- varchar2转换为varchar
select char_length(to_char(lpad('abccc',1024*1024*11,'x')::varchar2(10485760)));