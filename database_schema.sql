DROP DATABASE IF EXISTS restoran_db;
CREATE DATABASE restoran_db;
USE restoran_db;

-- 1. Table Pelanggan
CREATE TABLE pelanggan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    no_telepon VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100),
    tanggal_daftar TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nama (nama),
    INDEX idx_telepon (no_telepon)
);

-- 2. Table Kategori Menu
CREATE TABLE kategori_menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_kategori VARCHAR(50) NOT NULL,
    deskripsi TEXT
);

-- 3. Table Menu
CREATE TABLE menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_menu VARCHAR(100) NOT NULL,
    kategori_id INT,
    harga DECIMAL(10,2) NOT NULL,
    deskripsi TEXT,
    stok INT DEFAULT 0,
    FOREIGN KEY (kategori_id) REFERENCES kategori_menu(id),
    INDEX idx_nama (nama_menu),
    INDEX idx_kategori (kategori_id)
);

-- 4. Table Meja
CREATE TABLE meja (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomor_meja VARCHAR(10) UNIQUE NOT NULL,
    kapasitas INT NOT NULL,
    status ENUM('tersedia', 'dipesan', 'terisi') DEFAULT 'tersedia',
    lokasi VARCHAR(50),
    INDEX idx_status (status),
    INDEX idx_nomor (nomor_meja)
);

-- 5. Table Pesanan
CREATE TABLE pesanan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_pesanan VARCHAR(20) UNIQUE NOT NULL,
    pelanggan_id INT,
    meja_id INT,
    tanggal_pesanan DATETIME DEFAULT CURRENT_TIMESTAMP,
    status_pesanan ENUM('diproses', 'disajikan', 'selesai', 'dibatalkan') DEFAULT 'diproses',
    total_harga DECIMAL(12,2) DEFAULT 0,
    catatan TEXT,
    FOREIGN KEY (pelanggan_id) REFERENCES pelanggan(id),
    FOREIGN KEY (meja_id) REFERENCES meja(id),
    INDEX idx_tanggal (tanggal_pesanan),
    INDEX idx_status (status_pesanan),
    INDEX idx_kode (kode_pesanan)
);

-- 6. Table Detail Pesanan
CREATE TABLE detail_pesanan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pesanan_id INT NOT NULL,
    menu_id INT NOT NULL,
    jumlah INT NOT NULL,
    harga_satuan DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) AS (jumlah * harga_satuan) STORED,
    FOREIGN KEY (pesanan_id) REFERENCES pesanan(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_id) REFERENCES menu(id),
    INDEX idx_pesanan (pesanan_id)
);

-- 7. Insert Sample Data
INSERT INTO kategori_menu (nama_kategori, deskripsi) VALUES 
('Appetizer', 'Makanan pembuka'),
('Main Course', 'Hidangan utama'),
('Dessert', 'Makanan penutup'),
('Beverage', 'Minuman');

INSERT INTO menu (nama_menu, kategori_id, harga, stok, deskripsi) VALUES
('Caesar Salad', 1, 45000, 20, 'Salad dengan saus caesar spesial'),
('Cream Soup', 1, 35000, 15, 'Sup krim jagung'),
('Grilled Salmon', 2, 125000, 10, 'Salmon bakar dengan lemon butter sauce'),
('Beef Steak', 2, 150000, 8, 'Steak daging sapi dengan kentang tumbuk'),
('Chocolate Cake', 3, 40000, 12, 'Kue coklat dengan vanilla ice cream'),
('Ice Cream', 3, 25000, 30, '3 scoop ice cream pilihan'),
('Orange Juice', 4, 20000, 50, 'Jus jeruk segar'),
('Coffee', 4, 15000, 40, 'Kopi hitam atau dengan susu'),
('Tea', 4, 10000, 60, 'Teh panas atau dingin');

INSERT INTO meja (nomor_meja, kapasitas, lokasi) VALUES
('A01', 2, 'Area Smoking'),
('A02', 4, 'Area Non-Smoking'),
('A03', 2, 'Window Side'),
('B01', 6, 'VIP Area'),
('B02', 8, 'Family Area'),
('B03', 4, 'Terrace'),
('C01', 4, 'Garden View'),
('C02', 10, 'Private Room');

INSERT INTO pelanggan (nama, no_telepon, email) VALUES
('Budi Santoso', '081234567890', 'budi@email.com'),
('Siti Aminah', '082345678901', 'siti@email.com'),
('Agus Wijaya', '083456789012', NULL),
('Dewi Lestari', '084567890123', 'dewi@email.com');

-- Test pesanan
INSERT INTO pesanan (kode_pesanan, pelanggan_id, meja_id, catatan) VALUES
('RES240115001', 1, 1, 'Tidak pakai bawang'),
('RES240115002', 2, 3, 'Extra spicy');

INSERT INTO detail_pesanan (pesanan_id, menu_id, jumlah, harga_satuan) VALUES
(1, 3, 2, 125000),
(1, 8, 1, 15000),
(2, 4, 1, 150000),
(2, 7, 2, 20000);

-- Update total harga
UPDATE pesanan SET total_harga = 265000 WHERE id = 1;
UPDATE pesanan SET total_harga = 190000 WHERE id = 2;

-- Update status meja
UPDATE meja SET status = 'terisi' WHERE id IN (1, 3);

SELECT 'DATABASE SETUP COMPLETE!' as status;

