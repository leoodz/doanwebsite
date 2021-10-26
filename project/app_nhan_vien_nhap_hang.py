from project import app
from flask import render_template, request, Markup, redirect , session
from project.models.sanpham import SanPham ,KT_GH, XuLy_Ten, check_TTSP
from project.models.XuLy.XuLy_NVNH import add_PN
from project.models.loai import Loai
from project.models.nhanhang import NhanHang
from project.models.taikhoan import TaiKhoan, random_id



@app.route('/nhan-vien-nhap-hang-<string:id>',methods=['GET','POST'])
def nhap_hang(id):
    if session.get('nhan_vien_nhap_hang')==None:
        return redirect('/dangnhap')
    dsNH = NhanHang().Lis_NH()
    dsLoai = Loai().Lis_Loai()
    sanpham = SanPham().Lay_Sp()
    chuoi_tim=""
    if request.method == 'POST':
        if request.form.get('Logout')=='out':
            session['nhan_vien_nhap_hang']= None
            return redirect('/dangnhap')
        if KT_GH(request.form,'TH_gt_tim'):
            chuoi_tim = request.form.get('TH_gt_tim')
            sanpham = SanPham().Tim_kiem_ten(XuLy_Ten(chuoi_tim))
        if KT_GH(request.form,'Loai'):
            sanpham = SanPham().Tim_TheoLoai(request.form.get('Loai'))
        if KT_GH(request.form,'NhanHang'):
            sanpham = SanPham().Tim_TheoNH(request.form.get('NhanHang'))
    session['Home'] = '/nhan-vien-nhap-hang-'+id
    return render_template('nhan_vien_nhap_hang/index.html',danh_sach_sanpham=sanpham,Home = session['Home'],id =id,dsNH=dsNH,dsLoai=dsLoai,chuoi_tim=chuoi_tim)



@app.route('/nhap-san-pham-<string:IdSP>', methods=['GET','POST'])
def nvnh_SL(IdSP):
    if session.get('nhan_vien_nhap_hang')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap')

    data = SanPham().Lay_SP_id(IdSP) 

    if request.method == 'POST':
        if KT_GH(request.form,IdSP):
            SL_them = request.form.get(IdSP)
            TongSL=data[8]+int(SL_them)
            if add_PN(session.get('nhan_vien_nhap_hang'),IdSP,int(SL_them)):
                a = SanPham().update_SL(IdSP,TongSL)
                return redirect(session['Home'])
        if KT_GH(request.form,'Logout'):
            if request.form.get('Logout')=='out':
                session['nhan_vien_nhap_hang']= None
                return redirect('/dangnhap')
    return render_template('nhan_vien_nhap_hang/them_SL.html',data=data,Home=session['Home'])



@app.route('/them-san-pham-<string:Id>', methods=['GET','POST'])
def nvnh_addSP(Id):
    Thong_bao = ""
    if session.get('nhan_vien_nhap_hang')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap')
    loai = Loai().Lis_Loai()
    nh = NhanHang().Lis_NH()
    if request.method == 'POST':
        if KT_GH(request.form,'Logout'):
            if request.form.get('Logout')=='out':
                session['nhan_vien_nhap_hang']= None
                return redirect('/dangnhap')
        NameSP = request.form.get("NameSP")
        MaLoai = request.form.get("MaLoai")
        MaNH = request.form.get("MaNH")
        Buy = request.form.get("Buy")
        Sell = request.form.get("Sell")
        ImageUrl ="MacDinh.png"
        Description = request.form.get("Description")
        SL = request.form.get("SL")
        
        if request.files.get('f'):
            f = request.files.get('f')
            f.save('project/static/images/' + f.filename)
            ImageUrl = f.filename
        if check_TTSP(NameSP,MaLoai,MaNH,Buy,Sell,ImageUrl,Description,SL)==False:
            Thong_bao = Markup('<div class="alert alert-danger" role="alert">Vui lòng điền đầy đủ thông tin</div>')
        else:
            IdSP = random_id(10)
            a = (IdSP,NameSP,int(MaLoai),int(MaNH),int(Buy),int(Sell),ImageUrl,Description,int(SL))
            if SanPham().add_Sanpham(a)>0:
                add_PN(session.get('nhan_vien_nhap_hang'),IdSP,int(SL))
                Thong_bao = Markup('<div class="alert alert-success" role="alert">Đã thêm thành sản phẩm thành công</div>')
    return render_template('nhan_vien_nhap_hang/nhaphang.html',Home=session['Home'],nh=nh,loai=loai,Thong_bao=Thong_bao)


