from pyodbc import connect
import json


class NhanHang:
    def __init__(self):
        file = open('project/models/Data/NameServer.json',encoding='utf-8')
        NameSerrver_1 = json.load(file)
        file.close()
        self.db = connect('Driver={SQL Server};Server='+NameSerrver_1["NameServer"]+';Database='+NameSerrver_1["NameDatabase"]+';Uid='+NameSerrver_1["Account_SQL"]+';Pwd='+NameSerrver_1["Pass_SQL"]+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
	
    def add_NH(self,NameNH):
        sql ='''INSERT INTO dbo.NhanHang(NameNH)
        VALUES( ?)'''
        cur = self.db.cursor()
        cur.execute(sql,(NameNH,))
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret

    def Check_NH(self, NameNH):
        sql ='''SELECT * FROM dbo.NhanHang WHERE NameNH=? '''
        cur = self.db.cursor()
        cur.execute(sql,(NameNH,))
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret

    def Lis_NH(self):                                  
        sql = 'SELECT * FROM dbo.NhanHang ORDER BY MaNH DESC'
        cur = self.db.cursor()
        cur.execute(sql)
        v = cur.fetchall()
        cur.close()
        return v
    
    def NH_SLmua(self,thang,nam):                                  
        sql = '''SELECT dbo.NhanHang.NameNH, (SELECT ISNULL(SUM(a.SlMua),0)
				FROM dbo.CTHD a, dbo.HoaDon b,dbo.SanPham d 
				WHERE a.MaHD=b.MaHD AND a.IdSP=d.IdSP AND d.MaNH=dbo.NhanHang.MaNH AND MONTH(b.DateTT)=? AND YEAR(b.DateTT)=?)
				AS 'TongSP' FROM dbo.NhanHang
				ORDER BY MaNH DESC '''
        cur = self.db.cursor()
        cur.execute(sql,thang,nam)
        v = cur.fetchall()
        cur.close()
        return v

    def __def__(self):
        self.db.close()

