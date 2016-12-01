# -*- coding: utf-8 -*-

import os
import re


class EvernoteToOctopressBlog:
    # 输入信息：folder_name、 evernote_file_path、octopress_title、octopress_categories、octopress_tags
    def __init__(self, folder_name, evernote_file_path, octopress_title, octopress_categories, octopress_tags):
        # Octopress 博客的文件和图片文件夹名
        self.folder_name = folder_name
        # 马克飞象笔记文件（`.md`文件）路径
        self.evernote_file_path = evernote_file_path
        # Octopress 博客博文的title、categories、tags
        self.octopress_title = octopress_title
        self.octopress_categories = octopress_categories
        self.octopress_tags = octopress_tags
        # 标志位 马克飞象笔记是文件夹还是文件（是文件夹，为True）
        self.evernote_is_folder = True
        # 马克飞象笔记的文件名
        self.evernote_folder_name = ''
        # 马克飞象笔记文件夹所在路径
        self.root_directory = ''
        pass

    def __repr__(self):
        return 'EvernoteToOctopressBlog(\n\t{0.folder_name!r},\n\t{0.evernote_file_path!r},\n\t{0.octopress_title!r},\n\t{0.octopress_categories!r},\n\t{0.octopress_tags!r}\n)'.format(self)

    def __str__(self):
        return 'EvernoteToOctopressBlog(\n\t{0.folder_name!s},\n\t{0.evernote_file_path!s},\n\t{0.octopress_title!s},\n\t{0.octopress_categories!s},\n\t{0.octopress_tags!s}\n)'.format(self)

    def autoCheckEvernoteIsFolderOrFile(self): # Folder is return True
        # 自动检测这个博客是：仅仅一个文件（`.md`），还是一个文件夹
        # 给定马克飞象笔记文件（`.md`文件）路径，自动获取`root_directory`路径 和 `evernote_folder_name`名字
        delimiter = '\\'
        l1 = self.evernote_file_path.split(delimiter)
        # print(l1[-2])
        l2 = l1[-1].split('.')
        # print(l2[0])
        self.evernote_is_folder = l1[-2] == l2[0]
        a = -1
        str_temp = '文件'
        if self.evernote_is_folder:
            a = -2
            str_temp = '文件夹'
            pass
        print('当前处理的这个马克飞象笔记是一个' + str_temp)

        # 马克飞象笔记的文件名
        self.evernote_folder_name = l2[0]
        # 马克飞象笔记文件夹所在路径
        self.root_directory = delimiter.join(l1[:a]) + '\\'

        print('马克飞象笔记的文件或文件夹名：' + self.evernote_folder_name)
        print('马克飞象笔记的文件或文件夹所在目录：' + self.root_directory)
        pass

    def createFolderName(self):
        # 在root_directory路径里面创建一个名为 folder_name 的文件夹。（如果文件夹已经存在，则不用创建）
        folder_name_exists = os.path.exists(self.root_directory + self.folder_name)
        try:
            if folder_name_exists == False:
                print('Create a folder:' + self.root_directory + self.folder_name)
                os.mkdir(self.root_directory + self.folder_name)
                pass
            else:
                print(
                    'The folder "' + self.root_directory + self.folder_name + '" was already exist. Not need to create again.')
        except OSError as err:
            print('File error: ' + str(err))
            pass
        pass

    def copyImages(self):
        # 将马克飞象笔记文件夹里面的所有图片全部复制到刚刚新创建的folder_name 文件夹（路径）里面
        copy_img_command = 'copy "' + self.root_directory + self.evernote_folder_name + r'\*.png" "' + self.root_directory + self.folder_name + r'\"'
        # print(copy_img_command)
        os.system(copy_img_command)
        pass

    def openEvernoteFile(self):
        # 打开马克笔记的文件（.md后缀）
        evernote_file = open(self.evernote_file_path, 'rt', encoding='utf-8')
        evernote_data = evernote_file.read()
        evernote_file.close()
        # print(evernote_data)
        return evernote_data

    def replaceImgLink(self, evernote_data):
        # 将里面的图片链接替换为**Octopress**本地链接的形式
        image_local_path = re.findall('!\[Alt text\]\((.*?)\)', evernote_data, re.S)
        # print(image_local_path)
        image_relative_path = []
        for i in range(len(image_local_path)):
            image_relative_path.append('/images/' + self.folder_name + image_local_path[i][1:])
            # print(image_relative_path[i])
            evernote_data = evernote_data.replace(image_local_path[i], image_relative_path[i])
            pass
        # print(evernote_data)
        return evernote_data

    def getTime(self):
        # 获取当前系统时间（格式化成2016-03-20 11:45:39形式）
        import time
        # 格式化成2016-03-20 11:45:39形式
        time_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print(time_data)
        return time_data

    # 添加**Octopress**博客前缀
    def addOctopressBlogPrefix(self, octopress_file, title, data, categories, tags):
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

    def getOctopressFile(self, evernote_data):
        # 删除笔记里面的 第一个标题行（# xxx） 和 归宿笔记本行（@(xxx)）
        # 以后记马克飞象笔记，第1行是标题，第3行是 归宿笔记本。所以，我们只需要简单的将前3行删除就可。
        evernote_data_list = evernote_data.splitlines()
        octopress_file_path = self.root_directory + self.folder_name + '.markdown'  # r'F:\octopress\source\_posts\\' + self.folder_name + '.markdown'
        octopress_file = open(octopress_file_path, 'w', encoding='utf-8')
        time_data = self.getTime()
        octopress_file = self.addOctopressBlogPrefix(octopress_file, self.octopress_title, time_data, self.octopress_categories,
                                                self.octopress_tags)
        for i in range(3, len(evernote_data_list)):
            octopress_file.write(evernote_data_list[i] + '\n')
        octopress_file.close()
        octopress_file = open(octopress_file_path, 'r', encoding='utf-8')
        # print(octopress_file.read())
        octopress_file.close()
        pass

    def autoProcess(self):
        self.autoCheckEvernoteIsFolderOrFile()
        if self.evernote_is_folder: # 执行以下代码的前提是：马克飞象笔记是一个文件夹
            self.createFolderName()
            self.copyImages()
            pass
        evernote_data = self.openEvernoteFile()
        if self.evernote_is_folder: # 执行以下代码的前提是：马克飞象笔记是一个文件夹
            evernote_data = self.replaceImgLink(evernote_data)
            pass
        self.getOctopressFile(evernote_data)
        pass


