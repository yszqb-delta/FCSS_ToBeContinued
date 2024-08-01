import GetOEM
import SolveOEM

# print(m.solve(["2024", "7", "", "", "", ""]))

CSS = SolveOEM.OEM()
m = GetOEM.GetOEM()
m.GetFile()

# ----------------------------------------------------------------------------------------------------
O_XYZ = m.Get(1720153200)  # UTC:2024,7,5 12:20:00   北京时间:2024,7,5 20:20:00
print(O_XYZ)
print("处理前: ", O_XYZ)
print("处理后: ", CSS.Solve(O_XYZ), '\n')
# 天文通数据: 经度-109.19 纬度23.1 高375.6
# 2024-07-05T12:20:00.00 6235.996563264 -93.558956408 2583.857468476

O_XYZ = m.Get(1720155360)  # UTC:2024,7,5 12:56:00   北京时间:2024,7,5 20:56:00
print("处理前: ", O_XYZ)
print("处理后: ", CSS.Solve(O_XYZ), '\n')
# 天文通数据: 经度30.52 纬度2.29 高380.0
# ----------------------------------------------------------------------------------------------------

# O_XYZ = m.Get(1720220400)  # UTC:2024,7,6 7:00：00    北京时间:2024,7,6 15:00:00
# print(O_XYZ)
# print(O_XYZ[0], CSS.Solve(O_XYZ), '\n')
# # 天文通数据: 经度43 纬度40 高381


# for i in range(m.START_TIME + 240 * 100, m.START_TIME + 240 * 110, 240):  # m.STOP_TIME + 240
#     O_XYZ = m.Get(i)
#     print(O_XYZ[0], CSS.Solve(O_XYZ), '\n')

# pip install --upgrade pip setuptools
