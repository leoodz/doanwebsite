from flask import Flask

app = Flask(__name__)
app.secret_key = 'do_an_m1_2021'

import project.run_app_DangNhap
import project.run_app_nguoidung
import project.app_nhan_vien_ban_hang
import project.app_nhan_vien_nhap_hang
import project.app_quan_ly_ban_hang
import project.app_quan_ly_cong_ty
import project.app_quan_ly_nhap_hang
import project.app_thong_tin_nv
import project.app_quen_mat_khau