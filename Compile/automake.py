#	coding: UTF-8
#	author:	Guixinyu
#	create Time: 2019-09-17 18:15:39

import os
import re
from automake_config import *
import subprocess
import sys
a=sys.argv
# program global set
COMMON_TYPE = 1		# common program
DYNAMIC_TYPE = 2	# dynamic library
STATIC_TYPE = 3		# static library

g_tabKey = "\t"
g_newLine = g_tabKey
g_mid_ext = ".o"			# 中间文件扩展名


includeReg = r'''^\s*#include\s*"(.+?\.h)"\s*$'''		# 获取所包含头文件的正则表达式
sourceItemList = None
headerItemList = None


def is_same_dir(srcDir, dstDir) :
	'''
	是否同一目录
	'''

	if os.path.abspath(srcDir) == os.path.abspath(dstDir) :
		return True
	else :
		return False

def get_files(path, typeList, isRecursion = False, exceptFileList = [], exceptDirList = []) :
	'''
	description: 获取符合条件的文件名(包括路径)列表
	param path 指定路径
	param typeList 文件类型
	param isRecursion 是否递归处理子目录
	param exceptFileList 除外的文件
	param exceptDirList 除外的目录,仅当isRecursion为True时才生效
	'''

	resultList = []
	fileNames = os.listdir(path)
	for name in fileNames :
		if name !='TOOLS':
			filePath = os.path.join(path, name)
			fileFullPath = os.path.abspath(filePath)
			isDir = os.path.isdir(filePath)
			if isDir and (isRecursion == True) and (fileFullPath not in exceptDirList) :
				resultList.extend( get_files(filePath, typeList, isRecursion, exceptFileList, exceptDirList) )	# 处理子目录
			elif not isDir and (os.path.splitext(filePath)[1] in typeList) and (fileFullPath not in exceptFileList) :
				resultList.append(filePath)		# 处理文件

	return resultList

def createIndex(fileList) :
	'''
	建立索引
	'''

	resultDict = {}
	for filePath in fileList :
	
		fileName = os.path.split(filePath)[1]
		
		#fileName = os.path.splitext(fileName)[0]
		resultDict[fileName] = filePath
		#print resultDict

	return resultDict



def generaret_sourcesmk(sourceItemList) :


	objFileListStr = ""
	cFileListStr = ""
	dFileListStr = ""
	objectlistpath=[]
	f=open('./Default/sources.mk','w')
	txt= '''S_SRCS := 
ASM_UPPER_SRCS := 
CPCP_SRCS := 
ASM_SRCS := 
MCS_SRCS := 
S_UPPER_SRCS := 
O_SRCS := 
PCP_S := 
EXECUTABLES := 
C_SRCS := 
OBJS := 
C_DEPS := 
SUBDIRS := '''	
	subdirs=""
	f.write(txt)
	#objDebugFileListStr = ""
	for name in sourceItemList :

		path=re.split(name,sourceItemList[name])[0].replace('\\','/')
		#print path
		name1=os.path.splitext(sourceItemList[name])[0].replace('\\','/')
		name = os.path.splitext(name)[0]
		#objFileListStr += ('./Object/'+name+ g_mid_ext + " \\\n" )
		#objectlistpath += ('Object/'+name+ g_mid_ext + " \n" )
		#cFileListStr += ("."+ path +name+ '.c' + " \\\n" )
		#dFileListStr += ('./Object/'+name+ '.d' + " \\\n" )
		objectlistpath.append(name1+ g_mid_ext + " \n" )
		#objDebugFileListStr += ( g_tabKey + name + g_debug_mid_ext + "\\\n")
		if path not in subdirs:
				subdirs +=('\\\n'+path+' ')
	f.write(subdirs)
	f.close()

	f.close()
	f2=open('./Default/Default.objectlist','w')
	a=objectlistpath.sort()
	#print(a)
	#print(objectlistpath)
	for ii in objectlistpath:
	    #print(ii)
	    f2.write(ii)
	f2.close()
	#print "OBJECTS_DEBUG=\\"
	#print objDebugFileListStr + g_tabKey





