from pyodbc import connect
import json

class TrangThai:
    def __init__(self):
        file = open('project/models/Data/NameServer.json',encoding='utf-8')
        NameSerrver_1 = json.load(file)
        file.close()
        self.db = connect('Driver={SQL Server};Server='+NameSerrver_1["NameServer"]+';Database='+NameSerrver_1["NameDatabase"]+';Uid='+NameSerrver_1["Account_SQL"]+';Pwd='+NameSerrver_1["Pass_SQL"]+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
	
    def Lis_TT(self):                                  
        sql = 'SELECT * FROM dbo.TrangThai '
        cur = self.db.cursor()
        cur.execute(sql)
        v = cur.fetchall()
        cur.close()
        return v

    def Update_TT(self,TenTT,TT):                                  
        sql = ''' Update dbo.TrangThai Set TrangThai=? where NameTT=? '''
        cur = self.db.cursor()
        cur.execute(sql,TT,TenTT)
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    def Update_All(self,TT):                                  
        sql = ''' Update dbo.TrangThai Set TrangThai=?  '''
        cur = self.db.cursor()
        cur.execute(sql,TT)
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret


    def __def__(self):
        self.db.close()

def Xuat_Dis():
    a = TrangThai().Lis_TT()
    lis = {}
    for i in a:
        lis[i[0].replace(" ", "")] =  i[1]
    return lis


