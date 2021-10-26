from project import app
from flask import render_template, request, redirect , session, Markup
from project.models.khachhang import Doc_DS_DH ,save_list_KH ,check_TTKH, fake_TTGH ,random_id
from project.models.sanpham import KT_GH ,TongTien,SanPham ,Tao_gio_hang, XuLy_Ten
from project.models.XuLy.XuLy_NVBH import tach_id ,LapHD
from project.models.loai import Loai
from project.models.nhanhang import NhanHang
from project.models.taikhoan import TaiKhoan


@app.route('/nhan-vien-ban-hang-<string:id>',methods=['GET','POST'])
def ban_hang(id):
    if session.get('nhan_vien_ban_hang')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap')
    chuoi_tim=""
    sanpham = SanPham().Lay_Sp()
    dsLoai = Loai().Lis_Loai()
    dsNH = NhanHang().Lis_NH()
    if request.method == 'POST':
        if KT_GH(request.form,'Logout'):
            if request.form.get('Logout')=='out':
                session['nhan_vien_ban_hang']= None
                return redirect('/dangnhap')
        if KT_GH(request.form,'TH_gt_tim'):
            chuoi_tim = request.form.get('TH_gt_tim')
            sanpham = SanPham().Tim_kiem_ten(XuLy_Ten(chuoi_tim))
        if KT_GH(request.form,'Loai'):
            sanpham = SanPham().Tim_TheoLoai(request.form.get('Loai'))
        if KT_GH(request.form,'NhanHang'):
            sanpham = SanPham().Tim_TheoNH(request.form.get('NhanHang'))
    
    session['Home'] = '/nhan-vien-ban-hang-'+id
    return render_template('nhan_vien_ban_hang/index.html',danh_sach_sanpham=sanpham,Home = session['Home'],id =id,dsNH=dsNH,dsLoai=dsLoai,chuoi_tim=chuoi_tim)

@app.route('/danh-sach-khach-hang-dang-cho-xu-ly', methods=['GET','POST'])
def danh_sach_KH():
    DS_KH  = Doc_DS_DH()
    if session.get('nhan_vien_ban_hang')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap') 
    if request.method == 'POST':
        if KT_GH(request.form,'Logout'):
            if request.form.get('Logout')=='out':
                session['nhan_vien_ban_hang']= None
                return redirect('/dangnhap')
        if KT_GH(request.form,'ThaoTac'):
            Thao_tac = request.form.get('ThaoTac')
            id, thao_tac = tach_id(Thao_tac)
            if thao_tac=='XemTT':
                DS_KH[id]["TrangThai"]="Đang xử lý"
                save_list_KH(DS_KH)
                return redirect('/don-hang/'+id)
            if thao_tac =='DELETE':
                DS_KH.pop(id)
                save_list_KH(DS_KH)
    return render_template('/nhan_vien_ban_hang/danhSachKH.html',DS_KH =DS_KH,Home = session['Home'])

@app.route('/don-hang/<string:id>', methods=['GET','POST'])
def don_hang(id):
    if session.get('nhan_vien_ban_hang')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False:
        return redirect('/dangnhap') 
    DS_KH = Doc_DS_DH()
    Thong_bao =""
    if KT_GH(DS_KH,id):
        data = DS_KH[id]
    else:
        return redirect(session['Home'])
    GioHang = data['GioHang']
    if request.method == 'POST':
        if KT_GH(request.form,'Logout'):
            if request.form.get('Logout')=='out':
                DS_KH[id]["TrangThai"]="Chờ xử lý"
                save_list_KH(DS_KH)
                session['nhan_vien_ban_hang']= None
                return redirect('/dangnhap')
        if KT_GH(request.form,'Thao_tac'):
            thao_tac = request.form.get('Thao_tac')
            if thao_tac=='Out':
                DS_KH[id]["TrangThai"]="Chờ xử lý"
                save_list_KH(DS_KH)
                return redirect('/danh-sach-khach-hang-dang-cho-xu-ly')
            if thao_tac=='XacNhan':
                NV_BH = session.get('nhan_vien_ban_hang')
                if LapHD(id ,NV_BH,data)==1:
                    DS_KH.pop(id)
                    save_list_KH(DS_KH)
                    return redirect('/danh-sach-khach-hang-dang-cho-xu-ly')
                else:
                    Thong_bao = Markup('<div class="alert alert-danger text-center" role="alert">Hàng trong kho không đủ</div>')
    return render_template('/nhan_vien_ban_hang/donhang.html',data= data,Gio_hang =GioHang,Tongtien=TongTien(GioHang),Thong_bao=Thong_bao)

@app.route('/ban-san-pham-<string:IdSP>', methods=['GET','POST'])
def nvbh_ban(IdSP):
    if session.get('nhan_vien_ban_hang')==None or TaiKhoan().Lay_TrangThai_id(session.get('id'))==False : 
        return redirect('/dangnhap')

    data = SanPham().Lay_SP_id(IdSP) 
    
    if KT_GH(session,IdSP):
        pass
    else:
        session[IdSP]=0
   
    if request.method == 'POST':
        if KT_GH(request.form,IdSP):
            session[IdSP] = int(request.form.get(IdSP))
            return render_template('nhan_vien_ban_hang/new.html',data=data,Home=session['Home'],SL=session[IdSP])
        if KT_GH(request.form,'Logout'):
            if request.form.get('Logout')=='out':
                session['nhan_vien_ban_hang']= None
                return redirect('/dangnhap')
        lenh = request.form
        if KT_GH(lenh,'NameKH'):
            if check_TTKH(lenh.get('NameKH'),lenh.get('DC_KH'),lenh.get('SDT_KH')):
                Gio_hang =[]
                a = Tao_gio_hang(Gio_hang,IdSP,session[IdSP])
                lis_fake = fake_TTGH(lenh.get('NameKH'),lenh.get('DC_KH'),lenh.get('SDT_KH'),a)
                NV_BH = session.get('nhan_vien_ban_hang')
                if LapHD( random_id(10),NV_BH,lis_fake)==1:
                    session[IdSP]=0
                    return redirect(session['Home'])
    return render_template('nhan_vien_ban_hang/new.html',data=data,Home=session['Home'],SL=session[IdSP])