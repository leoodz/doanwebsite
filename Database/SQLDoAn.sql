

CREATE DATABASE QLBH
go 

-- Phân chia Chức Vụ Để Cấp Quyền 
CREATE TABLE dbo.ChucVu(
IDCV INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
NameCV NVARCHAR(20) NOT NULL
)

-- Thông Tin Đang Nhập 
CREATE TABLE dbo.TaiKhoan(
id CHAR(10) NOT NULL PRIMARY KEY, 
TenTK CHAR(15) NOT NULL,
IDCV INT NOT NULL REFERENCES dbo.ChucVu(IDCV),
pws CHAR(32) NOT NULL,
TT BIT NOT NULL -- 0 la block, 1 la unloock
);


INSERT INTO dbo.ChucVu
(
    NameCV
)
VALUES
(N'Quản Lý Công Ty' ), --chú ý những thành phần ở đây vị trí có thể ảnh hưởng tới quyền truy cập web
(N'Quản Lý Nhập Hàng' ),
(N'Quản Lý Bán Hàng' ),
(N'Nhân Viên Bán Hàng'),
(N'Nhân Viên Nhập Hàng');


-- MD5 
--INSERT INTO dbo.TaiKhoan(TenTK,IDCV,pws)VALUES('Tai2580',1,HashBytes('MD5', 'Tai4564567'));  
-- cách này không hiệu quả,  nên mã hóa trước khi đưa vào database 
--SELECT * FROM dbo.TaiKhoan WHERE pws= HashBytes('MD5', 'Tai4564567')
-- do sử lý ở database nên dễ sảy ra lỗi 


CREATE TABLE dbo.Loai(
MaLoai INT NOT NULL PRIMARY KEY IDENTITY(1,1),
NameLoai NVARCHAR(25) NOT NULL 
);


-- Phân loại thiết bị
INSERT INTO dbo.Loai
(
    NameLoai
)
VALUES
(N'Khác'),
(N'Laptop' ),
(N'Mouse' ),
(N'Keyboard' ),
(N'HDD' ),
(N'HeadrPhone'),
(N'Tivi');



-- Nhãn Hàng
CREATE TABLE dbo.NhanHang(
MaNH INT NOT NULL PRIMARY KEY IDENTITY(1,1),
NameNH NVARCHAR(20) NOT NULL
);

INSERT INTO dbo.NhanHang
(
    NameNH
)
VALUES
(N'Khác'), 
(N'SONY'),
(N'SAMSUNG'),
(N'RAZER'),
(N'ASUS'),
(N'MSI'),
(N'ACER');


-- San Pham
-- Lưu ý MaLoai và MaNH ảnh hưởng  đến tính Sản phẩm 
CREATE TABLE dbo.SanPham(
IdSP CHAR(10) NOT NULL PRIMARY KEY, -- Co the sua lai (CHU Y)
NameSP NVARCHAR(128) NOT NULL,
MaLoai INT NOT NULL REFERENCES dbo.Loai(MaLoai),
MaNH INT NOT NULL REFERENCES dbo.NhanHang(MaNH),
Buy BIGINT ,
Sell BIGINT,
ImageUrl VARCHAR(128),
Description NVARCHAR(Max),
SL SMALLINT NOT NULL,
);


--Tao table thong tin=========================================================

CREATE TABLE dbo.ThongTinNV(
id CHAR(10) PRIMARY KEY REFERENCES dbo.TaiKhoan(id),
NameNV NVARCHAR(25),
GT BIT , -- 0 la Nam ,1 la Nu
NS DATE,
SDT CHAR(11),
DiaChi NVARCHAR(50)
);


CREATE TABLE dbo.ThongTinKH(
idKH CHAR(10) PRIMARY KEY,
NameKH NVARCHAR(25) NOT NULL,
DCKH NVARCHAR(50) NOT NULL,
SDTKH CHAR(11) NOT NULL
);

CREATE TABLE dbo.HoaDon(
MaHD CHAR(20) PRIMARY KEY,
idKH CHAR(10) NOT NULL REFERENCES dbo.ThongTinKH(idKH),
id CHAR(10) NOT NULL REFERENCES dbo.TaiKhoan(id),
DateTT DATE ,
TongTien BIGINT,
);

