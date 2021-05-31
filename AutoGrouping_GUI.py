# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################
import argparse
from os import path as p
import os
import time

def ReadCsv(path):
    with open(path,encoding='utf-8') as txt:
        ReturnTxt = txt.readlines()
    return ReturnTxt

class Student:
    def __init__(self,name,sex,sumgrades):
        self.Name = name
        self.Sex = sex
        self.SumGrades = sumgrades

class Group:
    def __init__(self,s1=None,s2=None,s3=None,s4=None,s5=None):
        self.student1 = s1
        self.student2 = s2
        self.student3 = s3
        self.student4 = s4
        self.student5 = s5
    def PermitSex (self):
        key = 0
        if(self.student2 != None):
            key += self.student1.Sex + self.student2.Sex
        if(self.student3 != None):
            key += self.student3.Sex
        if(self.student4 != None):
            return 3#组别已满
        if(self.student3 != None):
            if(key == 1):
                return 1 #缺女生
            elif(key == 2):
                return 0 #缺男生
            else:
                return 2 #放弃治疗
        elif(key == 0):
            return 1 #缺女生
        elif(key == 2):
            return 0#缺男生
        elif(key == 1):
            return 2#男女皆可

    def Print(self):
        if(self.student5 != None):
            print("Group of {},{},{},{},{}".format(self.student1.Name,self.student2.Name,self.student3.Name,self.student4.Name,self.student5.Name))
        elif(self.student4 != None):
            print("Group of {},{},{},{}".format(self.student1.Name,self.student2.Name,self.student3.Name,self.student4.Name))
        elif(self.student3 != None):
            print("Group of {},{},{}".format(self.student1.Name,self.student2.Name,self.student3.Name))
        
    def GetAvg(self):
        if(self.student5 != None):
            GroupAvg = (self.student1.SumGrades + self.student2.SumGrades + self.student3.SumGrades + self.student4.SumGrades + self.student5.SumGrades) /5
            mess = {self.student1.Name:self.student1.SumGrades,self.student2.Name:self.student2.SumGrades,self.student3.Name:self.student3.SumGrades,self.student4.Name:self.student4.SumGrades,self.student5.Name:self.student5.SumGrades}
            # print("Group of {},{},{},{},{},{}".format(self.student1.Name,self.student2.Name,self.student3.Name,self.student4.Name,self.student5.Name,GroupAvg))
        elif(self.student4 != None):
            GroupAvg = (self.student1.SumGrades + self.student2.SumGrades + self.student3.SumGrades + self.student4.SumGrades) /4
            mess = {self.student1.Name:self.student1.SumGrades,self.student2.Name:self.student2.SumGrades,self.student3.Name:self.student3.SumGrades,self.student4.Name:self.student4.SumGrades}
            # print("Group of {},{},{},{},{}".format(self.student1.Name,self.student2.Name,self.student3.Name,self.student4.Name,GroupAvg))
        elif(self.student3 != None):
            GroupAvg = (self.student1.SumGrades + self.student2.SumGrades + self.student3.SumGrades) /3
            mess = {self.student1.Name:self.student1.SumGrades,self.student2.Name:self.student2.SumGrades,self.student3.Name:self.student3.SumGrades}
            # print("Group of {},{},{},{}".format(self.student1.Name,self.student2.Name,self.student3.Name,GroupAvg))
        return GroupAvg, mess

def AnaTxT(txt):
    NewTxT = []
    title_line = txt[0].replace(',,','').replace("\ufeff",'').replace("\n",'').split(',')
    for num in range(2,len(txt)):
        line = txt[num]
        line = line.replace('\n','').split(',')
        NewTxT.append(line)
    return title_line, NewTxT

