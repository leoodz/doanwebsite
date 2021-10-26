from datetime import datetime
from re import X
from flask.scaffold import F
from project import app
from flask import render_template, request, Markup, redirect , session
from project.models.nhanhang import NhanHang
from project.models.sanpham import KT_GH, SanPham, XuLy_Ten
from project.models.loai import Loai
from project.models.hoadon import HoaDon
from project.models.phieunhap import PhieuNhap
from project.models.XuLy.XuLy_Date import Tru_thang,Cong_thang
from project.models.trangthai import TrangThai,Xuat_Dis
from project.models.taikhoan import TaiKhoan

@app.route('/quan-ly-cong-ty-<string:id>',methods=['GET','POST'])
def quan_ly_cong_ty(id):
    if session.get('quan_ly_cong_ty')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap')
    if KT_GH(session,'Thang'):
        session.pop('Thang')
    DS = SanPham().Lay_Sp()
    dsNH = NhanHang().Lis_NH()
    dsLoai = Loai().Lis_Loai()
    chuoi_tim= ""
    session['Home'] = '/quan-ly-cong-ty-'+id
    if request.method == 'POST':
        if request.form.get('Logout')=='out':
            session['quan_ly_cong_ty']= None
            return redirect('/dangnhap')
        if KT_GH(request.form,'TH_gt_tim'):
            chuoi_tim = request.form.get('TH_gt_tim')
            DS = SanPham().Tim_kiem_ten(XuLy_Ten(chuoi_tim))
        if KT_GH(request.form,'Loai'):
            DS = SanPham().Tim_TheoLoai(request.form.get('Loai'))
        if KT_GH(request.form,'NhanHang'):
            DS = SanPham().Tim_TheoNH(request.form.get('NhanHang'))
    return render_template('quan_ly_cong_ty/index.html',DS=DS,id=id,Home=session['Home'],chuoi_tim=chuoi_tim,dsNH=dsNH,dsLoai=dsLoai)

@app.route('/quan-ly-cong-ty/doanh-thu',methods=['GET','POST'])
def quan_ly_cong_ty_doanh_thu():
    if session.get('quan_ly_cong_ty')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap')
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
    loai= Loai().Loai_SLmua(session['Thang'],session['Nam'])
    NH = NhanHang().NH_SLmua(session['Thang'],session['Nam'])
    Chi = PhieuNhap().Tong_Chi(session['Thang'],session['Nam'])
    Thu = HoaDon().Tong_Thu(session['Thang'],session['Nam'])
    if request.method == 'POST':
        if request.form.get('Logout')=='out':
            session['quan_ly_cong_ty']= None
            return redirect('/dangnhap')
        if request.form.get('Trang')=='Truoc':
            session['Thang'], session['Nam'] = Tru_thang(session['Thang'],session['Nam'])
            loai= Loai().Loai_SLmua(session['Thang'],session['Nam'])
            NH = NhanHang().NH_SLmua(session['Thang'],session['Nam'])
            Chi = PhieuNhap().Tong_Chi(session['Thang'],session['Nam'])
            Thu = HoaDon().Tong_Thu(session['Thang'],session['Nam'])
            return render_template('quan_ly_cong_ty/doanhthu.html',Thang=session['Thang'],Nam=session['Nam'],Thu=Thu,Chi=Chi,NH=NH,loai=loai,Home=session['Home'],Thang_max=session['Thang_max'],Nam_max=session['Nam_max'])
        if request.form.get('Trang')=='Sau':
            session['Thang'], session['Nam'] = Cong_thang(session['Thang'],session['Nam'])
            loai= Loai().Loai_SLmua(session['Thang'],session['Nam'])
            NH = NhanHang().NH_SLmua(session['Thang'],session['Nam'])
            Chi = PhieuNhap().Tong_Chi(session['Thang'],session['Nam'])
            Thu = HoaDon().Tong_Thu(session['Thang'],session['Nam'])
            return render_template('quan_ly_cong_ty/doanhthu.html',Thang=session['Thang'],Nam=session['Nam'],Thu=Thu,Chi=Chi,NH=NH,loai=loai,Home=session['Home'],Thang_max=session['Thang_max'],Nam_max=session['Nam_max'])
    return render_template('quan_ly_cong_ty/doanhthu.html',Thang=session['Thang'],Nam=session['Nam'],Thu=Thu,Chi=Chi,NH=NH,loai=loai,Home=session['Home'],Thang_max=session['Thang_max'],Nam_max=session['Nam_max'])

