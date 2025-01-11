# import subprocess
#
#
# def execute_test_here(command):
#     try:
#         result = subprocess.run(
#             command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             check=True
#         )
#         return result.returncode, result.stdout, result.stderr
#     except subprocess.CalledProcessError as e:
#         return e.returncode, e.stdout, e.stderr
#
#
# # 示例：执行一个命令
# command = ["ls", "-l", "f./"]  # 将此替换为你要执行的系统命令
# return_code, stdout, stderr = execute_test_here(command)
#
# print("Return code:", return_code)
# print("STDOUT:", stdout)
# print("STDERR:", stderr)

#
# import os
# import tempfile
#
#
# def run_command(command):
#     with tempfile.NamedTemporaryFile(delete=True) as temp_out, tempfile.NamedTemporaryFile(delete=True) as temp_err:
#         return_code = os.system(f"{command}  2> {temp_err.name}")
#
#         with open(temp_err.name, 'r') as f:
#             stderr = f.read()
#         return return_code, stderr
#
#
# command = "ls -l f./"
# return_code, stderr = run_command(command)
#
# print("Return code:", return_code)
# print("STDERR:", stderr)



# cov_collect = f"lcov --capture --directory /software/tvm/build/CMakeFiles/tvm_objs.dir/src/ " \
#                                       f"--output-file /software/tvm/cov_modeltailor_{4}.info --rc lcov_branch_coverage=1"
# import subprocess
# subprocess.run(cov_collect)


# 示例 API 名字和参数
api_name = 'example_api'
args = [1, 2]
kwargs = {'kwarg1': 'value3'}


def Add(a, b):
    return a+b


res = Add(*args)
print(res)


