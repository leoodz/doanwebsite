from pyodbc import connect
import json
from project.models.taikhoan import random_id


class KhachHang:
    def __init__(self):
        file = open('project/models/Data/NameServer.json',encoding='utf-8')
        NameSerrver_1 = json.load(file)
        file.close()
        self.db = connect('Driver={SQL Server};Server='+NameSerrver_1["NameServer"]+';Database='+NameSerrver_1["NameDatabase"]+';Uid='+NameSerrver_1["Account_SQL"]+';Pwd='+NameSerrver_1["Pass_SQL"]+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
	
    def add_KhachHang(self, arr):
        sql ='''INSERT INTO dbo.ThongTinKH(idKH,NameKH,DCKH,SDTKH)
        VALUES( ?, ? ,? , ?)'''
        cur = self.db.cursor()
        cur.execute(sql,arr)
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    def Lay_KH(self):
        sql = 'SELECT * FROM dbo.ThongTinKH'
        cur = self.db.cursor()
        cur.execute(sql)
        a = cur.fetchall()
        cur.close()
        return a
    
    def Lay_KH_id(self, idKH):
        sql = 'SELECT * FROM dbo.ThongTinKH WHERE idKH = ?'
        cur = self.db.cursor()
        cur.execute(sql,(idKH, ))
        v = cur.fetchone()
        cur.close()
        return v
  
    
    def deletes(self,arr):
        cur = self.db.cursor()
        cur.execute('DELETE dbo.ThongTinKH WHERE idKH =?',arr)
        ret =cur.rowcount
        self.db.commit()
        cur.close()
        return ret

    def Tim_kiem_ten(self,nameKH):
        sql = 'SELECT * FROM dbo.ThongTinKH WHERE NameKH LIKE ?'
        cur = self.db.cursor()
        cur.execute(sql,(nameKH,))
        a = cur.fetchall()
        cur.close()
        return a
    
    def __def__(self):
        self.db.close()
 
def check_TTKH(ten,diachi,sdt): #check thong tin khac hang
    if ten == "" :               # trả về flase nếu khách hàng để trống
        return False
    if diachi == '' :
        return False
    if sdt == '':
        return False                # dể tránh KH đưa thông tin giả
    return True                    # ta trả dữ liệu về cho NV bán hàng 

def fake_TTGH(ten, diachi , sdt , giohang):  # tạo 1 biến ảo dạng JSON( disc của Python) lưu KH và giỏ hàng (Lưu ý: chỉ là biến ảo chưa đc NV xử lý )
    fake_json ={'NameKH':ten,'DCKH':diachi,'SDTKH':sdt,'GioHang':giohang,'TrangThai':'Chờ xử lý'}
    return fake_json

def Doc_DS_DH():                                                                        # Do list DS đặt hàng là biến ảo nên không   
    _f = open('project/models/Data/List_DatHang.json','r',encoding='utf-8')
    data = json.load(_f)
    _f.close()
    return data

def add_list_KH(fake_json):
    data = Doc_DS_DH()
    _f = open('project/models/Data/List_DatHang.json','w',encoding='utf-8')
    data[random_id(10)] = fake_json
    json.dump(data,_f,indent=4, ensure_ascii= False)
    _f.close()

def save_list_KH(list_ao):
    _f = open('project/models/Data/List_DatHang.json','w',encoding='utf-8')
    json.dump(list_ao,_f,indent=4, ensure_ascii= False)
    _f.close()
