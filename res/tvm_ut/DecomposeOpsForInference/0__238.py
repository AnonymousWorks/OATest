# from tvm.script import ir as I
# from tvm.script import relax as R

@I.ir_module
class Module:
    @R.function
    def main1(x: R.Tensor((1, 64, 112, 112), dtype="float32"), gamma: R.Tensor((64,), dtype="float32"), beta: R.Tensor((64,), dtype="float32"), moving_mean: R.Tensor((64,), dtype="float32"), moving_var: R.Tensor((64,), dtype="float32")) -> R.Tensor((1, 64, 112, 112), dtype="float32"):
        with R.dataflow():
            bn: R.Tuple(R.Tensor((1, 64, 112, 112), dtype="float32"), R.Tensor((64,), dtype="float32"), R.Tensor((64,), dtype="float32")) = R.nn.batch_norm(x, gamma, beta, moving_mean, moving_var, axis=1, epsilon=1.0000000000000001e-05, center=True, scale=True, momentum=0.10000000000000001)
            gv: R.Tensor((1, 64, 112, 112), dtype="float32") = bn[0]
            R.output(gv)
        return gv

    @R.function
    def main(x: R.Tensor((1, 64, 112, 112), dtype="float32"), gamma: R.Tensor((64,), dtype="float32"), beta: R.Tensor((64,), dtype="float32"), moving_mean: R.Tensor((64,), dtype="float32"), moving_var: R.Tensor((64,), dtype="float32")) -> R.Tensor((1, 64, 112, 112), dtype="float32"):
        with R.dataflow():
            bn: R.Tuple(R.Tensor((1, 64, 112, 112), dtype="float32"), R.Tensor((64,), dtype="float32"), R.Tensor((64,), dtype="float32")) = R.nn.batch_norm(x, gamma, beta, moving_mean, moving_var, axis=1, epsilon=1.0000000000000001e-05, center=True, scale=True, momentum=0.10000000000000001)
            gv: R.Tensor((1, 64, 112, 112), dtype="float32") = bn[0]
            R.output(gv)
        return gv