#!/usr/bin/env python3  
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from lib.ui_main import Ui_Main 
import os 
from pathlib import Path
import time 



class MainClass(QWidget,Ui_Main):
  
    def __init__(self,parent=None):
        
        self.os= 'linux'
        self.templatpath = '/opt/tools/PayClip/templates' 
        self.listoftemplets = []
        
        self.valide = False 
        self.alreadycoped = False
        QWidget.__init__(self,parent=parent)

        self.setupUi(self)


        self.treeWidget.itemClicked.connect(self.getpayloads)
        self.listWidget.itemClicked.connect(self.CopyToClip)
        self.setIcon('/opt/tools/PayClip/icon/icon.png')
        self.PrepareTreelist()
       
        self.lineEdit.returnPressed.connect(self.CopyToClipCmd)
        self.lineEdit.textChanged.connect(self.CopyByCmd)
    
    def testing(self) : 
        print("its oky ")
    def setIcon(self,iconpath):
        appIcon = QIcon(iconpath)
        self.setWindowIcon(appIcon)

    def GetTemplets(self) :
        return sorted(Path(self.templatpath).iterdir(), key=os.path.getmtime)
    def PrepareTreelist(self) : 
        self.treeWidget.clear()
        
        for filename in  self.GetTemplets(): 

            item_tf= QTreeWidgetItem(self.treeWidget)
            item_tf.setText(0, filename.name)
            self.listoftemplets.append(filename.name)
    def AfListpayload(self,filepath) : 
        self.listWidget.clear()
        readf = open(filepath,'r') 
        indx=1
        for payloads in readf.readlines() : 

            if payloads[0] == '#' or payloads.strip() == '' :
                qlistitem = QListWidgetItem(self.listWidget)
                qlistitem.setText(payloads.strip()) 
                qlistitem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                qlistitem.setForeground(QColor(150,150,150))
                qlistitem.setBackground(QColor(50, 68, 168))
                
            else :
                textobject = payloads.split("<->")
                qlistitem = QListWidgetItem(self.listWidget)
                
                qlistitem.setText(str(indx)+"::"+textobject[0].strip()) 
                if len(textobject) > 1 :
                    qlistitem.setToolTip(textobject[1].strip())
                indx+=1
            
    def getpayloads(self,itm) :
        self.AfListpayload(self.templatpath+'/'+itm.text(0))
        
    def CopyToClip(self,itm) :
        if itm.text()[0] !=  '#': 
            itm.setSelected(False)
            payload_ = itm.text().split("::")[1]
            print("Copied successfully ")
            QApplication.clipboard().setText(payload_)
            time.sleep(0.1)
    
    def CopyByCmd(self) : 
        
        self.Changebackground(0)
        cmdtxt = self.lineEdit.text() 
        indx = -1 
        if ":" in  cmdtxt : 
            try : 
                ll = cmdtxt.split(":")
                templatename =  ll[0]
                sindx = ll[1]
                
                if len(sindx) > 0 : 
                    indx = int(sindx)
                
               
                if templatename in self.listoftemplets : 
                    
                    
                    
                    self.AfListpayload(self.templatpath+'/'+templatename)
                    
                    if indx > self.listWidget.count() : 
                        self.Changebackground(0)
                    else : 
                        myitme = self.listWidget.item(indx-1)
                        myitme.setSelected(True)
                        self.listWidget.setCurrentItem(myitme)
                         
                    self.Changebackground(1)
            except : 
                self.Changebackground(0)
                self.notifyme("please enter int ")
   
    def CopyToClipCmd(self) : 
        if self.valide : 
            itm=self.listWidget.currentItem() 
            itm.setSelected(False)
            payload_ = itm.text().split("::")[1]
            print("Copied successfully ")
            QApplication.clipboard().setText(payload_)
            time.sleep(0.1)
            self.lineEdit.setStyleSheet("""
                        border-style : none ; """ ) 
            self.alreadycoped = True
            self.lineEdit.setText("")
             
    def Changebackground(self,indx=0) : 
        if self.alreadycoped  : 
            self.lineEdit.setStyleSheet("""
                        border-style : none ; """ ) 
            return 0 
        if indx == 0 : 
            self.valide = False 
            self.alreadycoped = False
            self.lineEdit.setStyleSheet("""
                        border-style : solid ; 
                        border-width:2px;
                        border-color : #EB3737;

                    """) 
        elif indx == 1 : 
           self.valide = True 
           self.lineEdit.setStyleSheet("""
                        border-style : solid ; 
                        border-width:2px;
                        border-color : #66f542;

                    """) 
    
    def notifyme(self,str) : 
        print(str)

if __name__ == "__main__":
  import sys
  app = QApplication(sys.argv)
  MainWindow = MainClass()
  #ui = Ui_MainWindow()
  #ui.setupUi(MainWindow)
  MainWindow.show()
  sys.exit(app.exec_())
