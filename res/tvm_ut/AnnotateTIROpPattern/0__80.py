# from tvm.script import ir as I
# from tvm.script import tir as T

@I.ir_module
class Module:
    @T.prim_func
    def sum(A: T.Buffer((16, 16), "float32"), B: T.Buffer((16,), "float32")):
        T.func_attr({"global_symbol": "elemwise"})
        # with T.block("root"):
        for i, j in T.grid(16, 16):
            with T.block("matmul"):
                vi, vj = T.axis.remap("SR", [i, j])
                T.reads(A[vi, vj])
                T.writes(B[vi])
                with T.init():
                    B[vi] = T.float32(0)
                B[vi] = B[vi] + A[vi, vj]