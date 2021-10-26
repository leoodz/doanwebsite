from os import remove
from pyodbc import connect
import json


class SanPham:
    def __init__(self):
        file = open('project/models/Data/NameServer.json',encoding='utf-8')
        NameSerrver_1 = json.load(file)
        file.close()
        self.db = connect('Driver={SQL Server};Server='+NameSerrver_1["NameServer"]+';Database='+NameSerrver_1["NameDatabase"]+';Uid='+NameSerrver_1["Account_SQL"]+';Pwd='+NameSerrver_1["Pass_SQL"]+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
	
    
    def add_Sanpham(self, arr):
        sql ='''INSERT INTO dbo.SanPham(IdSP,NameSP,MaLoai,MaNH,Buy,Sell,ImageUrl,Description,SL)
        VALUES(?, ?, ? , ?, ?, ?, ? ,? , ?)'''
        cur = self.db.cursor()
        cur.execute(sql,arr)
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret
    
    def Lay_Sp(self):                                           # lấy toàn bộ sản phẩm để show cho người dùng
        sql = 'SELECT * FROM dbo.sanpham ORDER BY MaLoai DESC'  # có thể cái tiến khi quá nhiều dữ liệu
        cur = self.db.cursor()                                  # ý tưởng: có thể chia ra nhiều trang 
        cur.execute(sql)                                        # mỗi trang chỉ cần lấy ra 20 sp
        a = cur.fetchall()
        cur.close()
        return a
    
    def Lay_SP_id(self, idsp):                                  # dùng id để lấy thông tin sản phẩm
        sql = 'SELECT * FROM dbo.sanpham WHERE idsp = ?'
        cur = self.db.cursor()
        cur.execute(sql,(idsp, ))
        v = cur.fetchone()
        cur.close()
        return v
    
    def doi_thong_tin_sp(self,arr):
        cur = self.db.cursor()
        cur.execute('UPDATE  dbo.sanpham SET sl=? ,description= ? WHERE idsp =?',arr)
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret

    def update_SL(self,idsp,sl):
        sql = 'UPDATE dbo.sanpham SET sl =? WHERE idsp =?'
        cur = self.db.cursor()
        cur.execute(sql,(sl,idsp,))
        ret = cur.rowcount
        self.db.commit()
        cur.close()
        return ret

    def deletes(self,arr):
        cur = self.db.cursor()
        cur.execute('DELETE dbo.sanpham WHERE idsp =?',arr)
        ret =cur.rowcount
        self.db.commit()
        cur.close()
        return ret

    def Tim_TheoLoai(self,MaLoai):
        sql = 'SELECT * FROM dbo.SanPham WHERE MaLoai=?'
        cur = self.db.cursor()
        cur.execute(sql,(MaLoai,))
        a = cur.fetchall()
        cur.close()
        return a

    def Tim_TheoNH(self,MaNH):
        sql = 'SELECT * FROM dbo.SanPham WHERE MaNH=?'
        cur = self.db.cursor()
        cur.execute(sql,(MaNH,))
        a = cur.fetchall()
        cur.close()
        return a

    def Tong_SP_Ban_Thang(self,Thang,Nam):
        sql = ''' SELECT SUM(SlMua) AS 'TongSPMonth' FROM dbo.CTHD a,dbo.HoaDon b WHERE a.MaHD=b.MaHD AND MONTH(b.DateTT)=? AND YEAR(b.DateTT)=? '''
        cur = self.db.cursor()
        cur.execute(sql,(Thang,Nam,))
        a = cur.fetchone()
        cur.close()
        return a[0]
    
    def Tong_SP_Nhap_Thang(self,Thang,Nam):
        sql = ''' SELECT SUM(SLThem) AS 'TongSPThem' FROM dbo.PhieuNhap WHERE MONTH(NgayNhap)=? AND YEAR(NgayNhap)=? '''
        cur = self.db.cursor()
        cur.execute(sql,(Thang,Nam,))
        a = cur.fetchone()
        cur.close()
        return a[0]

    # SELECT * FROM dbo.SanPham WHERE NameSP LIKE N'%Chuột%'
    def Tim_kiem_ten(self,nameSP):
        sql = 'SELECT * FROM dbo.SanPham WHERE NameSP LIKE ?'
        cur = self.db.cursor()
        cur.execute(sql,(nameSP,))
        a = cur.fetchall()
        cur.close()
        return a
    
    def __def__(self):
        self.db.close()
 
# 1 số hàm bổ sung cho việc sử lý

def XuLy_Ten(chuoi):   # do chuổi tìm kiếm trong SQL cần thêm % trước sau chuỗi
    v ='%'+chuoi+'%'
    return v


def add_gio_hang(giohang,id):    # do giỏ hàng chỉ là biến ảo của người dùng nên không thể đưa vào database (chỉ khi xác nhận khách hang mua hàng mới đưa vào database)
    a = SanPham().Lay_SP_id(id)
    fake_gio_hang_new = {'IdSP':a[0],'NameSP':a[1],'Sell':a[5],'SL':a[8], 'ImageUrl':a[6],'SL_trong_gio':1} # chuyển thành dạng JSON (disc trong python)
    for i in giohang:
        if i['IdSP']==fake_gio_hang_new['IdSP']:
            i['SL_trong_gio']+=1
            return giohang
    giohang.append(fake_gio_hang_new)
    return giohang

def Tao_gio_hang(giohang,id,SL):   
    a = SanPham().Lay_SP_id(id)
    fake_gio_hang_new = {'IdSP':a[0],'NameSP':a[1],'Sell':a[5],'SL':a[8], 'ImageUrl':a[6],'SL_trong_gio':SL} 
    giohang.append(fake_gio_hang_new)
    return giohang

def KT_GH(sec,key):  #Kiểm tra sec[key] có tồn tại trong sec
    for i in sec:
        if i == key:
            return True
    return False

def Tinh_gio_hang(giohang):
    so_sp = 0
    if giohang == None:
        return so_sp
    for i in giohang:
        so_sp+=i['SL_trong_gio']
    return so_sp            # trả về số lượng sản phẩm trong giỏ

def xoa(giohang,id):  # dùng để bỏ món không muốn mua ra khỏi giỏ
    for i in giohang:
        if i['IdSP']== id:
            giohang.remove(i)
    return giohang

def doi_SL(giohang,id,SL):      # thay đổi số lượng trong giỏ
    for j in giohang:
        if j['IdSP'] == id:
            j['SL_trong_gio'] = int(SL)
    return giohang  

def check_lenh(giohang,lenh):  #kiểm tra lện để thực thi 1 trong 2 việc trên
    for i in lenh:
        id = i
        lenh_thuc_thi =lenh[i]
    if lenh_thuc_thi =='DELETE':
        return xoa(giohang,id)
    else:
        return doi_SL(giohang,id,lenh_thuc_thi)

def TongTien(giohang): #tính tiền trong giỏ
    Tong=0
    for i in giohang:
        Tong += (i['Sell']*i['SL_trong_gio'])
    return Tong

def check_TTSP(NameSP,MaLoai,MaNH,Buy,Sell,ImageUrl,Description,SL):
    if NameSP == "" :               
        return False
    if MaLoai == '' or MaLoai == 'Chọn loại hàng' :
        return False
    if MaNH == '' or MaNH == 'Chọn loại hàng':
        return False 
    if Buy == '':
        return False
    if Sell == '':
        return False
    if Description == '':
        return False
    if ImageUrl == '':
        return False 
    if SL == '':
        return False             
    return True 

