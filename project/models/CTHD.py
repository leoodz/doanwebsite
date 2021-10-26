from pyodbc import connect
import json

class CTHD:
    def __init__(self):
        file = open('project/models/Data/NameServer.json',encoding='utf-8')
        NameSerrver_1 = json.load(file)
        file.close()
        self.db = connect('Driver={SQL Server};Server='+NameSerrver_1["NameServer"]+';Database='+NameSerrver_1["NameDatabase"]+';Uid='+NameSerrver_1["Account_SQL"]+';Pwd='+NameSerrver_1["Pass_SQL"]+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
	

    def Tao_CTHD(self, arr):
        sql ='''INSERT INTO dbo.CTHD(MaHD,IdSP,SlMua)
        VALUES( ?, ? ,? )'''
        cur = self.db.cursor()
        cur.execute(sql,arr)
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    
    def Lay_CTHD_idHD(self, MaHD):
        sql = ''' SELECT b.NameSP,b.ImageUrl , b.Sell,a.SlMua ,b.Sell*a.SlMua AS 'ThanhTien' FROM dbo.CTHD a, dbo.SanPham b WHERE MaHD=? AND a.IdSP=b.IdSP '''
        cur = self.db.cursor()
        cur.execute(sql,(MaHD, ))
        v = cur.fetchall()
        cur.close()
        return v

    def del_CTHD(self,MaHD):
        cur = self.db.cursor()
        cur.execute('DELETE dbo.CTHD WHERE MaHD =?',(MaHD,))
        ret =cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    def __def__(self):
        self.db.close()
