# from tvm.script import ir as I
# from tvm.script import relax as R

@I.ir_module
class Module:
    @R.function
    def main(x: R.Tensor((2, 3, 4, 5), dtype="float32")) -> R.Tensor((3, 4), dtype="float32"):
        gv: R.Tensor((3, 4), dtype="float32") = R.mean(x, axis=[0, 3], keepdims=False)
        return gv