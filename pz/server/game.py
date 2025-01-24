import json
import sys, os
import platform
import pymysql

get_os = platform.system()
split_symbol = "\\" if get_os == "Windows" else '/'
current_path = os.path.abspath(__file__)
top_path = split_symbol.join(current_path.split(split_symbol)[:-2])
sys.path.append(top_path)
from src.const import *
from share.const import *
from const import *


class Game(object):
    def __init__(self):
        self.plantInfo = [[0] * GRID_COUNT[1] for _ in range(GRID_COUNT[0])]
        self.connectMysql()
        # self.loadPlantInfo()

    def connectMysql(self):
        config = {
            'host': DB_HOST,
            'port': DB_PORT,
            'user': DB_USER,
            'password': DB_PASS,
            'db': 'pvz',
            'charset': 'utf8mb4'  # 防止中文乱码
        }
        self.connection = pymysql.connect(**config)

    # def executeSql(self, sqlcmd):
    #     try:
    #         cursor = self.connection.cursor()
    #         cursor.execute(sqlcmd)
    #         self.connection.commit()
    #         results = cursor.fetchall()
    #         return results
    #     except Exception as e:
    #         print("execute failed!", sqlcmd, e)
    #         return []
    #
    # def loadPlantInfo(self):
    #     results = self.executeSql("select * from game;")
    #     if len(results) == 0:
    #         self.savePlantInfo()
    #     else:
    #         self.plantInfo = json.loads(results[0])
    #
    # def savePlantInfo(self):
    #     plantInfo = json.dumps(self.plantInfo)
    #     self.executeSql("insert into game (id,plantInfo) values (0,'%s') on duplicate key update plantInfo = '%s';" % (
    #         plantInfo, plantInfo))

    def checkAddPlant(self, pos, idx):
        msg = {
            'type': S2C_ADD_PLANT,
            'code': S2C_CODE_FAILED,
            'pos': pos,
            'plant_idx': idx
        }
        x, y = pos
        if x < 0 or x >= GRID_COUNT[0]:
            return msg
        if y < 0 or y >= GRID_COUNT[1]:
            return msg
        if self.plantInfo[x][y] == 1:
            return msg
        # 金钱判定
        self.plantInfo[x][y] = idx
        # self.savePlantInfo()
        msg['code'] = S2C_CODE_SUCCEED
        return msg
