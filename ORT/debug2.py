import onnx
import onnxruntime as ort
from onnxruntime.transformers import optimizer
import numpy as np
import type_utils


def random_input(model):
    inputs = {}
    for input_tensor in model.graph.input:
        input_name = input_tensor.name
        tensor_type = input_tensor.type.tensor_type
        this_dtype = type_utils.onnx_type2numpy[tensor_type.elem_type]
        # print(input_name, tensor_type)
        if len(tensor_type.shape.dim) != 0:  # has tensor shape
            shape = [dim.dim_value if dim.dim_value > 0 else 1 for dim in tensor_type.shape.dim]
            inputs[input_name] = np.random.rand(*shape).astype(this_dtype)

        elif tensor_type.elem_type in [0, 1, 10, 11, 16, 17, 18, 19, 20]:  # const: float
            inputs[input_name] = this_dtype(np.random.random())
        elif tensor_type.elem_type in [2, 3, 4, 5, 6, 7, 13, 21, 22]:  # const: int
            inputs[input_name] = this_dtype(np.random.randint(1, 10))
        elif tensor_type.elem_type in [9]:
            inputs[input_name] = np.bool_(np.random.choice([True, False]))
        else:
            print(f"[WARNING]: Unsolved type:{tensor_type.elem_type}!")
    return inputs


def optimize_and_infer(model_path):
    model = onnx.load(model_path)
    input_data = random_input(model)

    # [Online] Run inference with the original model
    sess_options = ort.SessionOptions()
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_DISABLE_ALL
    original_session = ort.InferenceSession(model_path, sess_options, providers=["CUDAExecutionProvider"])
    original_output_names = [output.name for output in original_session.get_outputs()]
    original_result = original_session.run(original_output_names, input_data)
    original_result2 = original_session.run(original_output_names, input_data)
    for r1, r2 in zip(original_result, original_result2):
        np.testing.assert_allclose(r1, r2, rtol=1e-3, atol=1e-3)

    # [Offline] Run inference with the optimized model
    optimized_model_path = f"./opt.onnx"
    optimized_model = optimizer.optimize_model(model_path, opt_level=1)  # [0, 1, 2, 99]
    optimized_model.save_model_to_file(optimized_model_path)
    optimized_session = ort.InferenceSession(optimized_model_path)
    optimized_output_names = [output.name for output in optimized_session.get_outputs()]
    optimized_result = optimized_session.run(optimized_output_names, input_data)

    # 【Differential Testing】 Compare the inference results between original and optimized models
    for r1, r2 in zip(original_result, optimized_result):
        np.testing.assert_allclose(r1, r2, atol=1e-3, rtol=1e-3)
    print("Run well!")


if __name__ == '__main__':
    optimize_and_infer("../res/onnx_res_1211/res_executions/17779.onnx")
