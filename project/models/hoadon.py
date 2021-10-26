from pyodbc import connect
import json

class HoaDon:
    def __init__(self):
        file = open('project/models/Data/NameServer.json',encoding='utf-8')
        NameSerrver_1 = json.load(file)
        file.close()
        self.db = connect('Driver={ODBC Driver 13 for SQL Server};Server='+NameSerrver_1["NameServer"]+';Database='+NameSerrver_1["NameDatabase"]+';Uid='+NameSerrver_1["Account_SQL"]+';Pwd='+NameSerrver_1["Pass_SQL"]+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
	

    def Tao_HD(self, arr):
        sql ='''INSERT INTO dbo.HoaDon(MaHD,idKH,id,DateTT,TongTien)
        VALUES( ?, ? ,? , ?, ?)'''
        cur = self.db.cursor()
        cur.execute(sql,arr)
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    
    def Lay_HD_idKH(self, idKH):
        sql = '''SELECT MaHD,idKH,id,CONVERT(varchar,DateTT,103) AS 'DateTT',TongTien FROM dbo.HoaDon WHERE idKH = ?'''
        cur = self.db.cursor()
        cur.execute(sql,(idKH, ))
        v = cur.fetchone()
        cur.close()
        return v
    
    def Lay_HD_MaHD(self, MaHD):
        sql = '''SELECT MaHD,idKH,id,CONVERT(varchar,DateTT,103) AS 'DateTT',TongTien FROM dbo.HoaDon WHERE MaHD = ?'''
        cur = self.db.cursor()
        cur.execute(sql,(MaHD, ))
        v = cur.fetchone()
        cur.close()
        return v
    
    def TongHD_Thang(self, Thang,Nam):
        sql = ''' SELECT COUNT(DISTINCT a.MaHD ) AS 'TongHDMonth' FROM dbo.CTHD a, dbo.HoaDon b WHERE a.MaHD=b.MaHD AND MONTH(b.DateTT)=? AND YEAR(b.DateTT)=? '''
        cur = self.db.cursor()
        cur.execute(sql,(Thang,Nam, ))
        v = cur.fetchone()
        cur.close()
        return v[0]
    
    def Lay_HD_NV_theoThang(self,idNV,thang,Nam):
        sql = ''' SELECT a.MaHD,CONVERT(VARCHAR,a.DateTT,103) AS 'DateTT',a.TongTien,b.NameKH FROM dbo.HoaDon a, dbo.ThongTinKH b
                WHERE a.idKH=b.idKH AND a.id=? AND MONTH(a.DateTT)=? AND YEAR(a.DateTT)=? '''
        cur = self.db.cursor()
        cur.execute(sql,(idNV,thang,Nam, ))
        v = cur.fetchall()
        cur.close()
        return v

    def del_HD(self,MaHD):
        cur = self.db.cursor()
        cur.execute('DELETE dbo.HoaDon WHERE MaHD =?',(MaHD,))
        ret =cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    def Tong_Thu(self, Thang,Nam):
        sql = ''' SELECT  ISNULL(SUM(TongTien),0) AS 'TongThu' FROM  HoaDon WHERE MONTH(DateTT)=? AND YEAR(DateTT)=? '''
        cur = self.db.cursor()
        cur.execute(sql,(Thang,Nam, ))
        v = cur.fetchone()
        cur.close()
        return v[0]

    def __def__(self):
        self.db.close()
