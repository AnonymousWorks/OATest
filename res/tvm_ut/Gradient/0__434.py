# from tvm.script import ir as I
# from tvm.script import relax as R

@I.ir_module
class Module:
    @R.function
    def main(x: R.Tensor((3, 3), dtype="float32"), y: R.Tensor((3, 3), dtype="float32")) -> R.Tensor((), dtype="float32"):
        with R.dataflow():
            lv1: R.Tensor((3, 3), dtype="float32") = R.permute_dims(x, axes=None)
            lv2: R.Tensor((3, 3), dtype="float32") = R.permute_dims(y, axes=None)
            lv3: R.Tensor((3, 3), dtype="float32") = R.matmul(lv1, lv2, out_dtype="float32")
            gv: R.Tensor((), dtype="float32") = R.sum(lv3, axis=None, keepdims=False)
            R.output(gv)
        return gv