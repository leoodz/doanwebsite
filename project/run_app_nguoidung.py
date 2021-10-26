from project import app
from flask import Flask, render_template, request, session, Markup
from project.models.sanpham import SanPham , XuLy_Ten ,add_gio_hang, Tinh_gio_hang,KT_GH,TongTien,check_lenh
from project.models.khachhang import check_TTKH, add_list_KH, fake_TTGH
from project.models.loai import Loai
from project.models.nhanhang import NhanHang

@app.route('/', methods=['GET','POST'])
def index():
    chuoi_tim = ''
    dsNH = NhanHang().Lis_NH()
    dsLoai = Loai().Lis_Loai()
    sanpham = SanPham().Lay_Sp()
    if KT_GH(session,'GioHang'):
        pass
    else:
        session['GioHang'] =[]
    if request.method == 'POST':
        if KT_GH(request.form,'TH_gt_tim'):
            chuoi_tim = request.form.get('TH_gt_tim')
            sanpham = SanPham().Tim_kiem_ten(XuLy_Ten(chuoi_tim))
        if KT_GH(request.form,'Loai'):
            sanpham = SanPham().Tim_TheoLoai(request.form.get('Loai'))
        if KT_GH(request.form,'NhanHang'):
            sanpham = SanPham().Tim_TheoNH(request.form.get('NhanHang'))
    return render_template('nguoidung/index.html',danh_sach_sanpham= sanpham,chuoi_tim=chuoi_tim,So_gioHang=Tinh_gio_hang(session['GioHang']),id =id,dsNH=dsNH,dsLoai=dsLoai) 

@app.route('/thong-tin-san-pham-<string:IdSP>', methods=['GET','POST'])
def nvnh_nh(IdSP):
    data = SanPham().Lay_SP_id(IdSP) 
    if request.method == 'POST':
        session['GioHang'] = add_gio_hang(session['GioHang'],IdSP)
    return render_template('nguoidung/new.html',data=data,So_gioHang=Tinh_gio_hang(session['GioHang']))

@app.route('/gio-hang', methods=['GET','POST'])
def gio_hang():
    thong_bao =''
    if request.method=='POST':
        lenh = request.form
        session['GioHang'] = check_lenh(session['GioHang'],lenh)
        if KT_GH(lenh,'NameKH'):
            if check_TTKH(lenh.get('NameKH'),lenh.get('DC_KH'),lenh.get('SDT_KH')):
                lis_fake = fake_TTGH(lenh.get('NameKH'),lenh.get('DC_KH'),lenh.get('SDT_KH'),session['GioHang'])
                add_list_KH(lis_fake)
                session['GioHang']=[]
                thong_bao = Markup('<div class="alert alert-success" role="alert">Đơn đang được nhận ( Vui lòng chờ nhân viên bán hàng xác nhận! )</div>')
            else:
                thong_bao = Markup('<div class="alert alert-danger" role="alert">Vui lòng điền đầy đủ thông tin</div>')
    return render_template('nguoidung/giohang.html',Gio_hang=session['GioHang'],Tongtien=TongTien(session['GioHang']),thong_bao=thong_bao)