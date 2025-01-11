def abstract_shapes(undefined_vars):
    """
    抽象 undefined_vars 的 shape，不考虑具体维度大小，只识别相等关系
    """
    abstracted_vars = []
    all_dim_symbol_dict = {}
    shape_map = {}
    counter = 0

    for var in undefined_vars:
        var_name, shape, dtype = var
        abstracted_shape = []
        for dim in shape:
            # 将每个具体的维度值用符号表示
            sym = f"dim{counter}"
            abstracted_shape.append(sym)
            shape_map[sym] = dim
            all_dim_symbol_dict[sym] = dim
            counter += 1
        abstracted_vars.append([var_name, abstracted_shape, dtype])
    return abstracted_vars, all_dim_symbol_dict


def infer_inputs_constraints(all_dim_symbol_dict):
    from collections import defaultdict
    clustered_dict = defaultdict(list)
    for key, value in all_dim_symbol_dict.items():
        clustered_dict[value].append(key)

    return dict(clustered_dict)



def create_mapping(undefined_vars, used_vars, constraints):
    """
    根据 undefined_vars 的 shape 约束从 used_vars 中选择符合条件的变量
    """
    mapping = {}

    # 遍历 undefined_vars，尝试找到与其匹配的 used_vars
    for uvar in undefined_vars:
        u_name, u_shape, u_dtype = uvar
        for used_var in used_vars:
            used_name, used_shape, used_dtype = used_var

            # 检查 dtype 和 shape 长度是否匹配
            if u_dtype == used_dtype and len(u_shape) == len(used_shape):
                shape_match = True
                for u_dim, used_dim in zip(u_shape, used_shape):
                    # 检查是否有与 constraints 相冲突的维度
                    if isinstance(u_dim, str):
                        continue  # 跳过符号
                    if u_dim != used_dim:
                        shape_match = False
                        break

                if shape_match:
                    mapping[u_name] = used_name
                    break

    return mapping

def find_var_mapping(undefined_vars, used_vars):
    """
    主函数：推导 undefined_vars 之间的 shape 约束，并根据这些约束从 used_vars 中创建映射
    """
    # 抽象 undefined_vars 的 shape
    print(undefined_vars)
    abstracted_vars, all_dim_symbol_dict = abstract_shapes(undefined_vars)
    print(abstracted_vars)
    print(all_dim_symbol_dict)

    # 推理 shape 的相等关系约束
    constraints = infer_inputs_constraints(all_dim_symbol_dict)
    print(constraints)
    # 根据约束从 used_vars 中选择符合条件的变量
    mapping = create_mapping(abstracted_vars, used_vars, constraints)

    return mapping

# 示例数据
undefined_vars = [['x1', [2, 3], 'float32'], ['y1', [3, 2], 'float32'], ['z1', [2, 3], 'float32']]
used_vars = [['a1', [4, 5], 'float32'], ['b1', [5, 4], 'float32'], ['c1', [4, 5], 'float32']]

# 运行函数
mapping = find_var_mapping(undefined_vars, used_vars)
print(mapping)
