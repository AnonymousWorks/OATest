# from tvm.script import ir as I
# from tvm.script import tir as T
# from tvm.script import relax as R

@I.ir_module
class Module:
    @R.function
    def main(x: R.Tensor(("a", "b", "c", "d"), dtype="float32")) -> R.Tensor((1, 1, 1, 1), dtype="int64"):
        a = T.int64()
        b = T.int64()
        c = T.int64()
        d = T.int64()
        gv: R.Tensor((1, 1, 1, 1), dtype="int64") = R.argmin(x, axis=None, keepdims=True)
        return gv