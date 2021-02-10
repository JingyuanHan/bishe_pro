import open3d as o3d
import numpy as np
FOV = (30/180)*np.pi
HOV = (60/180)*np.pi
ROW_SCALE = 512
COL_SCALE = 512
class_list = ['bg', 'road', 'car', 'pedestrian', 'obstacle', 'cyclist']
color_list = [[1, 1, 1], [0, 0, 0], [1, 0, 0], [0.5, 0.5, 0], [0, 1, 0], [0, 0, 1]]


def find_class(point, boxes):
    class_id = 'bg'
    inside_f = 0
    below_f = 0
    for box_n in boxes:
        if is_inside(point, np.asarray(boxes[box_n]['3d_points'], dtype=np.float64)) and below_f == 0 and inside_f == 0:
            inside_f = 1
            if (boxes[box_n]['class'] == 'Car') or (boxes[box_n]['class'] == 'Truck') or \
                    (boxes[box_n]['class'] == 'VanSUV') or (boxes[box_n]['class'] == 'Bus') or \
                    (boxes[box_n]['class'] == 'UtilityVehicle') or (boxes[box_n]['class'] == 'CaravanTransporter') or \
                    (boxes[box_n]['class'] == 'Trailer') or (boxes[box_n]['class'] == 'EmergencyVehicle'):
                class_id = 'car'
            elif boxes[box_n]['class'] == 'Pedestrian':
                class_id = 'pedestrian'
            elif (boxes[box_n]['class'] == 'Cyclist') or (boxes[box_n]['class'] == 'MotorBiker') or \
                    (boxes[box_n]['class'] == 'Bicycle') or (boxes[box_n]['class'] == 'Motorcycle'):
                class_id = 'cyclist'
            else:
                class_id = 'obstacle'
        if is_below(point, np.asarray(boxes[box_n]['3d_points'], dtype=np.float64)) and below_f == 0 and inside_f == 0:
            below_f = 1
            class_id = 'road'
    if not inside_f and not below_f:
        class_id = 'obstacle'
    # 只要不在3D_bounding_box内或者下的点被归类为障碍
    return class_list.index(class_id)


def projection(p):
    # 将3D点云投影到2D，返回值为原点在左上角的ROW_SCALE*COL_SCALE的2D坐标数据类型为列表
    r = np.sqrt(p[0] ** 2 + p[1] ** 2 + p[2] ** 2)
    pitch = np.arcsin(p[2] / r)  # 仰角
    yaw = np.arctan(p[1] / p[0])  # 水平角
    u = int(((pitch + FOV / 2) / FOV) * ROW_SCALE)
    # v = int(0.5*(1+yaw/np.pi)*COL_SCALE)
    v = int(((yaw + 30 * np.pi / 180) / HOV) * COL_SCALE)
    return [u, v]


def pcloud_display(source_data, colors):
    # open3d的3d散点图绘制方法，优化的比较好
    # 输入为np_array类型的点云数据，colors也是np_array类型
    axis = o3d.geometry.TriangleMesh.create_coordinate_frame(size=3, origin=[0, 0, 0])
    # x, y, z axis will be rendered as red, green, and blue
    point_cloud = o3d.open3d.geometry.PointCloud()
    point_cloud.colors = o3d.utility.Vector3dVector(colors)
    point_cloud.points = o3d.utility.Vector3dVector(source_data)
    o3d.open3d.visualization.draw_geometries([point_cloud, axis], left=0, top=50, mesh_show_back_face=0)


def is_inside(point, box):
    # 判断点是否在长方体内
    # flag = 1 表示在长方体内，反之则在外
    flag = 0
    if is_between(point, box[0], box[1]) and is_between(point, box[0], box[4]) and is_between(point, box[0], box[3]):
        flag = 1
    else:
        flag = 0
    return flag


def is_between(point, p1, p2):
    vec1 = p2 - p1
    vec2 = point - p1
    vec3 = point - p2
    if cos_angle(vec1, vec2) * cos_angle(vec1, vec3) < 0:
        return True
    else:
        return False


def cos_angle(a, b):
    cos = a.dot(b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return cos


def is_below(point, box):
    # flag = 1 ==> point is under the box
    tem = 10000
    flag = 0
    for p in box:
        if p[2] < tem:
            tem = p[2]
    if point[2] < tem:
        flag = 1
    return flag
