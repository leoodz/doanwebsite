from pyodbc import connect
import json
import random
import hashlib

class TaiKhoan:
    def __init__(self):
        file = open('project/models/Data/NameServer.json',encoding='utf-8')
        NameSerrver_1 = json.load(file)
        file.close()
        self.db = connect('Driver={SQL Server};Server='+NameSerrver_1["NameServer"]+';Database='+NameSerrver_1["NameDatabase"]+';Uid='+NameSerrver_1["Account_SQL"]+';Pwd='+NameSerrver_1["Pass_SQL"]+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
	
    
    def add_TaiKhoan(self, arr):
        sql ='''INSERT INTO TaiKhoan (id,TenTK, IDCV, pws,TT)
            VALUES(?,?,?,?,?)'''
        cur = self.db.cursor()
        cur.execute(sql,arr)
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    def Lay_TaiKhoan(self):
        sql = 'SELECT * FROM TaiKhoan'
        cur = self.db.cursor()
        cur.execute(sql)
        a = cur.fetchall()
        cur.close()
        return a
    
    def DangNhap(self, Ten_TK, pws):
        sql = 'SELECT * FROM dbo.TaiKhoan WHERE TenTK=? and pws=?'
        cur = self.db.cursor()
        cur.execute(sql,(Ten_TK,Bam_mk(pws), ))
        v = cur.fetchone()
        cur.close()
        return v

    def Lay_TaiKhoan_id(self, id):
        sql = 'SELECT * FROM dbo.TaiKhoan WHERE id=?'
        cur = self.db.cursor()
        cur.execute(sql,(id, ))
        v = cur.fetchone()
        cur.close()
        return v

    
    def doi_MK (self,arr):
        cur = self.db.cursor()
        cur.execute('UPDATE  dbo.TaiKhoan SET pws =? WHERE id =?',arr)
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    def Block_id(self,id):
        cur = self.db.cursor()
        cur.execute('UPDATE  dbo.TaiKhoan SET TT =0 WHERE id =?',(id,))
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    def Block_IDCV(self,idCV):
        cur = self.db.cursor()
        cur.execute('UPDATE  dbo.TaiKhoan SET TT =0 WHERE IDCV =?',(idCV,))
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    def UnBlock_id(self,id):
        cur = self.db.cursor()
        cur.execute('UPDATE  dbo.TaiKhoan SET TT =1 WHERE id =?',(id,))
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    def UnBlock_IDCV(self,idCV):
        cur = self.db.cursor()
        cur.execute('UPDATE  dbo.TaiKhoan SET TT =1 WHERE IDCV =?',(idCV,))
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    def Lay_TrangThai_id(self, id):
        sql = 'SELECT TT FROM dbo.TaiKhoan WHERE id=?'
        cur = self.db.cursor()
        cur.execute(sql,(id, ))
        v = cur.fetchone()
        cur.close()
        return v[0]

    def __def__(self):
        self.db.close()

def xu_ly_sang_json(thong_tin):
    fake_TK= {'id':thong_tin[0],'TenTK':thong_tin[1], 'IDCV':thong_tin[2], 'pws':thong_tin[3]}
    return fake_TK
    


def random_id(length):
    number = '0123456789'
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    id = ''
    for i in range(0,length,2):
        id += random.choice(number)
        id += random.choice(alpha)
    return id

def Bam_mk(mystring): #chuyển thành md5
    pws_md5 = hashlib.md5(mystring.encode())
    return pws_md5.hexdigest()


