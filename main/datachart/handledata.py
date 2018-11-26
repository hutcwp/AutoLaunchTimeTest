# ecoding=utf-8
import json
import os

from pyExcelerator import *

from log.log import MLog

reload(sys)
sys.setdefaultencoding('utf-8')

file_path = os.path.dirname(__file__) + os.sep + "dataresult" + os.sep


def utf8(file_name):
    return file_name.decode('utf-8')


def write_json(json_data, json_file_name):
    fileObject = open(json_file_name, 'w')
    fileObject.write(json.dumps(json_data))
    fileObject.close()


def init_normal_style():
    style = XFStyle()
    style.font.name = 'Times New Roman'
    style.font.struck_out = True
    style.font.bold = True
    style.font.outline = True

    # 这里设置边框
    borders = Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1

    # 这里设置对齐方式
    al = Alignment()
    al.horz = Alignment.HORZ_CENTER
    al.vert = Alignment.VERT_CENTER

    style = XFStyle()
    style.borders = borders
    style.alignment = al
    return style


# 创建详细数据excel表格
def create_detail_sheet_by_json(sheet_name, file_name, title, json_data, title_list):
    # 创建一个工作簿
    w = Workbook()
    # 创建一个工作表
    ws = w.add_sheet(sheet_name)
    style = init_normal_style()

    content_size = 6000

    for i in range(0, 20):
        ws.col(i).width = content_size

    x_offset = 1
    y_offset = 2

    MLog.debug(str(json_data))

    ws.write_merge(0, 0, 0, len(json_data[0]) - 1, unicode(str(title), 'utf-8'), style)

    for index in range(0, json_data.__len__()):
        # # 写title
        # if index == 0:
        for i in range(0, len(json_data[index].keys())):
            key = json_data[index].keys()[i]
            if index == 0:
                # 写标题
                ws.write(1, i, title_list[key], style)
            # 写内容
            ws.write(index + y_offset, i, json_data[index][key], style)

    file_name = file_path + file_name

    try:
        if not os.path.exists(file_path):
            print u"文件路径不存在，现在创建一个..."
            print file_path
            os.mkdir(file_path)

        w.save(file_name + '.xls')
    except IOError:
        print u"创建文件失败！，异常如下:"
        print Exception
    else:
        print (u"Excel文件生成路径:" + os.path.abspath(file_name))


def main():
    file_name = u"耗时详情"
    sheet_name = "detail_time_cost"
    title = u"oppo r11 耗时统计"

    json_detail = [
        {"count": "1", "first_start": "4444", "normal_start": "3333", "home_start": "4444"},
        {"count": "2", "first_start": "4444", "normal_start": "3333", "home_start": "4444"},
        {"count": "3", "first_start": "4444", "normal_start": "3333", "home_start": "4444"},
    ]

    title_list = {"count": u"次数", "first_start": u"首次启动耗时", "normal_start": u"非首次启动耗时", "home_start": u"首页耗时"}

    create_detail_sheet_by_json(sheet_name, file_name, title, json_detail, title_list)

    ############# 下面是平均耗时
    file_name = u"平均结果"
    data = [{"first_start": "7.17", "phone": "OPPO R9s", "app": "7.11.1", "home": "0.15", "normal_start": "5.65"},
            {"first_start": "7.17", "phone": "OPPO R9s", "app": "7.11.1", "home": "0.15", "normal_start": "5.65"}]

    title_list2 = {"phone": u"机型", "app": u"应用", "first_start": u"非首次启动耗时", "normal_start": u"首页耗时", "home": u"首页加载"}

    create_detail_sheet_by_json(sheet_name, file_name, title, data, title_list2)


if __name__ == '__main__':
    main()
