from project import app
from flask import render_template, request, Markup, redirect , session
from datetime import datetime
from project.models.XuLy.XuLy_Date import Cong_thang, Tru_thang
from project.models.nhanvien import NhanVien
from project.models.phieunhap import PhieuNhap
from project.models.sanpham import KT_GH, SanPham
from project.models.taikhoan import Bam_mk, TaiKhoan, random_id

@app.route('/quan-ly-nhap-hang-<string:id>',methods=['GET','POST'])
def quan_ly_nhap_hang(id):
    if session.get('quan_ly_nhap_hang')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap')
    session['Home']='/quan-ly-nhap-hang-'+id
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
    DS = NhanVien().Xuat_TPN_TSP(session['Thang'],session['Nam'])
    TongPN=PhieuNhap().TongPN_Thang(session['Thang'],session['Nam'])
    TongSP=SanPham().Tong_SP_Nhap_Thang(session['Thang'],session['Nam'])
    if request.method == 'POST':
        a= request.form
        if request.form.get('Logout')=='out':
            session['quan_ly_nhap_hang']= None
            return redirect('/dangnhap')
        if a.get('Block'):
            TaiKhoan().Block_id(a.get('Block'))
            return redirect(session['Home'])
        if a.get('UnBlock'):
            TaiKhoan().UnBlock_id(a.get('UnBlock'))
            return redirect(session['Home'])
        if request.form.get('Trang')=='Truoc':
            session['Thang'], session['Nam'] = Tru_thang(session['Thang'],session['Nam'])
            DS = NhanVien().Xuat_TPN_TSP(session['Thang'],session['Nam'])
            TongPN=PhieuNhap().TongPN_Thang(session['Thang'],session['Nam'])
            TongSP=SanPham().Tong_SP_Nhap_Thang(session['Thang'],session['Nam'])
            return render_template('quan_ly_nhap_hang/index.html',DS=DS,Home=session['Home'],Thang=session['Thang'],Nam=session['Nam'],Thang_max=session['Thang_max']
                            ,Nam_max=session['Nam_max'],id=id,TongPN=TongPN,TongSP=TongSP)
        if request.form.get('Trang')=='Sau':
            session['Thang'], session['Nam'] = Cong_thang(session['Thang'],session['Nam'])
            DS = NhanVien().Xuat_TPN_TSP(session['Thang'],session['Nam'])
            TongPN=PhieuNhap().TongPN_Thang(session['Thang'],session['Nam'])
            TongSP=SanPham().Tong_SP_Nhap_Thang(session['Thang'],session['Nam'])
            return render_template('quan_ly_nhap_hang/index.html',DS=DS,Home=session['Home'],Thang=session['Thang'],Nam=session['Nam'],Thang_max=session['Thang_max']
                            ,Nam_max=session['Nam_max'],id=id,TongPN=TongPN,TongSP=TongSP)
    return render_template('quan_ly_nhap_hang/index.html',DS=DS,Home=session['Home'],Thang=session['Thang'],Nam=session['Nam'],Thang_max=session['Thang_max']
                            ,Nam_max=session['Nam_max'],id=id,TongPN=TongPN,TongSP=TongSP)

@app.route('/them-nhan-vien-nhap-hang',methods=['GET','POST'])
def add_nv_nh():
    if session.get('quan_ly_nhap_hang')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap')
    thong_bao=""
    if KT_GH(session,'Thang'):
        session.pop('Thang')
    if request.method == 'POST':
        a = request.form
        if request.form.get('Logout')=='out':
            session['quan_ly_nhap_hang']= None
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
                TaiKhoan().add_TaiKhoan((id,NameTK,5,Bam_mk(a.get('new-Pwd-1')),1))
                NhanVien().add_NhanVien((id,NameNV,GT,Date,SDT,DiaChi))
                thong_bao = Markup('<div class="alert alert-success text-center" role="alert">Đã thêm nhân viên thành công </div>')
    return render_template('quan_ly_nhap_hang/themNV.html',Home=session['Home'],thong_bao=thong_bao)

@app.route('/chi-tiet-nhan-vien-nhap-hang/<string:id>',methods=['GET','POST'])
def cttt_nv_nh(id):
    if session.get('quan_ly_nhap_hang')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap')
    TT_NV = NhanVien().Lay_NV_id(id)
    DS = PhieuNhap().Lay_PN_NV_theoThang(id,session['Thang'],session['Nam'])
    if request.method == 'POST':
        a = request.form
        if request.form.get('Logout')=='out':
            session['quan_ly_ban_hang']= None
            return redirect('/dangnhap') 
        if a.get('Back')=='out':
            return redirect(session['Home'])
    return render_template('quan_ly_nhap_hang/chitietPN.html',DS=DS,Home=session['Home'],TT_NV= TT_NV)