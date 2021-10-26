from project import app
from flask import render_template, request, Markup, url_for, redirect , session
from datetime import datetime
from project.app_thong_tin_nv import thong_tin
from project.models.XuLy.XuLy_Date import Cong_thang, Tru_thang
from project.models.nhanvien import NhanVien
from datetime import datetime
from project.models.sanpham import KT_GH, SanPham
from project.models.taikhoan import Bam_mk, TaiKhoan, random_id
from project.models.hoadon import HoaDon
from project.models.CTHD import CTHD

@app.route('/quan-ly-ban-hang-<string:id>',methods=['GET','POST'])
def quan_ly_ban_hang(id):
    if session.get('quan_ly_ban_hang')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap')
    session['Home']="/quan-ly-ban-hang-"+id
    if KT_GH(session,'Thang'):
        pass
    else:
        now = datetime.now()
        Nam = int(now.strftime("%Y"))
        Thang =int(now.strftime("%m"))
        session['Nam_max']=Nam
        session['Thang_max']=Thang
        session['Thang']=Thang
        session['Nam']=Nam
    DS = NhanVien().Xuat_THD_TSP(session['Thang'],session['Nam'])
    TongHD=HoaDon().TongHD_Thang(session['Thang'],session['Nam'])
    TongSP=SanPham().Tong_SP_Ban_Thang(session['Thang'],session['Nam'])
    if request.method == 'POST':
        a = request.form
        if request.form.get('Logout')=='out':
            session['quan_ly_ban_hang']= None
            return redirect('/dangnhap')
        if a.get('Block'):
            TaiKhoan().Block_id(a.get('Block'))
            return redirect(session['Home'])
        if a.get('UnBlock'):
            TaiKhoan().UnBlock_id(a.get('UnBlock'))
            return redirect(session['Home'])
        if request.form.get('Trang')=='Truoc':
            session['Thang'], session['Nam'] = Tru_thang(session['Thang'],session['Nam'])
            DS = NhanVien().Xuat_THD_TSP(session['Thang'],session['Nam'])
            TongHD=HoaDon().TongHD_Thang(session['Thang'],session['Nam'])
            TongSP=SanPham().Tong_SP_Ban_Thang(session['Thang'],session['Nam'])
            return render_template('quan_ly_ban_hang/index.html',DS=DS,Thang=session['Thang'],Nam=session['Nam'],Home=session['Home']
                            ,id=id,TongHD=TongHD,TongSP=TongSP,Thang_max=session['Thang_max'],Nam_max=session['Nam_max'])
        if request.form.get('Trang')=='Sau':
            session['Thang'], session['Nam'] = Cong_thang(session['Thang'],session['Nam'])
            DS = NhanVien().Xuat_THD_TSP(session['Thang'],session['Nam'])
            TongHD=HoaDon().TongHD_Thang(session['Thang'],session['Nam'])
            TongSP=SanPham().Tong_SP_Ban_Thang(session['Thang'],session['Nam'])
            return render_template('quan_ly_ban_hang/index.html',DS=DS,Thang=session['Thang'],Nam=session['Nam'],Home=session['Home']
                            ,id=id,TongHD=TongHD,TongSP=TongSP,Thang_max=session['Thang_max'],Nam_max=session['Nam_max'])
    return render_template('quan_ly_ban_hang/index.html',DS=DS,Thang=session['Thang'],Nam=session['Nam'],Home=session['Home']
                            ,id=id,TongHD=TongHD,TongSP=TongSP,Thang_max=session['Thang_max'],Nam_max=session['Nam_max'])

@app.route('/them-nhan-vien-ban-hang',methods=['GET','POST'])
def add_nv_bh():
    if session.get('quan_ly_ban_hang')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap')
    thong_bao=""
    if KT_GH(session,'Thang'):
        session.pop('Thang')
    if request.method == 'POST':
        a = request.form
        if request.form.get('Logout')=='out':
            session['quan_ly_ban_hang']= None
            return redirect('/dangnhap') 
        if KT_GH(a,'NameNV'):
            NameNV = a.get('NameNV')
            GT =  a.get('GT')
            Date = a.get('Date')
            SDT = a.get('SDT')
            DiaChi = a.get('DiaChi')
            NameTK=a.get('NameTK')
            id= random_id(10)
            if NameNV.replace(" ", "")=="" or GT.replace(" ", "")=="" or Date.replace(" ", "")=="" or SDT.replace(" ", "")=="" or DiaChi.replace(" ", "")=="" or NameTK.replace(" ", "")=="":
                thong_bao = Markup('<div class="alert alert-danger text-center" role="alert">Không được để trống thông tin</div>')
            elif a.get('new-Pwd-1') != a.get('new-Pwd-2') :
                thong_bao = Markup('<div class="alert alert-danger text-center" role="alert">Mật khẩu không giống nhau</div>')
            else:
                TaiKhoan().add_TaiKhoan((id,NameTK,4,Bam_mk(a.get('new-Pwd-1')),1))
                NhanVien().add_NhanVien((id,NameNV,GT,Date,SDT,DiaChi))
                thong_bao = Markup('<div class="alert alert-success text-center" role="alert">Đã thêm nhân viên thành công </div>')
    return render_template('quan_ly_ban_hang/themNV.html',Home=session['Home'],thong_bao=thong_bao)


@app.route('/chi-tiet-nhan-vien-ban-hang/<string:id>',methods=['GET','POST'])
def cttt_nv_bh(id):
    if session.get('quan_ly_ban_hang')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap')
    session['Back']="/chi-tiet-nhan-vien-ban-hang/"+id
    TT_NV = NhanVien().Lay_NV_id(id)
    DS = HoaDon().Lay_HD_NV_theoThang(id,session['Thang'],session['Nam'])
    if request.method == 'POST':
        a = request.form
        if request.form.get('Logout')=='out':
            session['quan_ly_ban_hang']= None
            return redirect('/dangnhap') 
        if a.get('Back')=='out':
            return redirect(session['Home'])
    return render_template('quan_ly_ban_hang/new.html',DS=DS,Home=session['Home'],TT_NV= TT_NV)


@app.route('/hoa-don-thanh-toan-<string:MaHD>',methods=['GET','POST'])
def cthd_nv_bh(MaHD):
    if session.get('quan_ly_ban_hang')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap')
    DS = CTHD().Lay_CTHD_idHD(MaHD)
    if request.method == 'POST':
        a = request.form
        if request.form.get('Logout')=='out':
            session['quan_ly_ban_hang']= None
            return redirect('/dangnhap')
        if a.get('Back')=='out':
            return redirect(session['Back'])
    return render_template('quan_ly_ban_hang/chitietHD.html',Home=session['Home'],DS=DS,MaHD=MaHD)