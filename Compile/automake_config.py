#	coding: UTF-8
#	author:	Guixinyu
#	create Time: 2019-09-17 18:15:39

import re
import os

from xml.etree.ElementTree import Element,SubElement, ElementTree





def SeparatePath(path,AllPath2,dir):
    while 1:
    #path1=re.split(os.getcwd(),path)[0]
    #pathPart=re.split("\\",path1)
    #a=os.getcwd()
        if path!=dir:
            if path not in AllPath2:
                AllPath2.append(path)
            path=os.path.dirname(path)
        else:
            break
    '''for i in pathPart:
        a=os.path.join(a,i)
        if a not in AllPath2:
            AllPath2.append(a)'''
    return AllPath2

def FindAllPath(dir):
    AllPath1=[]

    for path,dirs,files in os.walk(dir):
        for file in files:
            if file.endswith('.h')  or file.endswith('.c') and "TOOLS" not in path :
                AllPath1=SeparatePath(path,AllPath1,dir)

    return AllPath1
#print(includepath)



#user global set
def maininit():
    g_program_type = 1			# 1 表示一般程序, 2 表示动态库, 3 表示静态库
    # 是否递归对子目录进行编译链接

    g_except_dir_list = []	# 不进行编译链接处理的目录, 仅当g_handle_subdir设置为True时才有效
    g_except_file_list = [] # 不进行编译链接处理的文件

    g_bin_name = "test"	# 生成程序名或动态库名或静态库名

    g_debug_bin_name = "test_debug"	# 执行make debug时生成的程序名

    global DebugName
    global HighTecDir
    global CCFLAG
    global LINKFLAG
    global includepath
    global excludefiles
    DebugName = '11'
    HighTecDir = ''
    CCFLAG = ''
    LINKFLAG = ''
    includepath = []
    excludefiles = []




    if os.path.exists('./py.pyconfig'):
        f = open('./py.pyconfig')

        lines = f.readlines()


        for line in lines:
            # 工程名称
            # print(line)
            if 'DebugName=' in line:
                DebugName = re.split('DebugName=', line)[1]
                DebugName = DebugName[0:len(DebugName) - 1]

            # HighTec的路径
            if 'HighTecDir=' in line:
                HighTecDir = re.split('HighTecDir=', line)[1]
                HighTecDir = HighTecDir[0:len(HighTecDir) - 1]
            # 编译的标志
            if 'CCFLAG=' in line:
                CCFLAG = re.split('CCFLAG=', line)[1]
                CCFLAG = CCFLAG[0:len(CCFLAG) - 1]
            # 链接的标志
            if 'LINKFLAG=' in line:
                LINKFLAG = re.split('LINKFLAG=', line)[1]
                LINKFLAG = LINKFLAG[0:len(LINKFLAG) - 1]
            # post-build的设置
            if 'POSTBUILD=' in line:
                POSTBUILD = "os"
            # 所有目录的遍历
            # AllPath=FindAllPath()
            # 工程路径



            # dir
            if 'includepath=' in line:

                includepath1 = re.split('includepath=', line)[1]
                includepath1 = includepath1[0:len(includepath1) - 1]
                includepath1 = re.split(',', includepath1)
                for i in includepath1:
                    if i == '\n' or i == "":
                        continue
                    includepath.append(i)
            if 'excludefiles=' in line:

                excludefiles1 = re.split('excludefiles=', line)[1]
                excludefiles1 = excludefiles1[0:len(excludefiles1) - 1]
                excludefiles1 = re.split(',', excludefiles1)
                for j in excludefiles1:

                    if j == '\n' or j == '':
                        continue
                    excludefiles.append(j)



    else:
        f=open('./py.pyconfig','w')
        f.close()


    for exclude in excludefiles:
        if '.' in exclude:
            g_except_file_list.append(os.path.join(PROJECTDIR, exclude))
        else:
            g_except_dir_list.append(os.path.join(PROJECTDIR, exclude))

    return (DebugName,HighTecDir,CCFLAG,LINKFLAG,includepath,excludefiles,g_except_dir_list,g_except_file_list)

PROJECTDIR=os.getcwd()
g_handle_subdir = True
g_include_opt = ""  # 包含的头文件选项
g_libs_opt = ""  # 包含的动态库选项

g_ar_opt = ""  # 编译静态库时, ar命令的选项

g_install_commands = ["echo 'install command not set'"]
g_program_type = 1
