# from tvm.script import ir as I
# from tvm.script import tir as T
# from tvm.script import relax as R

@I.ir_module
class Module:
    @R.function
    def main(x: R.Tensor(("m", "n", "k"), dtype="int8")) -> R.Tensor(("m", "n", "k"), dtype="int8"):
        m = T.int64()
        n = T.int64()
        k = T.int64()
        gv: R.Tensor((m, n, k), dtype="int8") = R.tril(x, R.prim_value(-2))
        return gv