from datetime import datetime
import calendar
import requests
import zipfile
import bs4
import os


class GetOEM:
    def __init__(self):
        self.WebPath = "https://www.cmse.gov.cn/gfgg/zgkjzgdcs/"
        self.r = None
        self.bs = None
        self.Child_one = None
        self.Child_two = None
        self.Child_three = None
        self.WebFilePath = None
        self.WebFile = None
        self.zip_path = None
        self.content = None
        self.WebFileName = None

        self.path = os.getcwd()
        self.file = None
        self.files = None
        self.utc_time = None

        self.CCSDS_OEM_VERS = "2.0"
        self.CREATION_DATE = None
        self.ORIGINATOR = "BACC"
        self.OBJECT_NAME = "KJZ"
        self.OBJECT_ID = "CSS"
        self.CENTER_NAME = "EARTH"
        self.REF_FRAME = "EME2000"
        self.TIME_SYSTEM = "UTC"
        self.START_TIME = None
        self.STOP_TIME = None
        self.unit_coordinate = "km"
        self.unit_velocity = "km/s"
        self.OEMdata = []

    def solve(self, utc_time):
        self.utc_time = utc_time
        for i in range(6):
            self.utc_time[i] = int(float(self.utc_time[i]))
        # 确保年月日时分秒都是数字
        if self.utc_time[-1] == 59:
            self.utc_time[-2] += 1
            self.utc_time[-1] = 0
        # 处理秒的进位
        if self.utc_time[-2] == 60:
            self.utc_time[-3] += 1
            self.utc_time[-2] = 0
        # 处理分的进位
        if self.utc_time[-3] == 24:
            self.utc_time[2] += 1
            self.utc_time[-3] = 0
        # 处理时的进位
        if self.utc_time[2] > calendar.monthrange(self.utc_time[0], self.utc_time[1])[1]:
            self.utc_time[1] += 1
            self.utc_time[2] = 1
        # 处理日的进位，考虑月份天数
        if self.utc_time[1] > 12:
            self.utc_time[0] += 1
            self.utc_time[1] = 1
        # 处理月的进位
        # print(utc_time)
        temporary_variables = datetime(self.utc_time[0], self.utc_time[1], self.utc_time[2], self.utc_time[3], self.utc_time[4], self.utc_time[5])
        timestamp = int(temporary_variables.timestamp())
        return timestamp

    def Crawling(self):
        self.r = requests.get(self.WebPath,'lxml')
        self.r.encoding = 'utf-8'
        # print(self.r.text)

        self.bs = bs4.BeautifulSoup(self.r.text, "lxml")
        self.Child_one = self.bs.find('div',attrs={'class':'TRS_Editor'})
        self.Child_two = str(self.Child_one.find("a")).split(" ")[1]
        self.Child_three = str(self.Child_two)[7:-1]  # 官方zip文件网址后半段
        self.WebFilePath = self.WebPath + self.Child_three
        # print(self.WebFilePath)

        self.WebFile = requests.get(self.WebFilePath)
        self.zip_path = self.path + "\\OEM_File.zip"
        with open(self.zip_path, 'wb') as f:
            f.write(self.WebFile.content)
        # 保存zip文件到工作目录

        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.path)
        os.remove("OEM_File.zip")
        # 解压并删除多余文件

        self.WebFileName = self.Child_one.find("a").get_text()[:-4]
        with open(self.WebFileName + ".dat", "r") as dat_file:
            self.content = dat_file.read()
        with open(self.WebFileName + ".txt", "w") as txt_file:
            txt_file.write(self.content)
        os.remove(self.WebFileName + ".dat")
        # 改写dat为txt并删除多余文件

        GetOEM.GetFile(self)
        # 重新解析文件

    def save(self, Filename):
        with open(Filename, 'r') as f:
            lines = f.readlines()
            self.CREATION_DATE = lines[1][19:]
            sta_t = lines[10][19:].split('T')[0].split('-') + lines[10][19:].split('T')[1].split(':')
            sta_t[-1] = sta_t[-1][:-2]
            sto_t = lines[11][19:].split('T')[0].split('-') + lines[11][19:].split('T')[1].split(':')
            sto_t[-1] = sto_t[-1][:-2]
            self.START_TIME = GetOEM.solve(self, sta_t)
            self.STOP_TIME = GetOEM.solve(self, sto_t)

            child_list_two = []
            for i in range(15, len(lines)):
                child_list_two.clear()
                child_list_one = lines[i].split(' ')
                for j in child_list_one:
                    if j != '':
                        child_list_two.append(j)

                _utc_time = child_list_two[0]
                utc_time_left = _utc_time[:10]
                utc_time_right = _utc_time[11:]

                utc_time_left = utc_time_left.split('-')
                utc_time_right = utc_time_right.split(':')
                _utc_time = GetOEM.solve(self, utc_time_left + utc_time_right)
                # print(solve(_utc_time))

                temporary1 = (float(child_list_two[1]), float(child_list_two[2]), float(child_list_two[3]))
                temporary2 = (float(child_list_two[4]), float(child_list_two[5]), float(child_list_two[6][:-1]))
                temporary = [_utc_time, temporary1, temporary2]
                # print(temporary)

                self.OEMdata.append(temporary)
        # print(self.OEMdata)

    def Get(self, t):
        for i in self.OEMdata:
            if i[0] == t:
                return i

    def GetFile(self):
        self.file = os.listdir(self.path)
        self.files = []
        for i in self.file:
            if "_OEM_" in i:
                self.files.append(i)
        # print(self.files)

        if len(self.files) != 0:
            if len(self.files) == 1:
                file = self.files[0]
            else:
                year = []
                for i in self.files:
                    year.append(int(i[8:-9]))
                file = str(max(year))
                for i in self.files:
                    if file in i:
                        file = i
                        break
            # 获取最新文件
            GetOEM.save(self,file)
        else:
            GetOEM.Crawling(self)
