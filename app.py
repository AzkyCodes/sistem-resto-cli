#!/usr/bin/env python3
"""
SISTEM PEMESANAN RESTORAN - MAIN APPLICATION
Aplikasi utama yang mengintegrasikan semua komponen
Memenuhi 8 unit kompetensi sertifikasi programmer
"""

import sys
import os
import subprocess
from datetime import datetime, timedelta

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_connection import DatabaseConnection
from database.crud_operations import CRUDOperations
from models.pelanggan import Pelanggan
from models.meja import Meja
from models.pesanan import Pesanan
from models.laporan import LaporanGenerator
from models.menu import Menu
from utils.validasi_input import Validator
from utils.pdf_generator import PDFGenerator
from utils.logger import setup_logger

class SistemRestoran:
    """
    Class utama aplikasi sistem restoran
    Mengintegrasikan semua komponen yang dibangun
    """
    
    def __init__(self):
        """Initialize sistem dengan semua komponen"""
        self.logger = setup_logger('app_main')
        self.db = DatabaseConnection()
        self.crud = CRUDOperations()
        self.validator = Validator()
        self.pdf_gen = PDFGenerator()
        
        self.logger.info("Sistem Restoran diinisialisasi")
    
    def run(self):
        """Main program loop"""
        self.clear_screen()
        print("=" * 60)
        print("SISTEM PEMESANAN RESTORAN - UNILA CERTIFICATION")
        print("=" * 60)
        print("Dibuat untuk sertifikasi programmer")
        print("Memenuhi 8 unit kompetensi SKKNI")
        print("=" * 60)
        
        # Test koneksi database
        if not self.test_database():
            print("\n❌ ERROR: Tidak bisa terkoneksi ke database!")
            print("Pastikan MySQL berjalan dan database 'restoran_db' ada")
            print("Setup database: mysql -u root -p < database_schema.sql")
            input("\nTekan Enter untuk keluar...")
            sys.exit(1)
        
        self.main_menu()
    
    def clear_screen(self):
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def test_database(self):
        """Test koneksi database"""
        try:
            success = self.db.test_connection()
            if success:
                print("✅ Database connected successfully")
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(f"Database test failed: {e}")
            return False
    
    def main_menu(self):
        """Display main menu"""
        while True:
            self.clear_screen()
            print("\n" + "=" * 60)
            print("MENU UTAMA - SISTEM PEMESANAN RESTORAN")
            print("=" * 60)
            print("1.  Kelola Pelanggan")
            print("2.  Kelola Meja")
            print("3.  Buat Pesanan Baru")
            print("4.  Laporan Pesanan")
            print("5.  Debugging Demo")
            print("6.  Dokumentasi Sistem")
            print("0.  Keluar")
            print("=" * 60)
            
            try:
                choice = input("\nPilih menu [0-8]: ").strip()
                
                if choice == "1":
                    self.kelola_pelanggan()
                elif choice == "2":
                    self.kelola_meja()
                elif choice == "3":
                    self.buat_pesanan()
                elif choice == "4":
                    self.generate_laporan()
                elif choice == "5":
                    self.run_debugging_demo()
                elif choice == "6":
                    self.tampilkan_dokumentasi()
                elif choice == "0":
                    print("\nTerima kasih telah menggunakan sistem!")
                    print("Sistem dibuat untuk sertifikasi programmer UNILA")
                    break
                else:
                    print("⚠️  Pilihan tidak valid! Silakan pilih 0-8")
                    input("Tekan Enter untuk melanjutkan...")
                    
            except KeyboardInterrupt:
                print("\n\nProgram dihentikan oleh user")
                break
            except Exception as e:
                self.logger.error(f"Error di main menu: {e}")
                print(f"❌ Error: {e}")
                input("Tekan Enter untuk melanjutkan...")
    
    # ========== MENU 1: KELOLA PELANGGAN ==========
    
    def kelola_pelanggan(self):
        """Menu kelola pelanggan"""
        while True:
            self.clear_screen()
            print("\n" + "=" * 60)
            print("KELOLA PELANGGAN")
            print("=" * 60)
            print("1.  Daftar Pelanggan")
            print("2.  Tambah Pelanggan Baru")
            print("3.  Update Data Pelanggan")
            print("4.  Hapus Pelanggan")
            print("0.  Kembali ke Menu Utama")
            print("=" * 60)
            
            choice = input("\nPilih aksi: ").strip()
            
            if choice == "1":
                self.daftar_pelanggan()
            elif choice == "2":
                self.tambah_pelanggan()
            elif choice == "3":
                self.cari_pelanggan()
            elif choice == "4":
                self.update_pelanggan()
            elif choice == "5":
                self.hapus_pelanggan()
            elif choice == "0":
                break
            else:
                print("Pilihan tidak valid!")
    
    def daftar_pelanggan(self):
        """Tampilkan semua pelanggan"""
        print("\n" + "-" * 60)
        print("DAFTAR PELANGGAN")
        print("-" * 60)
        
        try:
            pelanggan_list = self.crud.read_pelanggan()
            
            # Pastikan selalu list, bahkan jika None
            if not pelanggan_list:
                pelanggan_list = []
            
            if len(pelanggan_list) == 0:
                print("📭 Belum ada pelanggan terdaftar.")
                print("\n💡 Tips: Tambah pelanggan baru di menu 'Tambah Pelanggan Baru'")
            else:
                print(f"{'ID':<5} {'Nama':<25} {'Telepon':<15} {'Email':<20}")
                print("-" * 70)
                
                for p in pelanggan_list:
                    # Pastikan p adalah dictionary
                    if isinstance(p, dict):
                        email = p.get('email', '-')
                        if email is None:
                            email = '-'
                        print(f"{p.get('id', '-'):<5} {p.get('nama', '-'):<25} {p.get('no_telepon', '-'):<15} {email[:20]:<20}")
                    else:
                        print(f"⚠️  Data tidak valid: {p}")
                
                print(f"\n📊 Total: {len(pelanggan_list)} pelanggan")
        
        except Exception as e:
            self.logger.error(f"Error membaca pelanggan: {e}")
            print(f"❌ Error membaca data pelanggan")
            print(f"🔧 Detail: {e}")
            print("\n💡 Cek: Apakah database 'restoran_db' sudah dibuat?")
            print("       Jalankan: mysql -u root -p < database_schema.sql")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    def tambah_pelanggan(self):
        """Tambah pelanggan baru"""
        print("\n" + "-" * 60)
        print("TAMBAH PELANGGAN BARU")
        print("-" * 60)
        
        try:
            # Input data
            nama = input("Nama lengkap: ").strip()
            telepon = input("No. Telepon: ").strip()
            email = input("Email (opsional): ").strip() or None
            
            # Validasi
            valid_nama, msg_nama = self.validator.validasi_nama(nama)
            valid_telp, msg_telp = self.validator.validasi_telepon(telepon)
            valid_email, msg_email = self.validator.validasi_email(email) if email else (True, "")
            
            if not valid_nama:
                print(f"❌ {msg_nama}")
            elif not valid_telp:
                print(f"❌ {msg_telp}")
            elif not valid_email:
                print(f"❌ {msg_email}")
            else:
                # Create object
                pelanggan_obj = Pelanggan(nama=nama, no_telepon=telepon, email=email)
                
                # Save to database
                pelanggan_id = self.crud.create_pelanggan(nama, telepon, email)
                
                if pelanggan_id:
                    print(f"\n✅ Pelanggan berhasil ditambahkan!")
                    print(f"   ID Pelanggan: {pelanggan_id}")
                    print(f"   Nama: {nama}")
                    
                    # Log activity
                    self.logger.info(f"Pelanggan baru ditambah: {nama} (ID: {pelanggan_id})")
                else:
                    print("❌ Gagal menambahkan pelanggan")
        
        except Exception as e:
            self.logger.error(f"Error tambah pelanggan: {e}")
            print(f"❌ Error: {e}")
        
        input("\nTekan Enter untuk melanjutkan...")
        
    def update_pelanggan(self):
        """Update data pelanggan"""
        print("\n" + "-" * 60)
        print("UPDATE DATA PELANGGAN")
        print("-" * 60)
        
        try:
            pelanggan_id = input("ID Pelanggan yang akan diupdate: ").strip()
            
            if not pelanggan_id.isdigit():
                print("❌ ID harus berupa angka")
            else:
                # Cek apakah pelanggan ada
                pelanggan = self.crud.read_pelanggan(int(pelanggan_id))
                
                if not pelanggan:
                    print(f"❌ Pelanggan dengan ID {pelanggan_id} tidak ditemukan")
                else:
                    print(f"\nData saat ini:")
                    print(f"Nama     : {pelanggan['nama']}")
                    print(f"Telepon  : {pelanggan['no_telepon']}")
                    print(f"Email    : {pelanggan.get('email', '-')}")
                    print("\n" + "-" * 40)
                    
                    # Input data baru
                    print("Masukkan data baru (kosongkan jika tidak ingin mengubah):")
                    
                    nama_baru = input(f"Nama [{pelanggan['nama']}]: ").strip()
                    telepon_baru = input(f"Telepon [{pelanggan['no_telepon']}]: ").strip()
                    email_baru = input(f"Email [{pelanggan.get('email', '')}]: ").strip()
                    
                    # Update hanya jika ada perubahan
                    updates = {}
                    if nama_baru:
                        updates['nama'] = nama_baru
                    if telepon_baru:
                        updates['telepon'] = telepon_baru
                    if email_baru:
                        updates['email'] = email_baru if email_baru else None
                    
                    if updates:
                        success = self.crud.update_pelanggan(
                            int(pelanggan_id),
                            **updates
                        )
                        
                        if success:
                            print("\n✅ Data pelanggan berhasil diupdate!")
                            self.logger.info(f"Pelanggan ID {pelanggan_id} diupdate: {updates}")
                        else:
                            print("❌ Gagal mengupdate data")
                    else:
                        print("⚠️  Tidak ada perubahan yang dilakukan")
        
        except Exception as e:
            self.logger.error(f"Error update pelanggan: {e}")
            print(f"❌ Error: {e}")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    def hapus_pelanggan(self):
        """Hapus pelanggan (soft delete)"""
        print("\n" + "-" * 60)
        print("HAPUS PELANGGAN")
        print("-" * 60)
        
        pelanggan_id = input("ID Pelanggan yang akan dihapus: ").strip()
        
        if not pelanggan_id.isdigit():
            print("❌ ID harus berupa angka")
        else:
            try:
                # Konfirmasi
                confirm = input(f"Yakin ingin menghapus pelanggan ID {pelanggan_id}? (y/n): ").strip().lower()
                
                if confirm == 'y':
                    self.crud.delete_pelanggan(int(pelanggan_id))
                    print("✅ Pelanggan berhasil dihapus (soft delete)")
                    self.logger.info(f"Pelanggan ID {pelanggan_id} dihapus")
                else:
                    print("❌ Penghapusan dibatalkan")
            
            except Exception as e:
                self.logger.error(f"Error hapus pelanggan: {e}")
                print(f"❌ Error: {e}")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    # ========== MENU 2: KELOLA MEJA ==========
    
    def kelola_meja(self):
        """Menu kelola meja"""
        while True:
            self.clear_screen()
            print("\n" + "=" * 60)
            print("KELOLA MEJA RESTORAN")
            print("=" * 60)
            print("1.  Daftar Semua Meja")
            print("2.  Lihat Meja Tersedia")
            print("3.  Update Status Meja")
            print("0.  Kembali ke Menu Utama")
            print("=" * 60)
            
            choice = input("\nPilih aksi: ").strip()
            
            if choice == "1":
                self.daftar_meja()
            elif choice == "2":
                self.meja_tersedia()
            elif choice == "3":
                self.update_status_meja()
            elif choice == "0":
                break
            else:
                print("Pilihan tidak valid!")
    
    def daftar_meja(self):
        """Tampilkan semua meja"""
        print("\n" + "-" * 60)
        print("DAFTAR MEJA RESTORAN")
        print("-" * 60)
        
        try:
            # Query untuk semua meja
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM meja ORDER BY nomor_meja")
            meja_list = cursor.fetchall()
            
            if not meja_list:
                print("Belum ada data meja.")
            else:
                print(f"{'ID':<5} {'No Meja':<10} {'Kapasitas':<10} {'Status':<15} {'Lokasi':<15}")
                print("-" * 60)
                
                for m in meja_list:
                    # Color coding untuk status
                    status = m['status']
                    if status == 'tersedia':
                        status_display = f"✅ {status}"
                    elif status == 'dipesan':
                        status_display = f"⚠️  {status}"
                    else:
                        status_display = f"❌ {status}"
                    
                    print(f"{m['id']:<5} {m['nomor_meja']:<10} {m['kapasitas']:<10} {status_display:<15} {m.get('lokasi', '-'):<15}")
                
                # Statistik
                total = len(meja_list)
                tersedia = len([m for m in meja_list if m['status'] == 'tersedia'])
                terisi = len([m for m in meja_list if m['status'] == 'terisi'])
                
                print(f"\n📊 STATISTIK:")
                print(f"   Total Meja    : {total}")
                print(f"   Tersedia      : {tersedia}")
                print(f"   Terisi/Dipesan: {terisi}")
        
        except Exception as e:
            self.logger.error(f"Error membaca meja: {e}")
            print(f"❌ Error: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
        
        input("\nTekan Enter untuk melanjutkan...")
    
    def meja_tersedia(self):
        """Tampilkan meja yang tersedia"""
        print("\n" + "-" * 60)
        print("MEJA TERSEDIA")
        print("-" * 60)
        
        try:
            kapasitas = input("Kapasitas minimal (kosongkan untuk semua): ").strip()
            kapasitas_min = int(kapasitas) if kapasitas.isdigit() else 0
            
            meja_tersedia = self.crud.get_meja_tersedia(kapasitas_min)
            
            if not meja_tersedia:
                if kapasitas_min > 0:
                    print(f"Tidak ada meja tersedia dengan kapasitas minimal {kapasitas_min}")
                else:
                    print("Tidak ada meja tersedia saat ini")
            else:
                print(f"\nDitemukan {len(meja_tersedia)} meja tersedia:")
                print(f"{'ID':<5} {'No Meja':<10} {'Kapasitas':<10} {'Lokasi':<15}")
                print("-" * 45)
                
                for m in meja_tersedia:
                    print(f"{m['id']:<5} {m['nomor_meja']:<10} {m['kapasitas']:<10} {m.get('lokasi', '-'):<15}")
        
        except Exception as e:
            self.logger.error(f"Error membaca meja tersedia: {e}")
            print(f"❌ Error: {e}")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    def update_status_meja(self):
        """Update status meja"""
        print("\n" + "-" * 60)
        print("UPDATE STATUS MEJA")
        print("-" * 60)
        
        try:
            meja_id = input("ID Meja: ").strip()
            
            if not meja_id.isdigit():
                print("❌ ID harus berupa angka")
            else:
                # Tampilkan status saat ini
                conn = self.db.get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM meja WHERE id = %s", (int(meja_id),))
                meja = cursor.fetchone()
                
                if not meja:
                    print(f"❌ Meja dengan ID {meja_id} tidak ditemukan")
                else:
                    print(f"\nMeja: {meja['nomor_meja']}")
                    print(f"Status saat ini: {meja['status']}")
                    print("\nPilihan status:")
                    print("1. tersedia")
                    print("2. dipesan")
                    print("3. terisi")
                    
                    pilihan = input("\nPilih status baru [1-3]: ").strip()
                    
                    status_map = {'1': 'tersedia', '2': 'dipesan', '3': 'terisi'}
                    
                    if pilihan in status_map:
                        status_baru = status_map[pilihan]
                        
                        success = self.crud.update_status_meja(int(meja_id), status_baru)
                        
                        if success:
                            print(f"\n✅ Status meja {meja['nomor_meja']} diubah menjadi: {status_baru}")
                            self.logger.info(f"Status meja {meja_id} diubah: {status_baru}")
                        else:
                            print("❌ Gagal mengupdate status")
                    else:
                        print("❌ Pilihan tidak valid")
        
        except Exception as e:
            self.logger.error(f"Error update status meja: {e}")
            print(f"❌ Error: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
        
        input("\nTekan Enter untuk melanjutkan...")
    
    # ========== MENU 3: BUAT PESANAN BARU ==========
    
    def buat_pesanan(self):
        """Buat pesanan baru"""
        print("\n" + "=" * 60)
        print("BUAT PESANAN BARU")
        print("=" * 60)
        
        try:
            # 1. Pilih atau buat pelanggan
            print("\n1. DATA PELANGGAN")
            print("-" * 40)
            
            pelanggan_id = None
            
            # Opsi: pelanggan baru atau existing
            print("\nPilih opsi:")
            print("1. Pelanggan baru")
            print("2. Pelanggan existing")
            
            opsi_pelanggan = input("\nPilih [1-2]: ").strip()
            
            if opsi_pelanggan == "1":
                # Buat pelanggan baru
                print("\nData Pelanggan Baru:")
                nama = input("Nama: ").strip()
                telepon = input("Telepon: ").strip()
                email = input("Email (opsional): ").strip() or None
                
                pelanggan_id = self.crud.create_pelanggan(nama, telepon, email)
                print(f"✅ Pelanggan baru dibuat (ID: {pelanggan_id})")
                
            elif opsi_pelanggan == "2":
                # Pilih dari pelanggan existing
                print("\nPilih pelanggan:")
                pelanggan_list = self.crud.read_pelanggan()
                
                if pelanggan_list:
                    for p in pelanggan_list[:10]:  # Tampilkan 10 pertama
                        print(f"{p['id']}. {p['nama']} - {p['no_telepon']}")
                    
                    pilihan = input("\nID Pelanggan: ").strip()
                    if pilihan.isdigit():
                        pelanggan_id = int(pilihan)
                    else:
                        print("❌ ID tidak valid")
                        return
                else:
                    print("❌ Tidak ada pelanggan terdaftar")
                    return
            else:
                print("❌ Pilihan tidak valid")
                return
            
            if not pelanggan_id:
                print("❌ Gagal mendapatkan pelanggan")
                return
            
            # 2. Pilih meja
            print("\n" + "-" * 40)
            print("2. PILIH MEJA")
            print("-" * 40)
            
            # Tampilkan meja tersedia
            meja_tersedia = self.crud.get_meja_tersedia()
            
            if not meja_tersedia:
                print("❌ Tidak ada meja tersedia saat ini")
                return
            
            print("\nMeja tersedia:")
            for m in meja_tersedia:
                print(f"{m['id']}. Meja {m['nomor_meja']} (Kapasitas: {m['kapasitas']})")
            
            meja_id = input("\nID Meja: ").strip()
            
            if not meja_id.isdigit() or int(meja_id) not in [m['id'] for m in meja_tersedia]:
                print("❌ Meja tidak valid atau tidak tersedia")
                return
            
            meja_id = int(meja_id)
            
            # 3. Pilih menu
            print("\n" + "-" * 40)
            print("3. PILIH MENU")
            print("-" * 40)
            
            items = []
            
            while True:
                # Tampilkan menu
                conn = self.db.get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT m.*, km.nama_kategori 
                    FROM menu m 
                    LEFT JOIN kategori_menu km ON m.kategori_id = km.id
                    WHERE m.stok > 0
                    ORDER BY km.nama_kategori, m.nama_menu
                """)
                menu_list = cursor.fetchall()
                
                if not menu_list:
                    print("❌ Tidak ada menu tersedia")
                    break
                
                print("\nDaftar Menu Tersedia:")
                print(f"{'ID':<5} {'Menu':<25} {'Kategori':<15} {'Harga':<10} {'Stok':<5}")
                print("-" * 70)
                
                for menu in menu_list:
                    print(f"{menu['id']:<5} {menu['nama_menu']:<25} {menu['nama_kategori']:<15} "
                          f"Rp{menu['harga']:<8,.0f} {menu['stok']:<5}")
                
                # Pilih menu
                print("\nPilih menu (0 untuk selesai):")
                menu_pilihan = input("ID Menu: ").strip()
                
                if menu_pilihan == "0":
                    if not items:
                        print("⚠️  Belum ada item dalam pesanan")
                        continue
                    else:
                        break
                
                if not menu_pilihan.isdigit():
                    print("❌ ID harus angka")
                    continue
                
                menu_id = int(menu_pilihan)
                
                # Cek apakah menu valid
                selected_menu = next((m for m in menu_list if m['id'] == menu_id), None)
                
                if not selected_menu:
                    print("❌ Menu tidak ditemukan")
                    continue
                
                # Input jumlah
                jumlah = input(f"Jumlah {selected_menu['nama_menu']} (stok: {selected_menu['stok']}): ").strip()
                
                if not jumlah.isdigit() or int(jumlah) <= 0:
                    print("❌ Jumlah harus angka positif")
                    continue
                
                jumlah = int(jumlah)
                
                if jumlah > selected_menu['stok']:
                    print(f"❌ Stok tidak cukup. Stok tersedia: {selected_menu['stok']}")
                    continue
                
                # Tambah ke items
                items.append((menu_id, jumlah))
                print(f"✅ {selected_menu['nama_menu']} x{jumlah} ditambahkan")
                
                # Tampilkan total sementara
                total_sementara = sum(
                    jumlah * next(m['harga'] for m in menu_list if m['id'] == mid)
                    for mid, jumlah in items
                )
                print(f"Total sementara: Rp{total_sementara:,.0f}")
            
            if not items:
                print("❌ Pesanan dibatalkan - tidak ada item")
                return
            
            # 4. Catatan pesanan
            print("\n" + "-" * 40)
            print("4. CATATAN PESANAN")
            print("-" * 40)
            
            catatan = input("Catatan khusus (kosongkan jika tidak ada): ").strip() or ""
            
            # 5. Konfirmasi
            print("\n" + "=" * 40)
            print("KONFIRMASI PESANAN")
            print("=" * 40)
            
            # Hitung total akhir
            total_akhir = sum(
                jumlah * next(m['harga'] for m in menu_list if m['id'] == mid)
                for mid, jumlah in items
            )
            
            print(f"Pelanggan ID : {pelanggan_id}")
            print(f"Meja ID      : {meja_id}")
            print(f"Jumlah Item  : {len(items)}")
            print(f"Total Harga  : Rp{total_akhir:,.0f}")
            print(f"Catatan      : {catatan or '-'}")
            
            konfirmasi = input("\nKonfirmasi pesanan? (y/n): ").strip().lower()
            
            if konfirmasi == 'y':
                # Simpan pesanan
                result = self.crud.create_pesanan(
                    pelanggan_id=pelanggan_id,
                    meja_id=meja_id,
                    items=items,
                    catatan=catatan
                )
                
                if result:
                    print(f"\n🎉 PESANAN BERHASIL DIBUAT!")
                    print(f"Kode Pesanan : {result['kode_pesanan']}")
                    print(f"Pesanan ID   : {result['pesanan_id']}")
                    print(f"Total        : Rp{result['total_harga']:,.0f}")
                    
                    # Log activity
                    self.logger.info(f"Pesanan baru dibuat: {result['kode_pesanan']} (ID: {result['pesanan_id']})")
                else:
                    print("❌ Gagal membuat pesanan")
            else:
                print("❌ Pesanan dibatalkan")
        
        except Exception as e:
            self.logger.error(f"Error buat pesanan: {e}")
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
        
        input("\nTekan Enter untuk melanjutkan...")
        
    
    # ========== MENU 5: LAPORAN ==========
    
    def generate_laporan(self):
        """Generate laporan sederhana - tampilkan semua pesanan"""
        print("\n" + "=" * 60)
        print("LAPORAN")
        print("=" * 60)
        
        try:
            print("\n📊 MEMUAT DATA PESANAN...")
            
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Query sederhana: semua pesanan
            query = """
            SELECT 
                p.kode_pesanan,
                p.tanggal_pesanan,
                pl.nama as pelanggan,
                m.nomor_meja,
                p.total_harga,
                p.status_pesanan
            FROM pesanan p
            LEFT JOIN pelanggan pl ON p.pelanggan_id = pl.id
            LEFT JOIN meja m ON p.meja_id = m.id
            ORDER BY p.tanggal_pesanan DESC
            LIMIT 50
            """
            
            cursor.execute(query)
            semua_pesanan = cursor.fetchall()
            
            # Statistik total
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_pesanan,
                    SUM(total_harga) as total_pendapatan,
                    MIN(tanggal_pesanan) as pertama,
                    MAX(tanggal_pesanan) as terakhir
                FROM pesanan
            """)
            statistik = cursor.fetchone()
            
            # TAMPILKAN HASIL
            print("\n" + "=" * 60)
            print("📈 STATISTIK KESELURUHAN")
            print("=" * 60)
            
            if statistik:
                print(f"Total Pesanan     : {statistik['total_pesanan'] or 0}")
                print(f"Total Pendapatan  : Rp{statistik['total_pendapatan'] or 0:,.0f}")
                
                if statistik['pertama'] and statistik['terakhir']:
                    print(f"Rentang Waktu     : {statistik['pertama'].strftime('%d/%m/%Y')} - {statistik['terakhir'].strftime('%d/%m/%Y')}")
            
            print("\n" + "=" * 60)
            print("📋 DAFTAR PESANAN TERBARU")
            print("=" * 60)
            
            if not semua_pesanan:
                print("📭 Tidak ada data pesanan")
            else:
                print(f"{'No':<3} {'Kode':<12} {'Tanggal':<12} {'Pelanggan':<20} {'Meja':<6} {'Total':<12} {'Status':<10}")
                print("-" * 80)
                
                for i, pesanan in enumerate(semua_pesanan, 1):
                    tanggal = pesanan['tanggal_pesanan'].strftime('%d/%m/%Y') if pesanan['tanggal_pesanan'] else '-'
                    pelanggan = pesanan['pelanggan'] or 'Tanpa Nama'
                    
                    print(f"{i:<3} "
                        f"{pesanan['kode_pesanan']:<12} "
                        f"{tanggal:<12} "
                        f"{pelanggan[:18]:<20} "
                        f"{pesanan['nomor_meja'] or '-':<6} "
                        f"Rp{pesanan['total_harga'] or 0:<10,.0f} "
                        f"{pesanan['status_pesanan']:<10}")
                
                print(f"\n📄 Menampilkan {len(semua_pesanan)} pesanan terbaru")
            
            # DETAIL 1 PESANAN PILIHAN
            if semua_pesanan:
                print("\n" + "-" * 60)
                print("🔍 LIHAT DETAIL PESANAN")
                print("-" * 60)
                
                pilihan = input("Masukkan nomor pesanan untuk detail (0 untuk skip): ").strip()
                
                if pilihan.isdigit() and 1 <= int(pilihan) <= len(semua_pesanan):
                    idx = int(pilihan) - 1
                    pesanan_terpilih = semua_pesanan[idx]
                    
                    # Ambil detail item pesanan
                    query_detail = """
                    SELECT 
                        mn.nama_menu,
                        dp.jumlah,
                        dp.harga_satuan,
                        (dp.jumlah * dp.harga_satuan) as subtotal
                    FROM detail_pesanan dp
                    LEFT JOIN menu mn ON dp.menu_id = mn.id
                    WHERE dp.pesanan_id = (
                        SELECT id FROM pesanan WHERE kode_pesanan = %s
                    )
                    """
                    
                    cursor.execute(query_detail, (pesanan_terpilih['kode_pesanan'],))
                    detail_items = cursor.fetchall()
                    
                    # Tampilkan detail
                    print("\n" + "=" * 60)
                    print(f"DETAIL PESANAN: {pesanan_terpilih['kode_pesanan']}")
                    print("=" * 60)
                    
                    print(f"Kode Pesanan   : {pesanan_terpilih['kode_pesanan']}")
                    print(f"Tanggal        : {pesanan_terpilih['tanggal_pesanan']}")
                    print(f"Pelanggan      : {pesanan_terpilih['pelanggan']}")
                    print(f"Meja           : {pesanan_terpilih['nomor_meja']}")
                    print(f"Status         : {pesanan_terpilih['status_pesanan']}")
                    print(f"Total          : Rp{pesanan_terpilih['total_harga']:,.0f}")
                    
                    print("\n" + "-" * 60)
                    print("ITEM PESANAN:")
                    print("-" * 60)
                    
                    if detail_items:
                        total_items = 0
                        for item in detail_items:
                            subtotal = item['jumlah'] * item['harga_satuan']
                            total_items += subtotal
                            print(f"  {item['nama_menu']:30} x{item['jumlah']:<3} @Rp{item['harga_satuan']:,.0f} = Rp{subtotal:,.0f}")
                        
                        print("-" * 60)
                        print(f"  TOTAL: Rp{total_items:,.0f}")
                    else:
                        print("  Tidak ada item ditemukan")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nTekan Enter untuk kembali ke menu...")
        
    # ========== MENU 6: DEBUGGING DEMO ==========
    
    def run_debugging_demo(self):
        """Jalankan debugging demonstration"""
        print("\n" + "=" * 60)
        print("DEBUGGING DEMONSTRATION")
        print("=" * 60)
        
        print("\nDemo debugging skills:")
        print("1. Error handling dengan try-except")
        print("2. Logging untuk tracking error")
        print("3. Validasi input user")
        print("4. Exception handling database")
        
        # Contoh debugging scenarios
        print("\n" + "-" * 40)
        print("SCENARIO 1: Division by zero error")
        print("-" * 40)
        
        try:
            numbers = [10, 5, 0, 2]
            for num in numbers:
                result = 100 / num  # Akan error saat num = 0
                print(f"100 / {num} = {result}")
        except ZeroDivisionError as e:
            print(f"❌ ERROR: {e}")
            print("✅ FIXED: Menangani division by zero dengan exception handling")
        
        print("\n" + "-" * 40)
        print("SCENARIO 2: Index out of range")
        print("-" * 40)
        
        try:
            data = [1, 2, 3]
            for i in range(5):
                print(f"data[{i}] = {data[i]}")  # Akan error saat i >= 3
        except IndexError as e:
            print(f"❌ ERROR: {e}")
            print("✅ FIXED: Menangani index error dengan bounds checking")
        
        print("\n" + "-" * 40)
        print("SCENARIO 3: Database error handling")
        print("-" * 40)
        
        try:
            # Simulasi database error
            raise ConnectionError("Database connection timeout")
        except ConnectionError as e:
            print(f"❌ DATABASE ERROR: {e}")
            print("✅ FIXED: Implement retry logic dan fallback")
            self.logger.error(f"Database connection error simulated: {e}")
        
        print("\n" + "-" * 40)
        print("SCENARIO 4: Input validation")
        print("-" * 40)
        
        test_input = "abc"
        if test_input.isdigit():
            print(f"Input '{test_input}' valid: angka")
        else:
            print(f"❌ INPUT ERROR: '{test_input}' bukan angka")
            print("✅ FIXED: Validasi input sebelum processing")
        
        print("\n" + "=" * 60)
        print("DEBUGGING DEMO COMPLETE")
        print("=" * 60)
        
        input("\nTekan Enter untuk melanjutkan...")
    
    # ========== MENU 7: DOKUMENTASI SISTEM ==========
    
    def tampilkan_dokumentasi(self):
        """Tampilkan dokumentasi sistem"""
        print("\n" + "=" * 60)
        print("DOKUMENTASI SISTEM")
        print("=" * 60)
        
        print("\n📋 INFORMASI SISTEM:")
        print(f"   Nama Sistem    : Sistem Pemesanan Restoran")
        print(f"   Versi         : 1.0.0")
        print(f"   Developer     : Peserta Sertifikasi UNILA")
        print(f"   Bahasa        : Python 3.8+")
        print(f"   Database      : MySQL")
        
        print("\n🏗️  ARSITEKTUR SISTEM:")
        print("   restoran_system/")
        print("   ├── app.py                    # Main application")
        print("   ├── models/                   # OOP Classes")
        print("   │   ├── pelanggan.py         # Class Pelanggan")
        print("   │   ├── meja.py              # Class Meja")
        print("   │   ├── pesanan.py           # Class Pesanan")
        print("   │   └── laporan.py           # Class Laporan")
        print("   ├── database/                 # Database operations")
        print("   │   ├── db_connection.py     # Connection pooling")
        print("   │   └── crud_operations.py   # CRUD operations")
        print("   ├── utils/                   # Utilities")
        print("   │   ├── validasi_input.py    # Input validation")
        print("   │   ├── pdf_generator.py     # PDF generation")
        print("   │   └── logger.py            # Logging system")
        print("   ├── tests/                   # Unit tests")
        print("   │   ├── test_models.py       # Test OOP models")
        print("   │   ├── test_database.py     # Test database")
        print("   │   └── test_integration.py  # Integration tests")
        print("   └── docs/                    # Dokumentasi")
        
        print("\n🎯 KOMPETENSI YANG DICOVER:")
        print("   1. J.620100.016.01 - Menulis Kode sesuai Guidelines")
        print("   2. J.620100.017.02 - Pemrograman Terstruktur")
        print("   3. J.620100.018.02 - Pemrograman Berorientasi Objek")
        print("   4. J.620100.019.02 - Menggunakan Library/Component")
        print("   5. J.620100.021.02 - Menerapkan Akses Basis Data")
        print("   6. J.620100.023.02 - Membuat Dokumentasi Kode")
        print("   7. J.620100.025.02 - Melakukan Debugging")
        print("   8. J.620100.033.02 - Melaksanakan Pengujian Unit")
        
        print("\n📚 LIBRARY YANG DIGUNAKAN:")
        print("   - mysql-connector-python: Koneksi database")
        print("   - fpdf2: Generate PDF reports")
        print("   - pandas: Data manipulation (untuk laporan)")
        print("   - logging: Built-in Python logging")
        
        print("\n🔧 CARA MENJALANKAN:")
        print("   1. Setup database: mysql -u root -p < database_schema.sql")
        print("   2. Install dependencies: pip install -r requirements.txt")
        print("   3. Run aplikasi: python app.py")
        print("   4. Run tests: python run_tests.py")
        
        print("\n📞 SUPPORT:")
        print("   Untuk masalah teknis, cek file README.md")
        print("   atau lihat log di folder logs/")
        
        input("\nTekan Enter untuk kembali ke menu utama...")

def main():
    """Main function"""
    try:
        app = SistemRestoran()
        app.run()
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nTekan Enter untuk keluar...")

if __name__ == "__main__":
    main()