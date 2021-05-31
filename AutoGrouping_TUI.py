import os
import argparse
import time
from os import path as p

def ReadCsv(path):
    with open(path) as txt:
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
        if(len(GroupMember) == 4):
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
    
    with open(NewCsv,'w') as csv:
        for n_line in table:
            csv.write(n_line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path",type=str,default="/Users/szchandler/Desktop/VScodePy/HaSir/data.csv")
    parser.add_argument("--out_path",type=str,default="/Users/szchandler/Desktop/VScodePy/HaSir/")
    parser.add_argument("--ZeroTable",type=list,default=[])
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
    Group2CSV(Groups,arg.out_path)
