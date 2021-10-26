from project import app
from flask import render_template, request, redirect , session, sessions
from project.models.taikhoan import TaiKhoan , xu_ly_sang_json



@app.route('/dangnhap', methods=['GET','POST'])
def dangnhap():
    session.clear()
    b =TaiKhoan()
    thong_bao = ""
    if request.method =='POST':
        TenTK = request.form.get('TenTK')
        pws = request.form.get('pws')
        thongtin = b.DangNhap(TenTK,pws)
        if thongtin == None:
            thong_bao='Sai tên đăng nhập và mật khẩu \n Liên hệ quản lý để lấy lại mật khẩu'
        elif thongtin[4]==0:
            thong_bao='Tài khoản của bạn đã bị khóa'
        else:
            if thongtin[2]==1:
                session['quan_ly_cong_ty']= xu_ly_sang_json(thongtin)   #   do dữ liệu trả về của SQL là dạng cột 
                session['id']=thongtin[0]
                return redirect('/quan-ly-cong-ty-'+thongtin[0])                     # session chỉ nhận dữ liệu dạng JSON (nếu không sử lý chương trình sẽ báo lỗi)
            if thongtin[2]==2:
                session['quan_ly_nhap_hang']= xu_ly_sang_json(thongtin)
                session['id']=thongtin[0]
                return redirect('/quan-ly-nhap-hang-'+thongtin[0])
            if thongtin[2]==3:
                session['quan_ly_ban_hang']= xu_ly_sang_json(thongtin)
                session['id']=thongtin[0]
                return redirect('/quan-ly-ban-hang-'+thongtin[0])
            if thongtin[2]==4:
                session['nhan_vien_ban_hang']= xu_ly_sang_json(thongtin)
                session['id']=thongtin[0]
                return redirect('/nhan-vien-ban-hang-'+thongtin[0])
            if thongtin[2]==5:
                session['nhan_vien_nhap_hang']= xu_ly_sang_json(thongtin)
                session['id']=thongtin[0]
                return redirect('/nhan-vien-nhap-hang-'+thongtin[0])
    return render_template('dangnhap/dangnhap.html',thong_bao=thong_bao)