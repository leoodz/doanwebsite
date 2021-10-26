from flask.scaffold import F
from project.models.hoadon import HoaDon
from project.models.CTHD import CTHD
from project.models.taikhoan import random_id
from project.models.khachhang import KhachHang
from project.models.sanpham import TongTien,SanPham
from datetime import datetime

def tach_id(thaotac):
    i = thaotac.split("-")
    ThaoTac =i[0]
    id = i[1]
    return id, ThaoTac

def LapHD(id_KH,NVHB,data):
    now = datetime.now()
    s1 = now.strftime("%Y-%m-%d")

    id_HD = random_id(20)
    id_NV = NVHB['id']
    Tong_tien = TongTien(data['GioHang'])
    # Taọ khách hàng
    if KhachHang().Lay_KH_id(id_KH):
        pass
    else:
        a = KhachHang().add_KhachHang([id_KH,data['NameKH'],data['DCKH'],data['SDTKH']])
    # Tao hoa don
    lis = [id_HD,id_KH,id_NV,s1,Tong_tien]
    b = HoaDon().Tao_HD(lis)
    # tao chi tiet HD
    c = CTHD()
    GH = data['GioHang']
    for j in GH:
        SP =SanPham().Lay_SP_id(j['IdSP'])
        if SP[8] < j['SL_trong_gio']:
            return 0
    for i in GH:
        SP =SanPham().Lay_SP_id(j['IdSP'])
        c.Tao_CTHD([id_HD,i['IdSP'],i['SL_trong_gio']])
        SanPham().update_SL(i['IdSP'],(SP[8] - j['SL_trong_gio']))
    return 1
