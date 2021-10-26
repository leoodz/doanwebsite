from pyodbc import connect
import json

class Chucvu:
    def __init__(self):
        file = open('project/models/Data/NameServer.json',encoding='utf-8')
        NameSerrver_1 = json.load(file)
        file.close()
        self.db = connect('Driver={SQL Server};Server='+NameSerrver_1["NameServer"]+';Database='+NameSerrver_1["NameDatabase"]+';Uid='+NameSerrver_1["Account_SQL"]+';Pwd='+NameSerrver_1["Pass_SQL"]+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
	

    def Lay_CV(self):
        sql = 'SELECT * FROM dbo.ChucVu'
        cur = self.db.cursor()
        cur.execute(sql)
        a = cur.fetchall()
        cur.close()
        return a
    
    def Lay_CV_id(self, idcv):
        sql = 'SELECT * FROM dbo.ChucVu WHERE IDCV = ?'
        cur = self.db.cursor()
        cur.execute(sql,(idcv, ))
        v = cur.fetchone()
        cur.close()
        return v


    def __def__(self):
        self.db.close()

