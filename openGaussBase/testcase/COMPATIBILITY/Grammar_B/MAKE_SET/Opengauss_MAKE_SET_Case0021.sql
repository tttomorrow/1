-- @testpoint:make_set在存储函数中的场景测试,部分用例合理报错
-- 清理环境;expect: 清理环境成功
drop function if exists f_Opengauss_MAKE_SET_Case0021_1;
-- 创建存储函数
create or replace function f_Opengauss_MAKE_SET_Case0021_1(num1 in text, total out text)
return text
as
begin
        total := make_set(num1,'t1','t2','t3','t4','t5','t6','t7','t8','t9','t10','t11','t12','t13','t14','t15','t16','t17','t18','t19','t20','t21','t22','t23','t24','t25','t26','t27','t28','t29','t30','t31','t32','t33','t34','t35','t36','t37','t38','t39','t40','t41','t42','t43','t44','t45','t46','t47','t48','t49','t50','t51','t52','t53','t54','t55','t56','t57','t58','t59','t60','t61','t62','t63','t64','t65','t66','t67','t68','t69','t70','t71','t72','t73','t74','t75','t76','t77','t78','t79','t80','t81','t82','t83','t84','t85','t86','t87','t88','t89','t90','t91','t92','t93','t94','t95','t96','t97','t98','t99','t100');
        return total;
end;
/
-- 执行存储函数
call f_Opengauss_MAKE_SET_Case0021_1(3,1);
call f_Opengauss_MAKE_SET_Case0021_1(null,1);
call f_Opengauss_MAKE_SET_Case0021_1(0111,1);
call f_Opengauss_MAKE_SET_Case0021_1('',1);
call f_Opengauss_MAKE_SET_Case0021_1(' ',1);
call f_Opengauss_MAKE_SET_Case0021_1(!,1);
call f_Opengauss_MAKE_SET_Case0021_1(我的,1);
call f_Opengauss_MAKE_SET_Case0021_1(,1);
call f_Opengauss_MAKE_SET_Case0021_1(3|1,1);
call f_Opengauss_MAKE_SET_Case0021_1(1+1,1);
call f_Opengauss_MAKE_SET_Case0021_1(a,1);
call f_Opengauss_MAKE_SET_Case0021_1(0,1);
call f_Opengauss_MAKE_SET_Case0021_1(2022-09-03,1);

-- 清理环境;expect: 清理环境成功
drop function if exists f_Opengauss_MAKE_SET_Case0021_1;
-- 创建存储函数
create or replace function f_Opengauss_MAKE_SET_Case0021_1(num1 in text, total out text)
return text
as
begin
        total := make_set(num1,'t1','','t3','',null,'t6','null',null,'t9','t10','t11','t12','t13','t14','t15','t16','t17','t18','t19','t20','t21','t22','t23','t24','t25','t26','t27','t28','t29','t30','t31','t32','t33','t34','t35','t36','t37','t38','t39','t40','t41','t42','t43','t44','t45','t46','t47','t48','t49','t50','t51','t52','t53','t54','t55','t56','t57','t58','t59','t60','t61','t62','t63','t64','t65','t66','t67','t68','t69','t70','t71','t72','t73','t74','t75','t76','t77','t78','t79','t80','t81','t82','t83','t84','t85','t86','t87','t88','t89','t90','t91','t92','t93','t94','t95','t96','t97','t98','t99','t100');
        return total;
end;
/
-- 执行存储函数
call f_Opengauss_MAKE_SET_Case0021_1(3,1);
call f_Opengauss_MAKE_SET_Case0021_1(null,1);
call f_Opengauss_MAKE_SET_Case0021_1(0111,1);
call f_Opengauss_MAKE_SET_Case0021_1('',1);
call f_Opengauss_MAKE_SET_Case0021_1(' ',1);
call f_Opengauss_MAKE_SET_Case0021_1(!,1);
call f_Opengauss_MAKE_SET_Case0021_1(我的,1);
call f_Opengauss_MAKE_SET_Case0021_1(,1);
call f_Opengauss_MAKE_SET_Case0021_1(3|1,1);
call f_Opengauss_MAKE_SET_Case0021_1(1+1,1);
call f_Opengauss_MAKE_SET_Case0021_1(a,1);
call f_Opengauss_MAKE_SET_Case0021_1(0,1);
call f_Opengauss_MAKE_SET_Case0021_1(2022-09-03,1);

