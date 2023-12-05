# -*- coding: utf-8 -*-
__author__ = 'zhuyixun'
__time__ = '2023/8/21'

import filecmp
import os
from difflib import HtmlDiff
import shutil

tag_1 = "base-2.4.3-20230630-1"
tag_2 = "base-2.4.4-20230803"
# 对升级包进行解压后的绝对路径，及存放对比结果的路径
path = 'D://diff'


def compare_folders(dir1, dir2, output):
    dcmp = filecmp.dircmp(dir1, dir2)

    for name in dcmp.left_only:
        output.write(f"只在{tag_1}中存在的文件或文件夹: {os.path.join(dir1, name)}\n")

    for name in dcmp.right_only:
        output.write(f"只在{tag_2}中存在的文件或文件夹: {os.path.join(dir2, name)}\n")

    for name in dcmp.diff_files:
        output.write(f"文件内容不同: {os.path.join(dir1, name)} - {os.path.join(dir2, name)}\n")

        # 输出不同文件的具体内容到HTML
        file1_path = f"{dir1}/{name}"
        file2_path = f"{dir2}/{name}"

        with open(file1_path, 'r', encoding='utf-8', errors='ignore') as file1, \
                open(file2_path, 'r', encoding='utf-8', errors='ignore') as file2:
            lines1 = file1.readlines()
            lines2 = file2.readlines()

        # 生成差异内容
        diff_html = HtmlDiff().make_file(lines1, lines2, fromdesc=file1_path, todesc=file2_path)

        # 将差异内容写入HTML文件
        with open(html_output_file, 'a', encoding='utf-8') as html_output:
            html_output.write(diff_html)

    for sub_dir in dcmp.common_dirs:
        compare_folders(os.path.join(dir1, sub_dir), os.path.join(dir2, sub_dir), output)


if __name__ == '__main__':
    try:
        folder_a_path = f"{path}/{tag_1}_diff_{tag_2}"
        # 删除文件夹A及其内容
        shutil.rmtree(folder_a_path)
        # 创建文件夹A
        os.mkdir(folder_a_path)
    except:
        # 创建文件夹A
        os.mkdir(folder_a_path)
    file_dict = ['base', 'base-web', 'audit', 'resource']
    for _path in file_dict:
        folder_A = f'{path}/cloudQuery_update{tag_1}/cloudQuery_update/cloudquery/{_path}/'
        folder_B = f'{path}/cloudQuery_update{tag_2}/cloudQuery_update/cloudquery/{_path}/'
        # 新建存在对比结果的目录文件夹，不存在则新建
        # os.path.join(directory, file_name)
        output_file = f'{path}/{tag_1}_diff_{tag_2}/{_path}.txt'
        html_output_file = f'{path}/{tag_1}_diff_{tag_2}/{_path}.html'
        with open(output_file, 'w') as output:
            compare_folders(folder_A, folder_B, output)