CREATE TABLE dbo.CTHD(
MaHD CHAR(20) NOT NULL  FOREIGN KEY REFERENCES dbo.HoaDon(MaHD),
IdSP CHAR(10) NOT NULL FOREIGN KEY REFERENCES dbo.SanPham(IdSP),
SlMua INT CHECK(SlMua>0),
);

CREATE TABLE dbo.PhieuNhap(
id CHAR(10) NOT NULL FOREIGN KEY REFERENCES dbo.TaiKhoan(id),
IdSP CHAR(10) NOT NULL FOREIGN KEY REFERENCES dbo.SanPham(IdSP),
SLThem INT CHECK(SLThem >0),
NgayNhap date
)
-- Luu ý table này để lưu các trạng thái của quản lý cong ty , dùng để lưu các chức năng đang hoạt dọng hay tắt 
CREATE TABLE dbo.TrangThai(
NameTT CHAR(20) PRIMARY KEY,
TrangThai BIT
)

INSERT INTO dbo.TrangThai(
	NameTT,
	TrangThai
)
VALUES
('DangNhap',0),
('QLBanHang',0),
('QLNhapHang',0),
('BanHang',0),
('NhapHang',0);


--============================================
-- Chu y phan insert san pham
/*SELECT *  FROM dbo.SanPham
SELECT * FROM dbo.TaiKhoan
SELECT * FROM dbo.ChucVu
SELECT * FROM dbo.PhieuNhap 
SELECT * FROM dbo.TaiKhoan
SELECT * FROM dbo.CTHD
SELECT * FROM dbo.HoaDon
SELECT * FROM dbo.ThongTinNV
SELECT * FROM dbo.Loai*/


/*SELECT DISTINCT TaiKhoan.id, NameNV,NS,SDT,TT ,(SELECT COUNT(id) FROM dbo.PhieuNhap WHERE id=dbo.ThongTinNV.id AND MONTH(NgayNhap)='10' AND YEAR(NgayNhap)='2021')
				AS 'SoPN', (SELECT SUM(SlThem) FROM dbo.PhieuNhap WHERE id=dbo.ThongTinNV.id  AND MONTH(NgayNhap)='10' AND YEAR(NgayNhap)='2021')
				AS 'TongHN' FROM dbo.PhieuNhap,dbo.ThongTinNV,dbo.TaiKhoan WHERE dbo.TaiKhoan.IDCV='5' AND dbo.TaiKhoan.id=dbo.ThongTinNV.id*/
--dem so hd theo hoa don

/*SELECT TaiKhoan.id, NameNV,NS,SDT,TT , ( SELECT COUNT(DISTINCT a.MaHD) FROM dbo.CTHD a, dbo.HoaDon b WHERE a.MaHD=b.MaHD AND b.id=dbo.TaiKhoan.id AND 
			MONTH(b.DateTT)='10' AND YEAR(b.DateTT)='2021') as 'TongHD',( SELECT SUM(a.SlMua) FROM dbo.CTHD a, dbo.HoaDon b WHERE a.MaHD=b.MaHD AND 
			b.id=dbo.TaiKhoan.id AND MONTH(b.DateTT)='10' AND YEAR(b.DateTT)='2021') as'TongSP' FROM dbo.ThongTinNV ,dbo.TaiKhoan  WHERE dbo.TaiKhoan.IDCV=4 AND
			dbo.ThongTinNV.id=dbo.TaiKhoan.id*/


/*SELECT dbo.Loai.MaLoai,NameLoai, (SELECT ISNULL(SUM(a.SlMua),0) 
									FROM dbo.CTHD a, dbo.HoaDon b,dbo.SanPham d 
									WHERE a.MaHD=b.MaHD AND a.IdSP=d.IdSP AND dbo.Loai.MaLoai=d.MaLoai AND MONTH(b.DateTT)='10' AND YEAR(b.DateTT)='2021')
									AS 'TongSP' FROM dbo.Loai 
									ORDER BY MaLoai DESC*/

/*SELECT dbo.NhanHang.MaNH,dbo.NhanHang.NameNH, (SELECT ISNULL(SUM(a.SlMua),0)
												FROM dbo.CTHD a, dbo.HoaDon b,dbo.SanPham d 
												WHERE a.MaHD=b.MaHD AND a.IdSP=d.IdSP AND d.MaNH=dbo.NhanHang.MaNH AND MONTH(b.DateTT)='10' AND YEAR(b.DateTT)='2021')
												AS 'TongSP' FROM dbo.NhanHang
												ORDER BY MaNH DESC*/

