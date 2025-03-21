# from tvm.script import ir as I
# from tvm.script import relax as R

@I.ir_module
class Module:
    @R.function
    def main(x: R.Tensor((2, 3, 4, 5), dtype="float32")) -> R.Tensor((), dtype="int64"):
        gv: R.Tensor((), dtype="int64") = R.argmin(x, axis=None, keepdims=False)
        return gv