import optparse

def main():
    # 输入信息：folder_name、 evernote_file_path、octopress_title、octopress_categories、octopress_tags
    parser = optparse.OptionParser('usage%prog ' +\
            '-f <folder_name> -p <evernote_file_path> -T <octopress_title> -c <octopress_categories> -t <octopress_tags>')
    parser.add_option('-f', dest='folder_name', type='string',\
                      help='be converted Octopress blog file and images file name')
    parser.add_option('-p', dest='evernote_file_path', type='string', \
                      help='evernote file path')
    parser.add_option('-T', dest='octopress_title', type='string', \
                      help='be converted Octopress blog\'s title')
    parser.add_option('-c', dest='octopress_categories', type='string', \
                      help='be converted Octopress blog\'s categories')
    parser.add_option('-t', dest='octopress_tags', type='string', \
                      help='be converted Octopress blog\'s tags')
    (options, args) = parser.parse_args()
    if (options.folder_name == None) | (options.evernote_file_path == None) | \
            (options.octopress_title == None) | (options.octopress_categories == None) | \
            (options.octopress_tags == None):
        print(parser.usage)
        exit(0)
        pass
    else:
        folder_name = options.folder_name
        evernote_file_path = options.evernote_file_path
        octopress_title = options.octopress_title
        octopress_categories = options.octopress_categories
        octopress_tags = options.octopress_tags
        # print(folder_name)
        # print(evernote_file_path)
        # print(octopress_title)
        # print(octopress_categories)
        # print(octopress_tags)
        eTo = EvernoteToOctopressBlog(folder_name, evernote_file_path, octopress_title, octopress_categories, octopress_tags)
        eTo.autoProcess()
        pass
    pass

if __name__ == '__main__':
    main()
    pass

# e.g. :
# python script\evernoteToOctopressBlog.py -f "2016-12-1-python-get-command-line-arguments" -p "D:\WorkSpace\test_ws\Python3 大型网络爬虫实战 003 — scrapy 大型静态图片网站爬虫项目实战 — 实战：爬取 169美女图片网 高清图片 — Over — 2016年11月26日 星期六\Python3 大型网络爬虫实战 003 — scrapy 大型静态图片网站爬虫项目实战 — 实战：爬取 169美女图片网 高清图片 — Over — 2016年11月26日 星期六.md" -T "Learning Python 028 获取命令行参数" -c "python" -t "python3, python2, 命令行, 参数, args"
