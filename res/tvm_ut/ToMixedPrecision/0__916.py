# from tvm.script import ir as I
# from tvm.script import relax as R

@I.ir_module
class Module:
    @R.function
    def main(x: R.Tensor((2, 3, 28, 28), dtype="float32"), w: R.Tensor((4, 3, 3, 3), dtype="float32")) -> R.Tensor((2, 4, 26, 26), dtype="float32"):
        with R.dataflow():
            x0: R.Tensor((2, 3, 28, 28), dtype="float32") = R.nn.relu(x)
            gv: R.Tensor((2, 4, 26, 26), dtype="float32") = R.nn.conv2d(x0, w, strides=[1, 1], padding=[0, 0, 0, 0], dilation=[1, 1], groups=1, data_layout="NCHW", kernel_layout="OIHW", out_layout="NCHW", out_dtype="float32")
            gv2: R.Tensor((2, 4, 26, 26), dtype="float32") = R.nn.relu(gv)
            R.output(gv2)
        return gv2