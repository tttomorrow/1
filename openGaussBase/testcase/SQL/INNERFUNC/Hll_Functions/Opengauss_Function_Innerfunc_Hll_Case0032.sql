-- @testpoint: hll_hashval_ne(hll_hashval, hll_hashval),当入参为非hll_hashval类型时，合理报错

select hll_hashval_ne(hll_hash_integer(1),basicemailmasking('abcd@gmail.com'));
select hll_hashval_ne('avbshsk',-8604791237420463362);