@app.route('/quan-ly-cong-ty/chuc-nang',methods=['GET','POST'])
def qlct_CN():
    if session.get('quan_ly_cong_ty')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap')
    if KT_GH(session,'Thang'):
        session.pop('Thang')
    DS = Xuat_Dis()
    thong_bao=""
    a= request.form
    if request.method == 'POST':
        print(a)
        if a.get('Logout')=='out':
            session['quan_ly_cong_ty']= None
            return redirect('/dangnhap')
        elif KT_GH(a,'DangNhap'):
            TrangThai().Update_All(False)
            TaiKhoan().UnBlock_IDCV(2)
            TaiKhoan().UnBlock_IDCV(3)
            TaiKhoan().UnBlock_IDCV(4)
            TaiKhoan().UnBlock_IDCV(5)
            if KT_GH(a,'DangNhap'):
                TrangThai().Update_TT('DangNhap',True)
            if KT_GH(a,'BanHang'):
                TrangThai().Update_TT('BanHang',True)
                TaiKhoan().Block_IDCV(4)
            if KT_GH(a,'NhapHang'):
                TrangThai().Update_TT('NhapHang',True)
                TaiKhoan().Block_IDCV(5)
            if KT_GH(a,'QLBanHang'):
                TrangThai().Update_TT('QLBanHang',True)
                TaiKhoan().Block_IDCV(3)
            if KT_GH(a,'QLNhapHang'):
                TrangThai().Update_TT('QLNhapHang',True)
                TaiKhoan().Block_IDCV(2)
            return redirect('/quan-ly-cong-ty/chuc-nang')
        elif KT_GH(a,'NH'):
            if a.get('NH').replace(" ","")=="":
                thong_bao = Markup('<div class="alert alert-danger text-center" role="alert">Vui lòng điền nhãn hàng trước khi thêm</div>')
            elif NhanHang().Check_NH(a.get('NH'))!=0:
                 thong_bao = Markup('<div class="alert alert-danger text-center" role="alert">Nhãn hàng đã tồn tại</div>')
            else:
                thong_bao = Markup('<div class="alert alert-success" role="alert">Đã được thêm</div>')
                NhanHang().add_NH(a.get('NH'))
        elif KT_GH(a,'Loai'):
            if a.get('Loai').replace(" ","")=="":
                thong_bao = Markup('<div class="alert alert-danger text-center" role="alert">Vui lòng điền loại hàng trước khi thêm</div>')
            elif Loai().Check_Loai(a.get('Loai'))!=0:
                 thong_bao = Markup('<div class="alert alert-danger text-center" role="alert">Loại hàng đã tồn tại</div>')
            else:
                thong_bao = Markup('<div class="alert alert-success" role="alert">Đã được thêm</div>')
                Loai().add_Loai(a.get('Loai'))
        else:
            TrangThai().Update_All(False)
            TaiKhoan().UnBlock_IDCV(2)
            TaiKhoan().UnBlock_IDCV(3)
            TaiKhoan().UnBlock_IDCV(4)
            TaiKhoan().UnBlock_IDCV(5)
            return redirect('/quan-ly-cong-ty/chuc-nang')
    return render_template('quan_ly_cong_ty/chucnang.html',Home=session['Home'],DS=DS,thong_bao=thong_bao)


