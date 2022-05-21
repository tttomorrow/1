-- @testpoint: 测试存储过程中if判断条件为复杂逻辑运算

--创建存储过程
CREATE OR REPLACE PROCEDURE PROC_IF_ELSE_011
AS
begin
	begin
		if((NOT ((((TRue AND FAlse)) AND (TRue OR FAlse)))))
		then
			raise info 'The condition is true';
		else
			raise info 'The condition is false';
		end if;
	end;
	begin
		if(NOT(1+2+3+4+5=3*5)OR(99999999999999-1>99999999999999)OR( (1=0) AND false))
		then
			raise info 'The condition is true';
		else
			raise info 'The condition is false';
		end if;
	end;
end ;
/
--调用存储过程
Call PROC_IF_ELSE_011();

--清理环境
drop PROCEDURE PROC_IF_ELSE_011;