-- 清理环境;expect: 清理环境成功
drop function if exists f_Opengauss_MAKE_SET_Case0021_1;
-- 创建存储函数
create or replace function f_Opengauss_MAKE_SET_Case0021_1(num1 in text, total out text)
return text
as
begin
        total := make_set(num1,false,true,'',1/8/1999,2022-09-03,'',null,'t6','null',null,'t9','t10','t11','t12','t13','t14','t15','t16','t17','t18','t19','t20','t21','t22','t23','t24','t25','t26','t27','t28','t29','t30','t31','t32','t33','t34','t35','t36','t37','t38','t39','t40','t41','t42','t43','t44','t45','t46','t47','t48','t49','t50','t51','t52','t53','t54','t55','t56','t57','t58','t59','t60','t61','t62','t63','t64','t65','t66','t67','t68','t69','t70','t71','t72','t73','t74','t75','t76','t77','t78','t79','t80','t81','t82','t83','t84','t85','t86','t87','t88','t89','t90','t91','t92','t93','t94','t95','t96','t97','t98','t99','t100');
        return total;
end;
/
-- 执行存储函数
call f_Opengauss_MAKE_SET_Case0021_1(3,1);
call f_Opengauss_MAKE_SET_Case0021_1(null,1);
call f_Opengauss_MAKE_SET_Case0021_1(0111,1);
call f_Opengauss_MAKE_SET_Case0021_1('',1);
call f_Opengauss_MAKE_SET_Case0021_1(' ',1);
call f_Opengauss_MAKE_SET_Case0021_1(!,1);
call f_Opengauss_MAKE_SET_Case0021_1(我的,1);
call f_Opengauss_MAKE_SET_Case0021_1(,1);
call f_Opengauss_MAKE_SET_Case0021_1(3|1,1);
call f_Opengauss_MAKE_SET_Case0021_1(1+1,1);
call f_Opengauss_MAKE_SET_Case0021_1(a,1);
call f_Opengauss_MAKE_SET_Case0021_1(0,1);
call f_Opengauss_MAKE_SET_Case0021_1(2022-09-03,1);

-- 清理环境;expect: 清理环境成功
drop function if exists f_Opengauss_MAKE_SET_Case0021_1;
-- 创建存储函数
create or replace function f_Opengauss_MAKE_SET_Case0021_1(num1 in text, total out text)
return text
as
begin
        total := make_set(num1,wd,我的我的,'',1/8/1999,2022-09-03,'',￥￥,'t6','null',null,'t9','t10','t11','t12','t13','t14','t15','t16','t17','t18','t19','t20','t21','t22','t23','t24','t25','t26','t27','t28','t29','t30','t31','t32','t33','t34','t35','t36','t37','t38','t39','t40','t41','t42','t43','t44','t45','t46','t47','t48','t49','t50','t51','t52','t53','t54','t55','t56','t57','t58','t59','t60','t61','t62','t63','t64','t65','t66','t67','t68','t69','t70','t71','t72','t73','t74','t75','t76','t77','t78','t79','t80','t81','t82','t83','t84','t85','t86','t87','t88','t89','t90','t91','t92','t93','t94','t95','t96','t97','t98','t99','t100');
        return total;
end;
/
-- 执行存储函数
call f_Opengauss_MAKE_SET_Case0021_1(3,1);
call f_Opengauss_MAKE_SET_Case0021_1(null,1);
call f_Opengauss_MAKE_SET_Case0021_1(0111,1);
call f_Opengauss_MAKE_SET_Case0021_1('',1);
call f_Opengauss_MAKE_SET_Case0021_1(' ',1);
call f_Opengauss_MAKE_SET_Case0021_1(!,1);
call f_Opengauss_MAKE_SET_Case0021_1(我的,1);
call f_Opengauss_MAKE_SET_Case0021_1(,1);
call f_Opengauss_MAKE_SET_Case0021_1(3|1,1);
call f_Opengauss_MAKE_SET_Case0021_1(1+1,1);
call f_Opengauss_MAKE_SET_Case0021_1(a,1);
call f_Opengauss_MAKE_SET_Case0021_1(0,1);
call f_Opengauss_MAKE_SET_Case0021_1(2022-09-03,1);
-- 清理环境;expect: 清理环境成功
drop function if exists f_Opengauss_MAKE_SET_Case0021_1;