--SELECT COUNT(NgayNhap) AS 'TongPN' FROM dbo.PhieuNhap WHERE MONTH(NgayNhap)='10'AND YEAR(NgayNhap)='2021'
--SELECT SUM(SLThem) AS 'TongSPThem' FROM dbo.PhieuNhap WHERE MONTH(NgayNhap)='10'AND YEAR(NgayNhap)='2021'
--SELECT SUM(SlMua) AS 'TongSPMonth' FROM dbo.CTHD a,dbo.HoaDon b WHERE a.MaHD=b.MaHD AND MONTH(b.DateTT)='10' AND YEAR(b.DateTT)='2021'
--SELECT COUNT(DISTINCT a.MaHD ) AS 'TongHDMonth' FROM dbo.CTHD a, dbo.HoaDon b WHERE a.MaHD=b.MaHD AND MONTH(b.DateTT)='10' AND YEAR(b.DateTT)='2021'

--SELECT id, ( SELECT SUM(a.SlMua) FROM dbo.CTHD a, dbo.HoaDon b WHERE a.MaHD=b.MaHD AND b.id=dbo.TaiKhoan.id) as'TongSP' FROM dbo.TaiKhoan WHERE IDCV=4
--SELECT SUM(a.SlMua) FROM dbo.CTHD a, dbo.HoaDon b WHERE a.MaHD=b.MaHD AND b.id='3m1q7a7e5p'
--SELECT a.id,a.NameNV,a.NS,a.GT,a.DiaChi,a.SDT,b.TenTK,b.TT FROM dbo.ThongTinNV a, dbo.TaiKhoan b WHERE a.id =b.id AND b.IDCV=4

/*SELECT a.IdSP,c.NameSP,a.NgayNhap,a.SLThem,c.Buy,c.ImageUrl 
FROM dbo.PhieuNhap a,dbo.ThongTinNV b, dbo.SanPham c 
WHERE a.IdSP=c.IdSP AND b.id=a.id AND MONTH(a.NgayNhap)='10' AND YEAR(a.NgayNhap)='2021' AND a.id='5x2w6w2t7h'*/

--SELECT  ISNULL(SUM(a.SLThem * b.Buy),0) AS 'TongChi' FROM PhieuNhap a, SanPham b WHERE a.IdSP=b.IdSP AND MONTH(a.NgayNhap)='10' AND YEAR(a.NgayNhap)='2021'

--SELECT  ISNULL(SUM(TongTien),0) AS 'TongThu' FROM  HoaDon WHERE MONTH(DateTT)='11' AND YEAR(DateTT)='2021'


--SELECT a.IDCV,b.IdSP,c.NameCV FROM dbo.TaiKhoan a, dbo.PhieuNhap b, dbo.ChucVu c WHERE a.id=b.id AND c.IDCV=a.IDCV
--SELECT * FROM dbo.ThongTinKH
--SELECT * FROM dbo.HoaDon
--SELECT * FROM dbo.CTHD

--SELECT a.MaHD,a.DateTT,a.TongTien,b.NameKH FROM dbo.HoaDon a, dbo.ThongTinKH b WHERE a.idKH=b.idKH AND a.id='3m1q7a7e5p' AND MONTH(a.DateTT)='10' AND YEAR(a.DateTT)='2021'
--SELECT b.NameSP,b.ImageUrl , b.Sell,a.SlMua ,b.Sell*a.SlMua AS 'ThanhTien' FROM dbo.CTHD a, dbo.SanPham b WHERE MaHD='7x3p6u1l4j0r7a0f3h3g' AND a.IdSP=b.IdSP
-- DELETE dbo.CTHD DELETE dbo.HoaDon DELETE dbo.ThongTinKH
-- UPDATE dbo.SanPham SET SL=10, Description=N'Mới 100%' WHERE IdSP='1n9f6a4j8l'
-- chuot-may-tinh-asus-tuf-gaming-m3-2_f1ab2f623d0343cebb5216f3a46b7466.jpg




