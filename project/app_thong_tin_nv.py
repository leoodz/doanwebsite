from project import app
from flask import render_template, request, redirect , session,Markup
from project.models.sanpham import KT_GH
from project.models.taikhoan import TaiKhoan,Bam_mk
from project.models.nhanvien import NhanVien
from project.models.chucvu import Chucvu

@app.route('/thong-tin-ca-nhan/<string:id>',methods=['GET','POST'])
def thong_tin(id):
    if session.get('id')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap')
    thong_bao=""
    thong_tin_TK = TaiKhoan().Lay_TaiKhoan_id(id) 
    thong_tin_CN = NhanVien().Lay_NV_id(id)
    CV = Chucvu().Lay_CV_id(thong_tin_TK[2])
    if KT_GH(session,'Thang'):
        session.pop('Thang')
    if request.method=='POST':
        a = request.form
        if KT_GH(request.form,'Logout'):
            if request.form.get('Logout')=='out':
                return redirect('/dangnhap')
        if KT_GH(a,'NameNV') and KT_GH(a,'GT') and KT_GH(a,'Date') and KT_GH(a,'SDT') and KT_GH(a,'DiaChi') :
            NameNV = a.get('NameNV')
            GT =  a.get('GT')
            Date = a.get('Date')
            SDT = a.get('SDT')
            DiaChi = a.get('DiaChi')
            if NameNV.replace(" ", "")=="" or GT.replace(" ", "")=="" or Date.replace(" ", "")=="" or SDT.replace(" ", "")=="" or DiaChi.replace(" ", "")=="":
                thong_bao = Markup('<div class="alert alert-danger text-center" role="alert">Không được để trống thông tin</div>')

            elif NhanVien().update_NV(id,NameNV,GT,Date,SDT,DiaChi) > 0:
                return redirect("/thong-tin-ca-nhan/"+id)
            else: 
                thong_bao = Markup('<div class="alert alert-danger text-center" role="alert">Cập nhật thất bại</div>')
        elif KT_GH(a,'pwd') and KT_GH(a,'new-Pwd-1') and KT_GH(a,'new-Pwd-2'):
            MKC = a.get('pwd')
            MKM_1 = a.get('new-Pwd-1')
            MKM_2 = a.get('new-Pwd-2')
            if Bam_mk(MKC) != thong_tin_TK[3]:
                thong_bao = Markup('<div class="alert alert-danger text-center" role="alert">Sai mật khẩu cũ</div>')
            elif MKM_1 != MKM_2:
                thong_bao = Markup('<div class="alert alert-danger text-center" role="alert">Mật khẩu mới không giống nhau</div>')
            else: 
                TaiKhoan().doi_MK([Bam_mk(MKM_1),id])
                thong_bao = Markup('<div class="alert alert-success text-center" role="alert">Đổi mật khẩu thành công</div>')
    return render_template("thong_tin_nv/index.html",Home=session['Home'],CN =thong_tin_CN,CV=CV,thong_bao=thong_bao)