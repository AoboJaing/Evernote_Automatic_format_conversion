# -*- coding: utf-8 -*-

import os
import re

# 输入信息：folder_name、 evernote_folder_name、 root_directory、octopress_title、octopress_categories、octopress_tags

# Octopress 博客的文件和文件夹名
folder_name = '2016-11-29-PyCharm-software-professional-download-install-Crack-Registration'
# 马克飞象笔记的文件名
evernote_folder_name = 'PyCharm 软件（professional版 专业版）在Windows系统上的下载、安装、破解图文教程  — 2016年11月29日 星期二'
# 马克飞象笔记文件夹所在路径
root_directory = r'D:\WorkSpace\test_ws\\'

# Octopress 博客博文的title、categories、tags
octopress_title = 'PyCharm 软件（professional版 专业版）在Windows系统上的下载、安装、破解图文教程'
octopress_categories = '软件安装'
octopress_tags = 'PyCharm, Windows, 软件安装'

# 在root_directory路径里面创建一个名为 folder_name 的文件夹
try:
    os.mkdir(root_directory+folder_name)
except OSError as err:
    print('File error: ' + str(err))
    pass

# 将马克飞象笔记文件夹里面的所有图片全部复制到刚刚新创建的folder_name 文件夹（路径）里面
copy_img_command = 'copy "' + root_directory + evernote_folder_name + r'\*.png" "' + root_directory + folder_name + r'\"'
# print(copy_img_command)
os.system(copy_img_command)

pass
# # 将马克飞象笔记文件夹（evernote_folder_name）里面的笔记文件（.md 文件），
# # 复制一份放到root_directory 路径下，并将其名字重命名为：folder_name 变量，并将其后缀修改为：.markdown
# copy_file_command = 'copy "' + root_directory + evernote_folder_name + r'\\' + evernote_folder_name + '.md" "' + root_directory + folder_name + '.markdown"'
# # print(copy_file_command)
# os.system(copy_file_command)
pass

# 打开马克笔记的文件（.md后缀）
evernote_file_path = root_directory + evernote_folder_name + r'\\' + evernote_folder_name + '.md'
evernote_file = open(evernote_file_path, 'rt', encoding='utf-8')
evernote_data = evernote_file.read()
evernote_file.close()
# print(evernote_data)

# 将里面的图片链接替换为**Octopress**本地链接的形式
image_local_path = re.findall('!\[Alt text\]\((.*?)\)', evernote_data, re.S)
# print(image_local_path)
image_relative_path = []
for i in range(len(image_local_path)):
    image_relative_path.append('/images/' + folder_name + image_local_path[i][1:])
    # print(image_relative_path[i])
    evernote_data = evernote_data.replace(image_local_path[i], image_relative_path[i])
# print(evernote_data)

# 获取当前系统时间（格式化成2016-03-20 11:45:39形式）
import time
# 格式化成2016-03-20 11:45:39形式
time_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# print(time_data)

# 添加**Octopress**博客前缀
def addOctopressBlogPrefix(octopress_file, title, data, categories, tags):
    octopress_file.write('---' + '\n')
    octopress_file.write('layout: post' + '\n')
    octopress_file.write('title: "' + title + '"' + '\n')
    octopress_file.write('date: ' + data + ' +0800' + '\n')
    octopress_file.write('comments: true' + '\n')
    octopress_file.write('sharing: true' + '\n')
    octopress_file.write('categories: [' + categories + ']' + '\n')
    octopress_file.write('tags: [' + tags + ']' + '\n')
    octopress_file.write('---' + '\n')
    return octopress_file


# 删除笔记里面的 第一个标题行（# xxx） 和 归宿笔记本行（@(xxx)）
# 以后记马克飞象笔记，第1行是标题，第3行是 归宿笔记本。所以，我们只需要简单的将前3行删除就可。
evernote_data_list = evernote_data.splitlines()
octopress_file_path = root_directory + folder_name + '.markdown'  # r'F:\octopress\source\_posts\\' + folder_name + '.markdown'
octopress_file = open(octopress_file_path, 'w', encoding='utf-8')
octopress_file = addOctopressBlogPrefix(octopress_file, octopress_title, time_data, octopress_categories,  octopress_tags)
for i in range(3, len(evernote_data_list)):
    octopress_file.write(evernote_data_list[i] + '\n')
octopress_file.close()
octopress_file = open(octopress_file_path, 'r', encoding='utf-8')
print(octopress_file.read())
octopress_file.close()



