from pyodbc import connect
import json

class Loai:
    def __init__(self):
        file = open('project/models/Data/NameServer.json',encoding='utf-8')
        NameSerrver_1 = json.load(file)
        file.close()
        self.db = connect('Driver={SQL Server};Server='+NameSerrver_1["NameServer"]+';Database='+NameSerrver_1["NameDatabase"]+';Uid='+NameSerrver_1["Account_SQL"]+';Pwd='+NameSerrver_1["Pass_SQL"]+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
	

    def add_Loai(self, NameLoai):
        sql ='''INSERT INTO dbo.Loai(NameLoai)
        VALUES( ?)'''
        cur = self.db.cursor()
        cur.execute(sql,(NameLoai,))
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    def Check_Loai(self, NameLoai):
        sql ='''SELECT * FROM dbo.Loai WHERE NameLoai=? '''
        cur = self.db.cursor()
        cur.execute(sql,(NameLoai,))
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret

    def Lis_Loai(self):                                  
        sql = 'SELECT * FROM dbo.Loai ORDER BY MaLoai DESC'
        cur = self.db.cursor()
        cur.execute(sql)
        v = cur.fetchall()
        cur.close()
        return v

    def Loai_SLmua(self,thang,nam):                                  
        sql = ''' SELECT NameLoai, (SELECT ISNULL(SUM(a.SlMua),0) 
					FROM dbo.CTHD a, dbo.HoaDon b,dbo.SanPham d 
					WHERE a.MaHD=b.MaHD AND a.IdSP=d.IdSP AND dbo.Loai.MaLoai=d.MaLoai AND MONTH(b.DateTT)=? AND YEAR(b.DateTT)=?)
					AS 'TongSP' FROM dbo.Loai 
					ORDER BY MaLoai DESC '''
        cur = self.db.cursor()
        cur.execute(sql,thang,nam)
        v = cur.fetchall()
        cur.close()
        return v
    

    def __def__(self):
        self.db.close()