def ClearZero(title,data,keys):
    DataDict = {}
    new_data = []
    LenSum = len(title) - 2 - len(keys)
    for t in title:
        DataDict[t] = True
    for line in data:
        new_dict = DataDict.copy()
        for num,mess in enumerate(line):
            new_dict[title[num]] = mess
        new_data.append(new_dict)
    for k in keys:
        right = 1
        for person in new_data:
            try:
                if(k in person):
                    person[k] = 0
            except:
                continue
        for i in person:
            if(k == i):
                right = 0
                break
        if(right == 1):
            LenSum += 1
    return new_data,LenSum

def AnaDict(title,data,lenkey):
    FinalData = []
    sexKey = {"男":0,"女":1}
    for d in data:
        name = d[title[0]]
        sex = sexKey[d[title[1]]]
        totalGrades = 0
        for num in range(2,len(title)):
            totalGrades += float(d[title[num]])
        AverageGrades = totalGrades/lenkey
        FinalData.append([name,sex,AverageGrades])
    return FinalData

def Login(datas):
    ReturnDatas = []
    for data in datas:
        PersonData = Student(data[0],data[1],data[2])
        # ReturnDatas.append(PersonData.output())
        ReturnDatas.append(PersonData)

    return ReturnDatas

def MakeGroups(Datas):
    if(len(Datas) % 2 == 0):
        mid = int(len(Datas) / 2)
    else:
        mid = int((len(Datas)-1)/2)
    GroupsNum = int(len(Datas) / 4)
    StillPerson = len(Datas) % 4
    #mid为第二组开始的由0开始计数的编号
    removebox = []
    GroupBox = []
    for i in range(mid):
        if(i == GroupsNum):
            break
        else:
            p1 = Datas[i]
            removebox.append(p1)
            p2 = Datas[len(Datas)-1-i]
            removebox.append(p2)
            NewGroup = Group(p1,p2)
            GroupBox.append(NewGroup)
    for rem in removebox:
        Datas.remove(rem)
    return Datas,GroupBox

def AppendThird(Datas,Groups,breaknum):
    Geted = []
    for group in Groups:
        SexKey = group.PermitSex()
        NumTimes = 0
        ramlog = []
        if(len(Datas)-len(Geted) <= breaknum):
            breaknum = len(Datas) - len(Geted) -1
        for num in range(len(Datas)):
            NumTimes += 1
            guy = (Datas[len(Datas) - 1 - num])
            if(guy not in Geted):
                ramlog.append(guy)
                if(SexKey == 2):
                    group.student3 = guy
                    Geted.append(guy)
                    break
                elif(SexKey == guy.Sex):
                    group.student3 = guy
                    Geted.append(guy)
                    break
                else:
                    if(NumTimes >= breaknum):
                        group.student3 = ramlog[0]
                        Geted.append(ramlog[0])
                        break
                    continue

    for guys in Geted:
        Datas.remove(guys)
    return Datas,Groups

def AppendFourth(Datas,Groups,breaknum):
    Geted = []
    for group in Groups:
        SexKey = group.PermitSex()
        NumTimes = 0
        ramlog = []
        if(len(Datas)-len(Geted) <= breaknum):
            breaknum = len(Datas) - len(Geted) -1
        for num in range(len(Datas)):
            NumTimes += 1
            guy = (Datas[len(Datas) - 1 - num])
            if(guy not in Geted):
                ramlog.append(guy)
                if(SexKey == 2):
                    group.student4 = guy
                    Geted.append(guy)
                    break
                elif(SexKey == guy.Sex):
                    group.student4 = guy
                    Geted.append(guy)
                    break
                else:
                    if(NumTimes >= breaknum):
                        group.student4 = ramlog[0]
                        Geted.append(ramlog[0])
                        break
                    continue
    for guys in Geted:
        Datas.remove(guys)
    return Datas,Groups

def AppendFifth(Datas,Groups):
    for num in range(len(Datas)):
        keynum = (len(Datas) - 1 - num)
        Groups[num].student5 = Datas[keynum]
    return Groups