def generaret_subdirmk(sourceItemList,includepath):
	paths=[]
	g=open('./Default/Default.includepathlist','w')
	for kk in includepath:

			path1=os.path.join(PROJECTDIR,kk[1:])
			#print(PROJECTDIR)
			kk=path1.replace('\\','/')

			#pathaa=PROJECTDIR.replace('\\','/')
			g.write(''' -I"'''+kk+'''"\n''')

	g.close()


	i=0

	for name in sourceItemList:
		path=re.split(name,sourceItemList[name])[0].replace('\\','/')
		if path not in paths:		
			paths.append(path)
	
	for k in paths:
		
		if os.path.exists('./Default/'+k.replace('./','')):
			
			
			pass
		else:
			os.makedirs('./Default/'+k.replace('./',''))



		f=open('./Default/'+k.replace('./','')+'/subdir.mk','w')

		#gxy 2019-06-06 change the subdir.mk improve the makefile rate
		listpath=os.listdir(PROJECTDIR+'/'+k)
		
		f.write('C_SRCS +=')
		
		for kfile in listpath:			
			if kfile.endswith('.c') and kfile  in sourceItemList:
				f.write(' \\\n')
				f.write('.'+sourceItemList[kfile].replace('\\','/'))
				
		f.write('\n')
		f.write('OBJS +=')
		for kfile in listpath:
			if kfile.endswith('.c') and kfile  in sourceItemList:
				f.write(' \\\n')
				#namefile=os.path.splitext(kfile)[0]				
				#f.write('./Object/'+namefile+'.o')
				namefile=os.path.splitext(sourceItemList[kfile])[0]
				f.write(namefile.replace('\\','/')+'.o')
		f.write('\n')
		f.write('C_DEPS +=')
		for kfile in listpath:
			if kfile.endswith('.c') and kfile  in sourceItemList:
				f.write(' \\\n')
				#namefile=os.path.splitext(kfile)[0]
				
				#f.write('./Object/'+namefile+'.d')
				namefile=os.path.splitext(sourceItemList[kfile])[0]
				f.write(namefile.replace('\\','/')+'.d')
		f.write('\n')
		aaa=k.replace('.','_')
		kkk=re.split('_/',aaa)[1]

		
		txt=kkk+'%.o: .'+k+'%.c\n'
		txt2='''	@echo 'Building file: $<'
	"tricore-gcc" -c '''
		f.write(txt+txt2)
		'''for kk in includepath:
			kk=kk.replace('/','\\')
			pathaa=PROJECTDIR'''
			#f.write(''' -I"'''+pathaa+'\\'+kk+'''"''')
		#f.write('^')
		nowpath=PROJECTDIR.replace('\\','/')
		txtincludepath='@'+nowpath+'/Default/Default.includepathlist'
		f.write(txtincludepath)

		txt3=' '+CCFLAG
		f.write(txt3)
		txt4='''\n	@echo 'Finished building: $<'\n'''
		txt5="	@echo ' '"
		f.write(txt4)
		f.write(txt5)
		f.close()
		i+=1
		
def generaret_makefile():
	libPath=PROJECTDIR
	txt='''-include ../makefile.init
RM := rm -rf
TRICORE_TOOLS=%s
-include sources.mk
'''%HighTecDir
	f=open('./Default/makefile','w')
	f.write(txt)
	#sublist=os.listdir('./Default/subdirmk')
	sublist=os.walk('./Default')
	#for i in sublist:
	#	f.write('-include subdirmk/'+i+'\n')

	for path22,dir22,filelist22 in sublist:
		for file222 in filelist22:
			if file222.endswith('.mk') and 'sources.mk' not in file222 :
				#print file222
				qwe=re.split('/Default/',path22.replace('\\','/'))
				qwe=qwe[len(qwe)-1]
				
				f.write('-include '+qwe.replace('\\','/')+'/'+file222+'\n')
	a=PROJECTDIR.replace('\\','/')
	postbuild=a+'/TOOLS/A2L/genA2l.bat '+PROJECTDIR.replace('\\','/')+" "+DebugName
	txt2='''ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 

#rebuild target
rebuild: clean all

# All Target
all: %s.elf

# Tool invocations
%s.elf: $(OBJS) $(USER_OBJS) $(ASM)
	@echo 'Building target: $@'
	"$(TRICORE_TOOLS)/bin/tricore-gcc" -o  "%s.elf" %s
	@echo 'Finished building target: $@'
	@echo ' '
	$(MAKE) --no-print-directory post-build

# Other Targets
clean:
	-$(RM) $(PCP_S)$(EXECUTABLES)$(OBJS)$(C_DEPS)$(CPCP_DEPS) %s.elf
	-@echo ' '

post-build:
	%s
	-@echo ' '

.PHONY: all clean dependents
.SECONDARY: post-build

-include ../makefile.targets'''%(DebugName,DebugName,DebugName,LINKFLAG,DebugName,postbuild)
	f.write(txt2)
	f.close()




path = "."
(DebugName,HighTecDir,CCFLAG,LINKFLAG,includepath,excludefiles,g_except_dir_list,g_except_file_list)=maininit()

sourceTypeList = ( ".c",)
headerTypeList = (".h", )
exceptFileList = [ os.path.abspath(i[3:]) for i in g_except_file_list ]

exceptDirList  = [ os.path.abspath(i[3:]) for i in g_except_dir_list ]

sourceItemList = createIndex( get_files(path, sourceTypeList, g_handle_subdir, exceptFileList, exceptDirList) )

#headerItemList = createIndex( get_files(path, headerTypeList, g_handle_subdir, exceptFileList, exceptDirList) )
#print sourceItemList
if g_program_type == DYNAMIC_TYPE :
		g_libs_opt += " -shared"


if os.path.exists('./Default'):
		pass
else:
		os.mkdir('./Default')

generaret_sourcesmk(sourceItemList)

generaret_subdirmk(sourceItemList,includepath)
generaret_makefile()
#os.system('TOOLS\Compile\compile.bat>console.log 2>&1')
cmd=HighTecDir+r'\bin\make'
#print(includepath)

#subprocess.Popen(a[1]+'\Compile\compile.bat '+cmd)
#os.system(a[1]+'\Compile\compile.bat '+cmd)
#os.system('echo 1')
