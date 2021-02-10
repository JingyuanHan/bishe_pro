import file_op
import data_op
import numpy as np
import time
import matplotlib.pyplot as plt
path = 'D:\\毕业设计\\data_set_3\\KITTITracking_data_tracking_velodyne\\training\\velodyne\\0000\\000000.bin'


def main():
    n = 108
    points_2d = []
    colors = []
    files_name_list = file_op.read_file()
    point_cloud = file_op.read_npz(files_name_list[0][n])
    boxes = file_op.read_json(files_name_list[1][n])
    for point in point_cloud:
        point_2d = data_op.projection(point)
        # point_2d.append(data_op.find_class(point, boxes))
        # point_2d.extend(point.tolist())
        points_2d.append(point_2d)
    for i in points_2d:
        print(points_2d.count(i))

    # for i in points_2d:
    #     colors.append(data_op.color_list[i[2]])
    # print(files_name_list[0][n])
    # data_op.pcloud_display(point_cloud, np.asarray(colors, dtype=np.float64))
    # points_2d = np.asarray(points_2d, dtype='float64')

    # fig = plt.figure()
    # ax1 = fig.add_subplot(1, 1, 1)
    # ax1.scatter(x=points_2d[:, 1], y=points_2d[:, 0], color=colors, s=10)
    # # plt.axis('off')
    # # fig.savefig('C:\\Users\\han\\Desktop\\1.png', bbox_inches='tight', pad_inches=0)
    # # fig.savefig('C:\\Users\\han\\Desktop\\2.png')
    # plt.show()
    return


def test_main():
    # 这里面都是瞎写的
    box = np.asarray([[11.07817559878468, -6.351005143423575, -1.8121],
                      [12.275471013185527, -3.4698797225758975, -1.8121],
                      [14.076174401215324, -4.218189356576427, -1.8121],
                      [12.878878986814478, -7.099314777424104, -1.8121],
                      [11.07817559878468, -6.351005143423575, 0.5178999999999999],
                      [12.275471013185527, -3.4698797225758975, 0.5178999999999999],
                      [14.076174401215324, -4.218189356576427, 0.5178999999999999],
                      [12.878878986814478, -7.099314777424104, 0.5178999999999999]],
                     dtype=np.float64)
    point = np.asarray([13, -6, 0.5], dtype=np.float64)
    print(data_op.is_inside(point, box))
    # tem = point_cloud.tolist()
    # tem.extend(boxes['box_1']['3d_points'])
    # print(boxes['box_1']['3d_points'])
    # point_cloud = np.asarray(tem)
    # colors.extend([[0, 0, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 0, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0]])
    # tem_min = 0
    # tem_max = 0
    # for i in points_2d:
    #     print(i[0:2])
    #     if i[1] > tem_max:
    #         tem_max = i[1]
    #     if i[1] < tem_min:
    #         tem_min = i[1]
    # print(tem_min, tem_max)


if __name__ == '__main__':
    start = time.perf_counter()
# code start

    # main()
    # test_main()
    color = []
    data = file_op.read_bin(path)
    for i in range(len(data)):
        color.append([0, 1, 0])
    color = np.asarray(color, dtype=np.float64)
    data_op.pcloud_display(data, color)

# code end
    end = time.perf_counter()
    print('\033[0;34m'+'[info] '+str(end - start)+' second elapsed'+'\033[0m')
