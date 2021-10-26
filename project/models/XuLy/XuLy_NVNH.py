from project.models.phieunhap import PhieuNhap
from datetime import datetime


def add_PN(NVNH,idsp,sl):
    now = datetime.now()
    s1 = now.strftime("%Y-%m-%d")
    id_NV = NVNH['id']
    a = PhieuNhap().Them_PN([id_NV,idsp,sl,s1])
    return 1

