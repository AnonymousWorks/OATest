import os
import tvm
import shutil


def load_seed_pool(seed_folder, max_pool_num):
    seed_cnt = 0
    for root, _, files in os.walk(seed_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith('.py'):
                _pass = os.path.basename(root)
                with open(file_path, 'r') as f:
                    content = f.read()
            try:
                ir = tvm.script.from_source(content)
            except Exception as e:
                print(e)
                # os.remove(file_path)
                continue
            seed_cnt += 1
            target_path = f"../res/irs_nnsmith/default/{file}"
            shutil.copy(file_path, target_path)
            print(seed_cnt)
            print(file_path, target_path)
            if seed_cnt >= max_pool_num:
                print(f"[INFO]: Finish load {seed_cnt} irs from {seed_folder}!")
                return
    print(f"[INFO]: Finish load {seed_cnt} irs from {seed_folder}!")


if __name__ == '__main__':
    load_seed_pool("../res/irs_nnsmith_9w/default/", 4000)

