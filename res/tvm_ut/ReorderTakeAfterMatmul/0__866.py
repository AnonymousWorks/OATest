# from tvm.script import ir as I
# from tvm.script import tir as T
# from tvm.script import relax as R

@I.ir_module
class Module:
    @R.function
    def main(x: R.Tensor(("batch_size", 1, 16), dtype="float32"), weight_table: R.Tensor(("routing_table_size", 16, 32), dtype="float32"), routing_table: R.Tensor(("batch_size",), dtype="int64")) -> R.Tensor(("batch_size", 1, 32), dtype="float32"):
        batch_size = T.int64()
        routing_table_size = T.int64()
        with R.dataflow():
            weight: R.Tensor((batch_size, 16, 32), dtype="float32") = R.take(weight_table, routing_table, axis=0)
            out: R.Tensor((batch_size, 1, 32), dtype="float32") = R.matmul(x, weight, out_dtype="void")
            R.output(out)
        return out