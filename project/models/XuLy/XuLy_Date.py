
def Tru_thang(thang,nam):
    if thang == 1:
        thang = 12
        nam -= 1
    else:
        thang=thang-1
    return thang,nam

def Cong_thang(thang,nam):
    if thang == 12:
        thang = 1
        nam = nam +1
    else:
        thang=thang+1
    return thang,nam