def GetZero(keysbox):
    ZeroKeys = []
    ClassDict = ["语文","数学","英语","物理","历史","化学","思想政治"]
    for num, c in enumerate(ClassDict):
        if(keysbox[num] == True):
            ZeroKeys.append(c)
    return ZeroKeys

def Group2CSV(Groups,path_use):
    table = []
    for num,group in enumerate(Groups):
        GroupAvg, GroupMember = group.GetAvg()
        GroupNum = "Group{}".format(num+1)
        LineBox = []
        LineBox.append(GroupNum)
        for guy in GroupMember:
            LineBox.append(guy)
            LineBox.append(str(round(GroupMember[guy],2)))
        if(len(GroupNum) == 4):
            LineBox.append("")
            LineBox.append("")
        LineBox.append("组平均成绩")
        LineBox.append(str(round(GroupAvg,2)))
        line = ""
        for i in range(len(LineBox)):
            line += LineBox[i]
            if(i != len(LineBox)-1):
                line += ','
            else:
                line += '\n'
        table.append(line)
    NowTime = (time.localtime(time.time()))
    FileName = str(NowTime.tm_year) + str(NowTime.tm_mon) + str(NowTime.tm_mday) + str(NowTime.tm_hour) +str(NowTime.tm_min) + str(NowTime.tm_sec)+".csv"
    NewCsv = p.join(path_use,FileName)
    
    with open(NewCsv,'w',encoding='utf-8') as csv:
        for n_line in table:
            csv.write(n_line)
    return 1

