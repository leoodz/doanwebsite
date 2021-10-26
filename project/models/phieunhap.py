from pyodbc import connect
import json

class PhieuNhap:
    def __init__(self):
        file = open('project/models/Data/NameServer.json',encoding='utf-8')
        NameSerrver_1 = json.load(file)
        file.close()
        self.db = connect('Driver={SQL Server};Server='+NameSerrver_1["NameServer"]+';Database='+NameSerrver_1["NameDatabase"]+';Uid='+NameSerrver_1["Account_SQL"]+';Pwd='+NameSerrver_1["Pass_SQL"]+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
	

    def Them_PN(self, arr):
        sql ='''INSERT INTO dbo.PhieuNhap(id,IdSP,SLThem,NgayNhap)
        VALUES( ?, ? , ?, ? )'''
        cur = self.db.cursor()
        cur.execute(sql,arr)
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    
    def TongPN_Thang(self, Thang,Nam):
        sql = ''' SELECT COUNT(NgayNhap) AS 'TongPN' FROM dbo.PhieuNhap WHERE MONTH(NgayNhap)=? AND YEAR(NgayNhap)=? '''
        cur = self.db.cursor()
        cur.execute(sql,(Thang,Nam, ))
        v = cur.fetchone()
        cur.close()
        return v[0]
    
    def Lay_PN_NV_theoThang(self,idNV,thang,Nam):
        sql = ''' SELECT a.IdSP,c.NameSP,CONVERT(VARCHAR,a.NgayNhap,103) AS 'NgayNhap',a.SLThem,c.Buy,c.ImageUrl 
                FROM dbo.PhieuNhap a,dbo.ThongTinNV b, dbo.SanPham c 
                WHERE a.IdSP=c.IdSP AND b.id=a.id AND MONTH(a.NgayNhap)=? AND YEAR(a.NgayNhap)=? AND a.id=? '''
        cur = self.db.cursor()
        cur.execute(sql,(thang,Nam,idNV, ))
        v = cur.fetchall()
        cur.close()
        return v

    def Tong_Chi(self, Thang,Nam):
        sql = ''' SELECT  ISNULL(SUM(a.SLThem * b.Buy),0) AS 'TongChi' FROM PhieuNhap a, SanPham b
                WHERE a.IdSP=b.IdSP AND MONTH(a.NgayNhap)=? AND YEAR(a.NgayNhap)=? '''
        cur = self.db.cursor()
        cur.execute(sql,(Thang,Nam, ))
        v = cur.fetchone()
        cur.close()
        return v[0]

    def __def__(self):
        self.db.close()


