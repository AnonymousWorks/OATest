# from tvm.script import ir as I
# from tvm.script import relax as R

@I.ir_module
class Module:
    @R.function
    def main(x: R.Tensor((2, 3, 4), dtype="float32"), index: R.Prim("int64")) -> R.Tensor((2, 4), dtype="float32"):
        gv: R.Tensor((2, 4), dtype="float32") = R.take(x, index, axis=1)
        return gv