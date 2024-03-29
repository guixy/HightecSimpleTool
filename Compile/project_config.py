# -*- coding: utf-8 -*-

#	author:	Guixinyu
#	create Time: 2019-10-17 18:15:39

from PyQt5.QtWidgets import  *
import sys
import first
import fileselect
import shutil

from first import Ui_MainWindow
import AddLibraryPath
import Enterlibraries
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import  os
import  re
import subprocess
import time
#读取log的线程
class BackendTread(QThread):
    setvalue = pyqtSignal(int)
    def __init__(self, parent=None):
        super(BackendTread, self).__init__(parent)
        self.working=True
    def stopSig(self):
        self.working=False
    def run(self):
        #cmd1 = r'''%s\bin\make -j8 all >console.log 2>&1''' % Hdir
        '''os.chdir(self.ProjectName_2.text() + '/Default')
        self.process = subprocess.call(cmd1)'''
        while VAL<NUM and self.working:
            num=0
            for path,dir,files in os.walk(os.getcwd()):
                for file in files:
                    if file.endswith('.o'):
                        num=num+1
            self.setvalue.emit(num)


#开编译的线程
class BackendTread1(QThread):
    startcompile1 = pyqtSignal(str)
    endSig = pyqtSignal()
    def __init__(self, parent=None):
        super(BackendTread1, self).__init__(parent)

    def startCom(self):
        self.process = subprocess.Popen(cmd1)

    def run(self):
        #cmd1 = r'''%s\bin\make -j8 all >console.log 2>&1''' % Hdir
        '''os.chdir(self.ProjectName_2.text() + '/Default')
        self.process = subprocess.call(cmd1)'''
        f=open('conerr.err','w+')

        self.process = subprocess.Popen(cmd1,stdout=subprocess.PIPE,stderr=f,bufsize=1)

        '''self.bt=BackendTread()
        self.bt.startcompile.connect(self.PrintConsole)
        self.bt.start()'''
        self.sleep(3)

        while self.process.poll() is None:
            #print(1)
            r = self.process.stdout.readline().decode('gbk')
            if r:
                self.startcompile1.emit(r)
            if 'tool>pause'in r:
                break
        os.system(r"taskkill /f /t /im make.exe")#因为在做post-build的时候，al2的工具需要按回车键才能结束进程，因为在这里强制性的使其结束
        self.endSig.emit()


