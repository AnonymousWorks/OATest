import re
import os


def parse_info_file(filename, target_folder):
    with open(filename, 'r') as file:
        lines = file.readlines()

    coverage_data = {'lines': set(), 'functions': set(), 'branches': set()}
    source_total_data = {'lines': set(), 'functions': set(), 'branches': set()}

    current_file = None
    for line in lines:
        if line.startswith('SF:'):
            current_file = line.strip().split(':')[1]
        elif current_file and (f'{target_folder}src' in current_file or f'{target_folder}include' in current_file) :
            current_file = current_file.split('/data/shenqingchao/zibo')[-1]
            current_file = current_file.split('/home/shenqingchao')[-1]
            # print(current_file)

            unused_module = {'topi', 'relay', '/auto', '/te/', 'test',
                             '/primitive', 'target/source', 'schedule'}
            if any(keyword in current_file for keyword in unused_module):
                continue

            elif line.startswith('FNDA:'):
                parts = line.strip().split(':')
                execution_count = int(parts[1].split(',')[0])
                function_name = parts[1].split(',')[1]
                source_total_data['functions'].add((current_file, function_name))
                if execution_count > 0:
                    coverage_data['functions'].add((current_file, function_name))
            elif line.startswith('DA:'):
                parts = line.strip().split(':')
                line_info = parts[1].split(',')
                line_number = int(line_info[0])
                execution_count = int(line_info[1])
                source_total_data['lines'].add((current_file, line_number))
                if execution_count > 0:
                    coverage_data['lines'].add((current_file, line_number))
            elif line.startswith('BRDA:'):
                parts = line.strip().split(':')
                branch_info = parts[1].split(',')
                line_number = int(branch_info[0])
                block_number = int(branch_info[1])
                branch_number = int(branch_info[2])
                taken = branch_info[3]
                source_total_data['branches'].add((current_file, line_number, block_number, branch_number))
                if taken != '0' and taken != '-' and int(taken) > 0:
                    # print(branch_info)
                    coverage_data['branches'].add((current_file, line_number, block_number, branch_number))
    source_total_num = {k:len(v) for k, v in source_total_data.items()}
    print(f"Total coverage of {filename}:")
    print(f"Lines: {len(coverage_data['lines'])} / {source_total_num['lines']} = {len(coverage_data['lines'])/source_total_num['lines']}")
    print(f"Functions:{len(coverage_data['functions'])} / {source_total_num['functions']} = {len(coverage_data['functions'])/source_total_num['functions']}")
    print(f"Branches:{len(coverage_data['branches'])} / {source_total_num['branches']} = {len(coverage_data['branches'])/source_total_num['branches']}")
    print('\n\n')

    # res_file_base = f"cov_{os.path.split(filename)[-1].split('.')[0]}"
    # for granularity in ['lines', 'functions', 'branches']:
    #     res_file = f"{res_file_base}_{granularity}.txt"
    #     with open(res_file, 'w') as f:
    #         for item in coverage_data[granularity]:
    #             f.write(f"{item}\n")
    return coverage_data, source_total_num


def combine_coverage(file1_data, file2_data):
    combined_cov_dict = {
        'lines': file1_data['lines'].union(file2_data['lines']),
        'functions': file1_data['functions'].union(file2_data['functions']),
        'branches': file1_data['branches'].union(file2_data['branches'])
    }
    return combined_cov_dict


if __name__ == '__main__':
    target_folder = '/tvm/'
    base_dir = "/share_container/optfuzz/res/cov_cumulate"
    proj_list = os.listdir(base_dir)

    cov_dict = {}
    sound_proj_name = {'OATest': 'OATest', 'nnsmith': 'NNSmith', "whitefox": "WhiteFox", "MT_combine": "ModelTailor"}  # "hirgen": "HirGen",
    for proj in list(sound_proj_name.keys()):
        cov_dict[sound_proj_name[proj]] = []
        proj_path = os.path.join(base_dir, proj)
        print(proj)
        # if proj != 'hirgen':
        #     continue
        if proj == 'nnsmith':
            target_folder = "/tvm-lunder/"
        else:
            target_folder = '/tvm/'
        for i in range(25):
            if proj == 'whitefox':
                info_file = f"{proj_path}/{proj}_{i}.info"
            else:
                info_file = f"{proj_path}/sp_{proj}_{i}.info"
            # if info_file != "/share_container/optfuzz/res/cov_cumulate/MT_combine/sp_MT_combine_23.info":
            #     continue

            if not os.path.exists(info_file):
                continue
            print(info_file)
            cov_data, _ = parse_info_file(info_file, target_folder)
            if len(cov_dict[sound_proj_name[proj]]) <= 24:
                cov_dict[sound_proj_name[proj]].append([len(cov_data['lines']), len(cov_data['functions']), len(cov_data['branches'])])

    cov_line_dict = {}
    cov_func_dict = {}
    cov_branch_dict = {}
    for k, v in cov_dict.items():
        if len(v) != 0:
            cov_line_dict[k] = [i[0] for i in v]
            cov_func_dict[k] = [i[1] for i in v]
            cov_branch_dict[k] = [i[2] for i in v]

    print("line_cov_dict=", cov_line_dict)
    print("func_cov_dict=", cov_func_dict)
    print("branch_cov_dict=", cov_branch_dict)

    # for VN-graph
    # ut_info_file = "/software/tvm/_cov/sp_ut.info"
    # cov_nnsmith2k = f'/software/tvm/_cov/sp_nnsmith2k.info'
    # cov_hirgen2k = f"/software/tvm/_cov/sp_hirgen2k.info"
    # cov_data, _ = parse_info_file(ut_info_file, target_folder)
    # cov_data, _ = parse_info_file(cov_nnsmith2k, target_folder)
    # cov_data, _ = parse_info_file(cov_hirgen2k, target_folder)

    #
    # parse_info_file('/share_container/optfuzz/res/cov_cumulate/MT_combine_113/sp_MT_combine_23.info', target_folder)
    #
    # base_dir = "/software/tvm/_cov"
    # cov_modeltailor_nnsmith = f"{base_dir}/sp_MT_nnsmith.info"
    # cov_modeltailor_ut = f"{base_dir}/sp_MT_ut.info"
    # cov_modeltailor_hirgen = f"{base_dir}/sp_MT_hirgen.info"
    # parse_info_file(cov_modeltailor_nnsmith, target_folder)
    # parse_info_file(cov_modeltailor_ut, target_folder)
    # parse_info_file(cov_modeltailor_hirgen, target_folder)