class MyFrame1 ( wx.Frame ):
    
    def __init__( self, parent):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"班级自动分组程序(初中版)", pos = wx.DefaultPosition, size = wx.Size( 605,186 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.InputText = wx.StaticText( self, wx.ID_ANY, u"原表格地址", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.InputText.Wrap( -1 )

        gbSizer1.Add( self.InputText, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

        self.Input_Ctrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
        gbSizer1.Add( self.Input_Ctrl, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.OpenDir_button1 = wx.Button( self, wx.ID_ANY, u"打开文件夹", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer1.Add( self.OpenDir_button1, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


        bSizer1.Add( gbSizer1, 0, wx.EXPAND, 5 )

        gbSizer11 = wx.GridBagSizer( 0, 0 )
        gbSizer11.SetFlexibleDirection( wx.BOTH )
        gbSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.OutputText = wx.StaticText( self, wx.ID_ANY, u"输出表地址", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.OutputText.Wrap( -1 )

        gbSizer11.Add( self.OutputText, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

        self.Output_Ctrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
        gbSizer11.Add( self.Output_Ctrl, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.OpenDir_button2 = wx.Button( self, wx.ID_ANY, u"打开文件夹", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer11.Add( self.OpenDir_button2, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


        bSizer1.Add( gbSizer11, 0, wx.EXPAND, 5 )

        gbSizer111 = wx.GridBagSizer( 0, 0 )
        gbSizer111.SetFlexibleDirection( wx.BOTH )
        gbSizer111.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.ZeroText = wx.StaticText( self, wx.ID_ANY, u"忽略的科目", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ZeroText.Wrap( -1 )

        gbSizer111.Add( self.ZeroText, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

        self.CN_checkBox = wx.CheckBox( self, wx.ID_ANY, u"语文", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer111.Add( self.CN_checkBox, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.MA_checkBox = wx.CheckBox( self, wx.ID_ANY, u"数学", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer111.Add( self.MA_checkBox, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.EN_checkBox = wx.CheckBox( self, wx.ID_ANY, u"英语", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer111.Add( self.EN_checkBox, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.PY_checkBox = wx.CheckBox( self, wx.ID_ANY, u"物理", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer111.Add( self.PY_checkBox, wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.HI_checkBox = wx.CheckBox( self, wx.ID_ANY, u"历史", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer111.Add( self.HI_checkBox, wx.GBPosition( 0, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.CH_checkBox = wx.CheckBox( self, wx.ID_ANY, u"化学", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer111.Add( self.CH_checkBox, wx.GBPosition( 0, 6 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.PO_checkBox = wx.CheckBox( self, wx.ID_ANY, u"思想政治", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer111.Add( self.PO_checkBox, wx.GBPosition( 0, 7 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


        bSizer1.Add( gbSizer111, 0, wx.EXPAND, 5 )

        self.Start_button = wx.Button( self, wx.ID_ANY, u"开始处理", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.Start_button, 0, wx.ALL|wx.EXPAND, 5 )

        self.Prompt = wx.StaticText( self, wx.ID_ANY, u"暂无状态提示", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Prompt.Wrap( -1 )

        bSizer1.Add( self.Prompt, 0, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

		# Connect Events
        self.OpenDir_button1.Bind( wx.EVT_BUTTON, self.OpenDir_Click1 )
        self.OpenDir_button2.Bind( wx.EVT_BUTTON, self.OpenDir_Click2 )
        self.Start_button.Bind( wx.EVT_BUTTON, self.StartButton_Click )

    def __del__( self ):
        pass

	# Virtual event handlers, overide them in your derived class
    def OpenDir_Click1( self, event ):
        wildcard = 'All files(.csv)|.csv'
        dialog = wx.FileDialog(None,'select',os.getcwd(),'',wildcard,wx.FC_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            input_path = dialog.GetPath()
            self.Input_Ctrl.SetValue(input_path)
            output_path = p.dirname(input_path)
            self.Output_Ctrl.SetValue(output_path)
            dialog.Destroy

    def OpenDir_Click2( self, event ):
        dialog = wx.DirDialog(self,u"选择文件夹",style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            self.Output_Ctrl.SetValue(dialog.GetPath())
            dialog.Destroy

    def StartButton_Click( self, event ):
        ErrorKey = 0
        InputPath = self.Input_Ctrl.GetValue()
        OutputPath = self.Output_Ctrl.GetValue()
        check_key1 = self.CN_checkBox.GetValue()
        check_key2 = self.MA_checkBox.GetValue()
        check_key3 = self.EN_checkBox.GetValue()
        check_key4 = self.PY_checkBox.GetValue()
        check_key5 = self.HI_checkBox.GetValue()
        check_key6 = self.CH_checkBox.GetValue()
        check_key7 = self.PO_checkBox.GetValue()

        Zero_keys = [check_key1,check_key2,check_key3,check_key4,check_key5,check_key6,check_key7]

        ZeroTable = GetZero(Zero_keys)

        ####=========TUI Main===========###

        parser = argparse.ArgumentParser()
        parser.add_argument("--csv_path",type=str,default=InputPath)
        parser.add_argument("--out_path",type=str,default= OutputPath)
        parser.add_argument("--ZeroTable",type=list,default=ZeroTable)
        parser.add_argument("--Break",type=int,default=5)
        arg = parser.parse_args()

        txt = ReadCsv(arg.csv_path)
        Title, Data = AnaTxT(txt)
        DictData,lenkey = ClearZero(Title,Data,arg.ZeroTable)
        Students = AnaDict(Title,DictData,lenkey)
        StandardizedData = Login(Students)
        SortedData = sorted(StandardizedData,key=lambda keys:keys.SumGrades,reverse=True)
        RemainDatas,Groups = MakeGroups(SortedData)
        RemainDatas,Groups = AppendThird(RemainDatas,Groups,arg.Break)
        RemainDatas,Groups = AppendFourth(RemainDatas,Groups,arg.Break)
        if(len(RemainDatas) != 0):
            Groups = AppendFifth(RemainDatas,Groups)
        ErrorKey = Group2CSV(Groups,arg.out_path) 
        if(ErrorKey == 1):
            self.Prompt.SetLabelText("已经成功分组并输出表格至输出表地址")
        else:
            self.Prompt.SetLabelText("出现错误，请检查表格格式")

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame1(None)
    frame.Show()
    app.MainLoop()
