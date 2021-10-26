from pyodbc import connect
import json




class NhanVien:
    def __init__(self):
        file = open('project/models/Data/NameServer.json',encoding='utf-8')
        NameSerrver_1 = json.load(file)
        file.close()
        self.db = connect('Driver={SQL Server};Server='+NameSerrver_1["NameServer"]+';Database='+NameSerrver_1["NameDatabase"]+';Uid='+NameSerrver_1["Account_SQL"]+';Pwd='+NameSerrver_1["Pass_SQL"]+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
	
    
    def add_NhanVien(self, arr):
        sql ='''INSERT INTO dbo.ThongTinNV(id,NameNV,GT,NS,SDT,DiaChi)
        VALUES( ?, ? ,? , ?, ?, ?)'''
        cur = self.db.cursor()
        cur.execute(sql,arr)
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    def Lay_NV_id(self, id):
        sql = ''' SELECT id,NameNV,GT,CONVERT(VARCHAR,ThongTinNV.NS,103) AS 'NS',SDT,DiaChi FROM dbo.ThongTinNV WHERE id = ? '''
        cur = self.db.cursor()
        cur.execute(sql,(id, ))
        v = cur.fetchone()
        cur.close()
        return v
  

    def deletes(self,id):
        cur = self.db.cursor()
        cur.execute('DELETE dbo.ThongTinNV WHERE id =?',(id,))
        ret =cur.rowcount
        self.db.commit()
        cur.close()
        return ret

    def Tim_kiem_ten(self,nameNV):
        sql = '''SELECT id,NameNV,GT,CONVERT(VARCHAR,ThongTinNV.NS,103) AS 'NS',SDT,DiaChi FROM dbo.ThongTinNV WHERE NameNV LIKE ?'''
        cur = self.db.cursor()
        cur.execute(sql,(nameNV,))
        a = cur.fetchall()
        cur.close()
        return a
    
    def Xuat_THD_TSP(self,thang,nam):
        sql = ''' SELECT TaiKhoan.id, NameNV,CONVERT(VARCHAR,ThongTinNV.NS,103) AS 'NS',SDT,TT , ( SELECT COUNT(DISTINCT a.MaHD) FROM dbo.CTHD a, dbo.HoaDon b 
            WHERE a.MaHD=b.MaHD AND b.id=dbo.TaiKhoan.id AND 
			MONTH(b.DateTT)=? AND YEAR(b.DateTT)=?) as 'TongHD',( SELECT SUM(a.SlMua) FROM dbo.CTHD a, dbo.HoaDon b WHERE a.MaHD=b.MaHD AND 
			b.id=dbo.TaiKhoan.id AND MONTH(b.DateTT)=? AND YEAR(b.DateTT)=?) as'TongSP' FROM dbo.ThongTinNV ,dbo.TaiKhoan  WHERE dbo.TaiKhoan.IDCV=4 AND
			dbo.ThongTinNV.id=dbo.TaiKhoan.id '''
        cur = self.db.cursor()
        cur.execute(sql,(thang,nam,thang,nam,))
        a = cur.fetchall()
        cur.close()
        return a
    
    def Xuat_TPN_TSP(self,thang,nam):
        sql = ''' SELECT DISTINCT TaiKhoan.id, NameNV,CONVERT(VARCHAR,ThongTinNV.NS,103) AS 'NS',SDT,TT ,(SELECT COUNT(id) FROM dbo.PhieuNhap WHERE id=dbo.ThongTinNV.id AND MONTH(NgayNhap)=?
                AND YEAR(NgayNhap)=?)
				AS 'SoPN', (SELECT SUM(SlThem) FROM dbo.PhieuNhap WHERE id=dbo.ThongTinNV.id  AND MONTH(NgayNhap)=? AND YEAR(NgayNhap)=?)
				AS 'TongHN' FROM dbo.PhieuNhap,dbo.ThongTinNV,dbo.TaiKhoan WHERE dbo.TaiKhoan.IDCV='5' AND dbo.TaiKhoan.id=dbo.ThongTinNV.id '''
        cur = self.db.cursor()
        cur.execute(sql,(thang,nam,thang,nam,))
        a = cur.fetchall()
        cur.close()
        return a
    
    
    def update_NV(self,id,NameNV,GT,NS,SDT,DiaChi):
        sql = 'UPDATE dbo.ThongTinNV SET NameNV =?,GT=?,NS=?,SDT=?,DiaChi=? WHERE id =?'
        cur = self.db.cursor()
        cur.execute(sql,(NameNV,GT,NS,SDT,DiaChi,id,))
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret

    def __def__(self):
        self.db.close()

