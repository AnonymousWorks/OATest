# from tvm.script import ir as I
# from tvm.script import relax as R

@I.ir_module
class Module:
    @R.function
    def main(x: R.Tensor((2, 3, 4, 5), dtype="float32"), gamma: R.Tensor((4, 5), dtype="float32"), beta: R.Tensor((4, 5), dtype="float32")) -> R.Tensor((2, 3, 4, 5), dtype="float32"):
        gv: R.Tensor((2, 3, 4, 5), dtype="float32") = R.nn.layer_norm(x, gamma, beta, axes=[-2, -1], epsilon=1.0000000000000001e-05, center=True, scale=True)
        return gv