import os
import numpy as np
import json
import struct
import open3d
# data_set_file = os.getcwd()+'\\data_set\\lidar_semantic_bboxes\\'


def read_file(file_name=os.getcwd()+'\\data_set\\lidar_semantic_bboxes\\'):
    # 输入为数据集绝对路径
    # 输出为.npz文件和.json文件位置
    npz_dir = []
    _3D_label_dir = []
    dirs = os.listdir(file_name)
    for di in dirs:
        if os.path.isdir(file_name+di):
            temp1 = os.listdir(file_name+di+'\\lidar\\cam_front_center')
            for i in range(len(temp1)):
                temp1[i] = file_name+di+'\\lidar\\cam_front_center\\' + temp1[i]
            npz_dir.extend(temp1)
            temp2 = os.listdir(file_name+di+'\\label3D\\cam_front_center')
            for i in range(len(temp2)):
                temp2[i] = file_name+di+'\\label3D\\cam_front_center\\' + temp2[i]
            _3D_label_dir.extend(temp2)
    return npz_dir, _3D_label_dir


def read_npz(file_path):
    # 输入为.npz文件路径
    # 输出为3D点云, 数据类型为np_array
    # npz文件的读取方法，注意，这种文件是一种压缩文件，不直接返回数据，使用以下方法获取压缩文件中的文件名
    # name_lis = np.load(file_path).files
    # print(name_lis)
    p_cloud = np.load(file_path)['points']
    return p_cloud


def read_json(file_path):
    # 返回值为字典列表类型
    with open(file_path, 'r') as js_f:
        load_dict = json.load(js_f)
    return load_dict


def read_bin(path):
    pc_list = []
    with open(path, 'rb') as f:
        content = f.read()
        pc_iter = struct.iter_unpack('ffff', content)
        for idx, point in enumerate(pc_iter):
            pc_list.append([point[0], point[1], point[2]])
    return np.asarray(pc_list, dtype=np.float64)