class basePage(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(basePage, self).__init__()
        self.setupUi(self)

        self.startpath=os.getcwd()
        self.actionbuild.triggered.connect(self.checkFLAG)
        #self.menuclean.triggered.connect(self.CleanProject)
        self.actionclean.triggered.connect(self.CleanProject)
        self.actionopen_project.triggered.connect(self.ChooseProDir)
        self.actionsave_project.triggered.connect(self.modifyFLAG)

        #self.quitApp.triggered.connect(QCoreApplication.instance().quit)   #关闭程序的第一种方式
        self.actionexit.triggered.connect(qApp.quit)#关闭程序的第二种方式



        #添加工具栏:停止和退出
        self.tb1=self.addToolBar('tool')
        actionopen1=QAction(QIcon('./Compile/file.png'),"打开工程",self)
        self.tb1.addAction(actionopen1)
        actionopen1.triggered.connect(self.ChooseProDir)
        self.tb1.addSeparator()
        actionstop=QAction(QIcon('./Compile/stop.png'),"停止",self)
        self.tb1.addAction(actionstop)
        actionstop.triggered.connect(self.KillProcess)
        self.tb1.addSeparator()
        actionExit=QAction(QIcon('./Compile/exit.png'),"退出",self)
        self.tb1.addAction(actionExit)
        actionExit.triggered.connect(qApp.quit)
        ##创建右键菜单
        #self.includeList.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.includeList.customContextMenuRequested.connect(self.showRightMenu)
        #self.includeList.customContextMenuRequested[QPoint].connect(self.remove)
        #单击一个选项
        #self.f=""
        #self.includeList.clicked.connect(self.check)
        self.includeList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.excludeList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.contextMenu=QMenu(self)


        self.actionA=self.contextMenu.addAction("删除")
        self.actionA.triggered.connect(self.remove)

        self.includeList.customContextMenuRequested.connect(lambda :self.showContextMenu(1))

        #self.contextMenu.triggered[QAction].connect(self.remove)
        #self.includeList.customContextMenuRequested[QPoint].connect(self.remove1)#[]里的代表传入的参数，自带的


        self.excludeList.customContextMenuRequested.connect(lambda :self.showContextMenu(2))
        #self.excludeList.customContextMenuRequested[QPoint].connect(self.remove2)  # []里的代表传入的参数，自带的



        self.delPath1.clicked.connect(self.includeList.clear)
        self.delPath2.clicked.connect(self.excludeList.clear)


        self.addPath1.clicked.connect(lambda :self.ShowDialog(1))
        self.addPath2.clicked.connect(self.AddExpath)


        self.fileselect = fileselect.Ui_Dialog()

        #初始化page

        self.listWidget.currentRowChanged.connect(self.display)

        #Library的初始化
        self.initLibraryWindow()
        self.Llist.setSelectionMode(3)
        self.llist.setSelectionMode(3)
        #self.add2.clidken.connect(self.ShowLWindow)
        #状态栏的部件
        self.barlabel = QLabel('barlabel')
        #self.initDialog()

        #self.fileselect.buttonBox
        #print(self.fileselect.treeWidget.currentItem().text(0))
    def initUI(self):
        self.includeList.clear()
        self.excludeList.clear()
        self.Llist.clear()
        self.llist.clear()
        self.ProjectName.setText(self.DebugName)
        self.HithTecDir.setText(self.HighTecDir)
        self.GCCFLAGName.setText(self.CCFLAG)
        self.LINKFLAGName.setText(self.LINKFLAG)
        self.ProjectName_2.setText(self.PROJECTDIR)
        self.ProjectName_2.setEnabled(False)

        self.barlabel.setText('准备中')
        self.statusBar.addPermanentWidget(self.barlabel)
        self.Result.clear()

        if self.includepath:
            #a=1
            self.includeList.addItems(self.includepath)

        if self.excludefiles:
            #a=1
            self.excludeList.addItems(self.excludefiles)

        if self.LibraryPath:
            #a=1
            self.Llist.addItems(self.LibraryPath)
        if self.libraties:
            #a=1
            self.llist.addItems(self.libraties)

    def display(self,index):
        self.index=index
        self.stackedWidget.setCurrentIndex(index)


    def initLibraryWindow(self):
        self.LWUI=AddLibraryPath.Ui_LSelect()
        self.LWin=QWidget()
        self.LWin.setWindowModality(Qt.ApplicationModal)#设置模态对话框
        self.LWUI.setupUi(self.LWin)
        self.LWUI.LibraryP.setText("")
        self.add1.clicked.connect(self.LWin.show)
        self.LWUI.L_Cancel.clicked.connect(self.LWin.close)
        self.LWUI.L_Workspace.clicked.connect(lambda: self.ShowDialog(1))
        self.LWUI.L_OK.clicked.connect(self.AddLibraryPath)
        self.del1.clicked.connect(self.DelLibraryPath)


        self.lWUI = Enterlibraries.Ui_LSelect()
        self.lWin = QWidget()
        self.lWin.setWindowModality(Qt.ApplicationModal)
        self.lWUI.setupUi(self.lWin)
        self.LWUI.LibraryP.setText("")
        self.add2.clicked.connect(self.lWin.show)
        self.lWUI.l_OK.clicked.connect(self.AddLibraries)
        self.lWUI.l_Cancel.clicked.connect(self.lWin.close)
        self.del2.clicked.connect(self.DelLibraries)





    def KillProcess(self):
        #self.process.kill()

        #self.process.pid
        os.system(r"taskkill /f /t /im make.exe")

        self.Result.append('用户终止执行')


    def ChooseProDir(self):
        dir=QFileDialog.getExistingDirectory()
        dir=dir.replace('/','\\')
        self.ProjectName_2.setText(dir)

        if dir!='':
            os.chdir(dir)

            import automake_config as ac
            (DebugName, HighTecDir, CCFLAG, LINKFLAG, includepath, excludefiles, g_except_dir_list,
             g_except_file_list,LibraryPath,libraties) = ac.maininit()
            self.includepath=includepath
            self.excludefiles=excludefiles
            self.DebugName=DebugName
            self.CCFLAG=CCFLAG
            self.LINKFLAG=LINKFLAG
            self.HighTecDir=HighTecDir
            self.PROJECTDIR=dir
            self.LibraryPath=LibraryPath
            self.libraties=libraties
            #print(os.getcwd())
            self.AllPath=ac.FindAllPath(dir)
            #print(self.AllPath)
            self.initDialog()
            #对Dialog按钮的设置
            self.fileselect.buttonBox.accepted.connect(self.GetPath)
            self.fileselect.treeWidget.setSelectionMode(3)
            self.fileselect.buttonBox.rejected.connect(self.Cleartree)

            #self.adds(dir,self.child0)
            a.initUI()


    def initDialog(self):
        self.di = QDialog()
        fileselect1 = self.fileselect
        fileselect1.setupUi(self.di)
        # self.di.show()


        child0 = QTreeWidgetItem(fileselect1.treeWidget)
        child0.setText(0, self.DebugName)
        child0.setIcon(0, QIcon('./Compile/01.png'))

        self.adds(os.getcwd(), child0)
        child1 = QTreeWidgetItem(child0)
        child1.setText(0, 'TOOLS')
        child1.setIcon(0, QIcon('./Compile/01.png'))

        #展开所有节点
        fileselect1.treeWidget.expandAll()
    def showContextMenu(self,id):
              # 如果有选中项，则显示显示菜单

            #if id==1:
            items1 = self.includeList.selectedIndexes()

                #self.idRm=id
            #print(items)
            #elif id==2:
            items2 = self.excludeList.selectedIndexes()

                #self.idRm = id

            if items1 or items2:

                self.contextMenu.show()
                #self.f=QPoint
                self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def remove(self):
        items1 = self.includeList.selectedIndexes()
        items2 = self.excludeList.selectedIndexes()
        if self.index==3:
            if items1:
                for jj in items1:
                    self.includeList.removeItemWidget(self.includeList.takeItem(jj.row()))
        if self.index == 4:
            if items2:
                for jj in items2:

                    self.excludeList.removeItemWidget(self.excludeList.takeItem(jj.row()))




    def EndResult(self):
        print(os.getcwd())
        f=open('./conerr.err','r')
        lines=f.readlines()
        j=0
        for ii in lines:
            if "error:"in ii:
                self.Result.append("<font color=\"#FF0000\">%s</font> "%ii)
                j=1
        if j!=1:
            self.Result.append("<font color=\"#FF0000\">finished!!!!!!!!</font> ")
            self.barlabel.setText('已完成')
        f.close()
        os.remove('./conerr.err')
        self.backend.working=False
        self.statusBar.removeWidget(self.progressBar)
        self.barlabel.setText('准备中')
        os.chdir(self.ProjectName_2.text())





    def initBar(self):
        global NUM
        self.progressBar = QProgressBar()
        self.Result.clear()
        self.barlabel.setText('正在编译：')
        self.statusBar.addPermanentWidget(self.progressBar, stretch=2)
        f = open('./Default/Default.objectlist','r')
        lines = f.readlines()
        f.close()
        NUM=len(lines)
        #self.progressBar.setGeometry(0,0,100,5)
        self.progressBar.setRange(0,len(lines))
        global VAL
        VAL=0


    def SetProgressBarVal(self,val):
        #global VAL

        n=VAL+val
        self.progressBar.setValue(n)
    def StartCompile(self,Hdir):


        global cmd1
        #cmd1 = r'''%s\bin\make -j8 all >console.log 2>&1''' % Hdir
        cmd1 = r'''%s\bin\make -j8 all''' % Hdir
        #cmd1 = self.startpath+'\Compile\compile.bat  '+Hdir
        # cmd1='cd ..'
        # print(includepath)
        # self.process =subprocess.Popen(self.startpath+ '\Compile\compile.bat ' + cmd1)

        os.chdir(self.ProjectName_2.text() + '/Default')
        #f=open('ccccc.txt','w')
        #self.process = subprocess.Popen(cmd1)


        self.backend1 = BackendTread1()
        self.backend1.startcompile1.connect(self.PrintConsole)
        self.backend1.endSig.connect(self.EndResult)
        #time.sleep(3)
        self.backend1.start()
        self.backend = BackendTread()
        self.backend.setvalue.connect(self.SetProgressBarVal)
        #self.backend.endSig.connect(self.EndResult)
        # time.sleep(3)

        self.backend.start()



        '''self.process = subprocess.call(cmd1)
        self.process.wait()
        f= open('console.log','r')
        lines =f.readlines()
        for  ii in lines:
            if 'error:'in ii:
                self.Result.insertText(ii+'\n')'''
        #os.chdir(self.ProjectName_2.text())


    def PrintConsole(self,r):
        #print(2222)
         # None表示正在执行中
        #r = self.process.stdout.readline()
            #self.Result.append(r)
        self.Result.append("<font color=\"#000000\">%s</font> "%r)
            #self.backend.stopSig()
              # 可修改输出方式，比如控制台、文件等

        #print(self.process.poll())

        # 重定向错误输出


    def checkFLAG(self):
        CCFLAG1 = self.GCCFLAGName.toPlainText()
        #CCFLAG1 = CCFLAG1[0:len(CCFLAG1) - 1]
        LINKFLAG1 = self.LINKFLAGName.toPlainText()
        #LINKFLAG1 = LINKFLAG1[0:len(LINKFLAG1) - 1]
        Hdir = self.HithTecDir.text()
        DebugName1 = self.ProjectName.text()

        inn=self.includeList.count()
        inpath=[]
        exn = self.excludeList.count()
        expath = []
        for i in range(inn):
            inpath.append(self.includeList.item(i).text())
        for i in range(exn):
            expath.append(self.excludeList.item(i).text())

        #print(CCFLAG1)
        # POSTBUILD1 = pb.get()
        # Hdir = Hdir[0:len(Hdir) - 1]
        #if CCFLAG1 != self.CCFLAG or self.LINKFLAG != LINKFLAG1 or Hdir != self.HighTecDir or DebugName1 != self.DebugName or expath != self.excludefiles or inpath != self.includepath:
        self.modifyFLAG()
        '''for i in range(0,len(CCFALG)):
                if CCFALG1[i]!=CCFALG[i]:
                    print(i)'''
        cmd=self.startpath+'\Compile\python  '+self.startpath+"\Compile/automake.py "+self.startpath
        a=subprocess.call(cmd)
        self.initBar()
        #a.wait()
        #cmd1 = Hdir + r'\bin\make'

        #self.backend.update_date.connect(self.handleDisplay)
        try:
            self.StartCompile(Hdir)
        except BaseException as e:
            print(333333)
            f=open('cons.log','w')
            f.write(e.args)
            f.close()
        #def


    def modifyFLAG(self):
        # f=open('./TOOLS/Compile/automake_config.py','r',encoding='utf-8')
        CCFLAGNOW = self.GCCFLAGName.toPlainText()
        # CCFLAG1 = CCFLAG1[0:len(CCFLAG1) - 1]
        LINKFLAGNOW = self.LINKFLAGName.toPlainText()
        # LINKFLAG1 = LINKFLAG1[0:len(LINKFLAG1) - 1]
        HighTecDirNOW = self.HithTecDir.text()
        DebugNameNOW = self.ProjectName.text()

        inn = self.includeList.count()
        inpathNOW = []
        exn = self.excludeList.count()
        expathNOW = []
        Ln = self.Llist.count()
        LnNOW = []
        ln = self.llist.count()
        lnNOW = []
        try:
            for i in range(inn):
                inpathNOW.append(self.includeList.item(i).text())
            for i in range(exn):
                expathNOW.append(self.excludeList.item(i).text())
            f = open('./py.pyconfig', 'w', encoding='utf-8')
            # lines=f.readlines()
            tLink = re.split(' ',LINKFLAGNOW)
            Linkchange=''
            for iii in tLink:
                if '-L' not in iii and '-l:' not in iii:
                    Linkchange+=iii+' '

            for i in range(Ln):
                p = re.split('{workspace}/',self.Llist.item(i).text())
                #print(p)
                if len(p)==1:
                    Linkchange+='''-L"'''+os.path.abspath(p[0])+'''" '''
                else:
                    Linkchange += '''-L"''' + os.path.abspath(p[1]) + '''" '''
                LnNOW.append(self.Llist.item(i).text())
            for i in range(ln):
                Linkchange+='-l'+self.llist.item(i).text()+' '
                lnNOW.append(self.llist.item(i).text())


            f.write('CCFLAG=' + CCFLAGNOW + "\n")
            f.write('LINKFLAG=' + Linkchange + "\n")
            f.write('HighTecDir=' + HighTecDirNOW + "\n")
            f.write('DebugName=' + DebugNameNOW + "\n")
            aa = "includepath="
            for a in inpathNOW:
                if a != "":
                    aa += a + ','
            f.write(aa + '\n')
            bb = "excludefiles="
            for b in expathNOW:
                if b != "":
                    bb += b + ','
            f.write(bb + '\n')
            cc = "LibraryPath="
            for c in LnNOW:
                if c != "":
                    cc += c + ','
            dd = "libraties="
            for d in lnNOW:
                if d != "":
                    dd += d + ','
            f.write(cc + '\n')
            f.write(dd + '\n')
            f.close()
            self.LINKFLAGName.setText('')
            self.LINKFLAGName.setText(Linkchange)
        except:
            f.close()



    def CleanProject(self):
        print('Cleanning project...... ')
        if os.path.exists('./Default'):
            shutil.rmtree('./Default')
        if os.path.exists('./delivery'):
            shutil.rmtree('./delivery')
        QMessageBox.about(self, "消息", "Clean has finished!")
        #tkinter.messagebox.showinfo('提示','Clean has finished!')
        print('Clean has finished!')

    def testaa(self):
        print("1")


    def CloseTools(self):
        print(1)
    def delPath(self,id):
        if id==1:
            self.includeList.clear()
        if id == 2:
            self.excludeList.clear()


    def ShowDialog(self,id):
        #self.di=QDialog()
        #fileselect1 = fileselect.Ui_Dialog()
        #fileselect1.setupUi(self.di)
        self.idPath=id
        self.di.exec()



            # for path,dir,files in os.walk(os.getcwd()):
            # for file in files:
            #    i=i+1
            # if file.endswith('.h')  and  "TOOLS" not in path:
            #    if "TOOLS" not in path:
            #        a='child'+str(i)
            #        a=QTreeWidgetItem(child0)

    def adds(self,paths, root):

        if os.path.isdir(paths):
            list = os.listdir(paths)
            for i in list:
                # j=0
                # for path1 ,dirs,files in os.walk(os.path.join(paths,i)):
                #    for file in files:
                #        if file.endswith('.h') or file.endswith('.c'):
                #            j=1

                if 'Default' not in i  and '.' not in i and '_pycache_' not in os.path.join(paths,i) and os.path.join(
                    paths, i) in self.AllPath:
                    # self.adds(os.path.join(paths, i),root)
                    if os.path.isdir(os.path.join(paths, i)):
                        childs = QTreeWidgetItem(root)
                        childs.setText(0, i)
                        childs.setIcon(0, QIcon('./Compile/01.png'))
                        self.adds(os.path.join(paths, i), childs)





        #注意：是对QDialog对象show()，并不是自己生成的Ui_Dialog对象 show()，开始没有写self.di，弹窗总是一闪而过，类的的函数加上self之后成功
        #print(QFileDialog.getExistingDirectory(None, "请选择要添加的文件", os.getcwd()))
    def GetPath(self):
        if self.index==3:
            pathlist = self.fileselect.treeWidget.selectedItems()
            # pathlist = QTreeWidgetItemIterator(self.fileselect.treeWidget)
            # print(pathlist.value().childCount())
            tempinclude = []
            for pathss in pathlist:
                tpathss = pathss
                tp = ""
                while 1:
                    if tpathss.text(0)!=self.DebugName:
                        tp = tpathss.text(0) + tp
                    if tpathss.parent():
                        tpathss = tpathss.parent()
                        tp = '/' + tp
                    else:
                        break
                if tp not in tempinclude and tp!="":
                    tempinclude.append(tp)
                    pathss.setSelected(False)


            self.includeList.addItems(sorted(tempinclude))



        elif self.idPath==2:
            pathlist = self.fileselect.treeWidget.selectedItems()
            #pathlist = QTreeWidgetItemIterator(self.fileselect.treeWidget)
            #print(pathlist.value().childCount())
            tempexclude=[]
            for pathss in pathlist:
                tpathss=pathss
                tp=""
                while 1:
                    if tpathss.text(0) != self.DebugName:
                        tp = tpathss.text(0)+tp
                    if tpathss.parent():
                            tpathss=tpathss.parent()
                            tp='/'+tp
                    else:
                            break
                if  tp not in tempexclude and tp!="":
                    tempexclude.append(tp)

            self.excludeList.addItems(sorted(tempexclude))


        elif self.index==2:
            pathlist = self.fileselect.treeWidget.selectedItems()
            # pathlist = QTreeWidgetItemIterator(self.fileselect.treeWidget)
            # print(pathlist.value().childCount())
            tempexclude = []
            for pathss in pathlist:
                tpathss = pathss
                tp = ""
                while 1:
                    if tpathss.text(0) != self.DebugName:
                        tp = tpathss.text(0) + tp
                    if tpathss.parent():
                        tpathss = tpathss.parent()
                        tp = '/' + tp
                    else:
                        break
                if tp not in tempexclude and tp != "":
                    tempexclude.append("{workspace}"+tp)
                    pathss.setSelected(False)


            self.Llist.addItems(tempexclude)
            self.LWin.close()#如果是通过workspace选的直接关掉选择框




        self.di.close()
        '''for selectedPath in pathlist:
                
                print(selectedPath.text(0))
            print(pathlist)'''
            #if pathlist.value().checkState(0) == Qt.Checked:


            #n=self.fileselect.treeWidget.topLevelItemCount()



        '''while pathlist.value():
                if pathlist.value().checkState(0)==Qt.Checked:
                    print(pathlist.value.text(0))
                    break'''
    def Cleartree(self):
        pathlist = self.fileselect.treeWidget.selectedItems()
        for pathss in pathlist:
            pathss.setSelected(False)
        self.di.close()

    def AddExpath(self):
        dir1,file1 = QFileDialog.getOpenFileNames (self,'选择过滤文件',os.getcwd(),"C FILES(*.c)")
        #print(dir1,file1)
        for ii in dir1:
            if ii!='' :
                dir2 = re.split(os.getcwd().replace('\\','/'),ii)[1]
                self.excludeList.addItem(dir2)

    #Library的具体操作
    def AddLibraryPath(self):
        txt=self.LWUI.LibraryP.text()
        if txt:
            self.Llist.addItem(txt)
        self.LWin.close()
    def AddLibraries(self):
        txt = self.lWUI.libraries.text()
        if txt:
            self.llist.addItem(txt)
        self.lWin.close()
    def DelLibraryPath(self):
        items1 = self.Llist.selectedIndexes()
        if items1:
            for jj in items1:
                self.Llist.removeItemWidget(self.Llist.takeItem(jj.row()))
    def DelLibraries(self):
        items1 = self.llist.selectedIndexes()
        if items1:
            for jj in items1:
                self.llist.removeItemWidget(self.llist.takeItem(jj.row()))

if __name__ == '__main__':
    cmd1 = ""
    NUM=0
    VAL=0
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./Compile/mainwindowIcon.png'))

    a=basePage()

    a.ChooseProDir()



    a.show()

    #进入程序的主循环，并通过exit函数确保主循环安全结束
    sys.exit(app.exec_())