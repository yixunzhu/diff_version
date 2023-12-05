# -*- coding: utf-8 -*-
__author__ = 'zhuyixun'
__time__ = '2023/8/21'

import filecmp
from difflib import HtmlDiff
import argparse
import json
import requests
import subprocess
import zipfile
import os

# 遛弯
url_test = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c6f24184-610f-4ad7-82a4-fcf913214386"
# 测试群
url_test_test = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4fb7d84a-78f3-44cf-a9cc-64e60f8c0723"
file_dict = ['base', 'base-web', 'audit', 'resource']


def send_projects_xx(send_message, mobile_lists, to_url=url_test):
    """
    默认发送测试群机器人
    :param send_message:
    :return:
    """
    data = json.dumps({
        "msgtype": "text",
        "text": {
            "content": send_message,  # 发送的消息内容
            "mentioned_list": mobile_lists,  # 圈出所有人
        }
    })
    # 指定机器人发送消息
    requests.post(to_url, data, auth=('Content-Type', 'application/json'), verify=False)


def compare_folders(dir1, dir2, output, args):
    dcmp = filecmp.dircmp(dir1, dir2)
    for name in dcmp.left_only:
        output.write(f"只在{args.tag_name_old}中存在的文件或文件夹: {os.path.join(dir1, name)}\n")

    for name in dcmp.right_only:
        output.write(f"只在{args.tag_name_new}中存在的文件或文件夹: {os.path.join(dir2, name)}\n")

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
        compare_folders(os.path.join(dir1, sub_dir), os.path.join(dir2, sub_dir), output, args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("tag_name_old", type=str, help='老版本的tag号')
    parser.add_argument("tag_name_new", type=str, help='新版本的tag号')
    args = parser.parse_args()
    tag_1 = args.tag_name_old
    tag_2 = args.tag_name_new
    bao_1 = f"cloudQuery_update{tag_1}.tar.gz"
    bao_2 = f"cloudQuery_update{tag_2}.tar.gz"

    # 远程压缩包路径
    remote_archive_path = "/mnt/backup/安装包"
    # 远程解压目标路径
    remote_diff_path = f"{remote_archive_path}/diff"
    # 执行远程命令判断解压目标文件夹是否存在并新建
    os.makedirs(f"{remote_diff_path}", exist_ok=True)
    # 删除远程diff文件夹下所有内容
    remote_folder_path = f"{remote_diff_path}"
    # 执行远程命令删除文件夹及其内容
    command = f"rm -rf {remote_folder_path}/*"
    subprocess.run(command, shell=True)
    # 先判断tag_1有没有
    if os.path.exists(os.path.join(remote_archive_path, tag_1)):
        # 执行解压缩命令
        tag_1_command = f"mkdir -p {remote_diff_path}/cloudQuery_update{tag_1}"
        subprocess.run(tag_1_command, shell=True)
        command_tar = f"tar -zxvf {remote_archive_path}/{tag_1}/{bao_1} -C {remote_diff_path}/cloudQuery_update{tag_1}"
        subprocess.run(command_tar, shell=True)
    else:
        print(f"没有{tag_1}安装/升级包文件")
    # 在判断tag_2有没有
    if os.path.exists(os.path.join(remote_archive_path, tag_2)):
        # 执行解压缩命令
        tag_2_command = f"mkdir -p {remote_diff_path}/cloudQuery_update{tag_2}"
        subprocess.run(tag_2_command, shell=True)
        command_tar = f"tar -zxvf {remote_archive_path}/{tag_2}/{bao_2} -C {remote_diff_path}/cloudQuery_update{tag_2}"
        subprocess.run(command_tar, shell=True)
    else:
        print(f"没有{tag_2}安装/升级包文件")
    ########################################
    # 对解压好的文件进行对比
    ########################################
    # 判断生成目标文件夹是否存在并新建
    os.makedirs(f'{remote_diff_path}/{tag_1}_diff_{tag_2}', exist_ok=True)
    for _path in file_dict:
        folder_A = f'{remote_diff_path}/cloudQuery_update{tag_1}/cloudQuery_update/cloudquery/{_path}/'
        folder_B = f'{remote_diff_path}/cloudQuery_update{tag_2}/cloudQuery_update/cloudquery/{_path}/'
        output_file = f'{remote_diff_path}/{tag_1}_diff_{tag_2}/{_path}.txt'
        html_output_file = f'{remote_diff_path}/{tag_1}_diff_{tag_2}/{_path}.html'
        with open(output_file, 'w') as output:
            compare_folders(folder_A, folder_B, output, args)

    folder_a = f'{remote_diff_path}/{tag_1}_diff_{tag_2}'
    zip_file = f'{folder_a}.zip'

    # 创建ZIP文件
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        # 遍历文件夹A中的所有文件和子文件夹
        for foldername, subfolders, filenames in os.walk(folder_a):
            for filename in filenames:
                # 将文件添加到ZIP文件中
                file_path = os.path.join(foldername, filename)
                zipf.write(file_path, os.path.relpath(file_path, folder_a))
    print(f"文件夹 {folder_a} 已成功压缩为 {zip_file}")
    _text = f"1、{tag_1} 和 {tag_2} 的配置对比完成;\n2、对比结果已经转换成压缩包名称：{tag_1}_diff_{tag_2}.zip，请及时查看结果！\n 3、可以在本地CMD下使用如下命令把结果复制到自己本地D盘中（D盘根目录），命令：scp root@192.168.3.115:{remote_diff_path}/{tag_1}_diff_{tag_2}.zip /D:/"
    send_projects_xx(_text, ["@all"])
    send_projects_xx(_text, ["@all"], url_test_test)
