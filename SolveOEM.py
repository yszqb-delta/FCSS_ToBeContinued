from datetime import datetime
import math


class OEM:
    def __init__(self):
        self.UTC_time = None
        self.X = None
        self.Y = None
        self.Z = None
        self.X_DOT = None
        self.Y_DOT = None
        self.Z_DOT = None
        self.theta = None
        self.earth_angle = None
        # 关于OEM协议内容

        self.Alpha_radians = None
        self.Alpha_angle = None
        self.Alpha_long = None
        # 关于Alpha的变量

        self.Alpha_l = None
        self.Beta_radians = None
        self.Beta_angle = None
        self.Beta_quadrant = None
        self.Beta_long = None
        # 关于Beta的变量

        self.rotation_speed = 360 / (23 + (56 / 60) + (4.1 / 3600))  # 自转速度(°/h)
        self.rotation_time = 23 * 60 * 60 + 56 * 60 + 4.1  # 自转时间(s)
        self.earth_r = None
        self.a = 6378.137
        self.b = 6356.752314245
        # 关于地球的几个常量

    def Alpha(self):
        self.Alpha_radians = math.atan(abs(self.X) / abs(self.Y))  # 弧度制
        self.Alpha_angle = math.degrees(self.Alpha_radians)  # 角度制

        if self.Y > 0 and self.X > 0:
            self.Alpha_angle = 90 - self.Alpha_angle
        elif self.Y < 0 and self.X > 0:
            self.Alpha_angle = -1 * (90 - self.Alpha_angle)
        elif self.Y < 0 and self.X < 0:
            self.Alpha_angle = -1 * (90 + self.Alpha_angle)
        else:
            self.Alpha_angle = 90 + self.Alpha_angle
        # 该坐标系: y轴正方向向右、x轴正方向向下

        self.Alpha_long = math.sqrt(self.Y ** 2 + self.X ** 2)

        return [self.Alpha_angle, self.Alpha_long]

    def Beta(self):
        self.Alpha_l = OEM.Alpha(self)[1]
        self.Beta_radians = math.atan(abs(self.Z) / abs(self.Alpha_long))  # 弧度制
        self.Beta_angle = math.degrees(self.Beta_radians)  # 角度制

        if self.Z < 0:
            self.Beta_angle = -1 * self.Beta_radians

        self.Beta_long = math.sqrt(self.Alpha_l ** 2 + self.Z ** 2)

        return [self.Beta_angle, self.Beta_long]

    def GetEarthRadius(self, theta):
        # print("θ:", theta)
        x = self.a * math.cos(theta * (math.pi / 180))
        y = self.b * math.sin(theta * (math.pi / 180))
        # print("x、y: ", x, y)
        self.earth_r = math.sqrt((x ** 2) + (y ** 2))
        # 受地球椭圆的影响,距地心不同维度的点，半径不同

    def GetRotationAngle(self, UTC):
        self.UTC_time = str(datetime.fromtimestamp(UTC)).split(' ')[1].split(':')
        self.UTC_time = [float(x) for x in self.UTC_time]
        second = float(self.UTC_time[0] * 3600 + self.UTC_time[1] * 60 + self.UTC_time[2])
        self.earth_angle = math.pi * 2 * (second / self.rotation_time)
        # 将UTC时间转化为地球自转角度(rad)

    def RotationMatrix(self, x, y, UTC):
        OEM.GetRotationAngle(self, UTC)
        self.X = x * math.cos(self.earth_angle) - y * math.sin(self.earth_angle)
        self.Y = x * math.sin(self.earth_angle) + y * math.cos(self.earth_angle)
        # 旋转矩阵

    def Solve(self, O_XYZ):
        self.UTC_time = O_XYZ[0]
        self.X = O_XYZ[1][0]
        self.Y = O_XYZ[1][1]
        self.Z = O_XYZ[1][2]
        self.X_DOT = O_XYZ[2][0]
        self.Y_DOT = O_XYZ[2][1]
        self.Z_DOT = O_XYZ[2][2]

        # OEM.RotationMatrix(self, self.X, self.Y, self.UTC_time)
        #  将EME2000坐标系旋转至地球经纬度坐标系(直接注释此行表示不进行变换)

        print("三轴数据: ", self.X, self.Y, self.Z)

        alpha_data = OEM.Alpha(self)
        beta_data = OEM.Beta(self)
        OEM.GetEarthRadius(self, beta_data[0])
        # print("此处地球半径:", self.earth_r)

        # α角角度、β角角度、目标距O点长度(km)
        return [alpha_data[0], beta_data[0], beta_data[1], beta_data[1] - self.earth_r]
