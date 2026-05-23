import hashlib
import hmac

def hitung_naive_mac(key: bytes, message: bytes, algorithm: str) -> str:
    """
    Simulasi MAC sederhana (Naive MAC) dengan menggabungkan Kunci + Pesan.
    Rentan terhadap Length Extension Attack.
    """
    hasher = hashlib.new(algorithm)
    hasher.update(key + message)
    return hasher.hexdigest()

def hitung_hmac(key: bytes, message: bytes, algorithm: str) -> str:
    """
    Simulasi HMAC standar yang aman menggunakan modul hmac bawaan Python.
    Menggunakan mekanisme double-hashing dengan ipad dan opad.
    """
    digestmod = getattr(hashlib, algorithm)
    h = hmac.new(key, message, digestmod=digestmod)
    return h.hexdigest()

if __name__ == "__main__":
    # 1. Inisialisasi Data awal
    kunci_rahasia = b"KunciRahasiaKripto123"
    pesan_asli = b"Transfer dana sebesar Rp 10.000.000 ke rekening Budi."

    print("=" * 70)
    print("      SIMULASI PENGGUNAAN HASH (MD5 & SHA-256) PADA MAC & HMAC")
    print("=" * 70)
    print(f"Pesan Asli : {pesan_asli.decode('utf-8')}")
    print(f"Kunci      : {kunci_rahasia.decode('utf-8')}")
    print("-" * 70)

    # 2. Proses Menggunakan MD5
    print("[ FUNGSI HASH: MD5 ]")
    mac_md5 = hitung_naive_mac(kunci_rahasia, pesan_asli, 'md5')
    hmac_md5 = hitung_hmac(kunci_rahasia, pesan_asli, 'md5')
    print(f"-> Naive MAC (MD5) : {mac_md5}")
    print(f"-> HMAC (MD5)       : {hmac_md5}")
    print("-" * 70)

    # 3. Proses Menggunakan SHA-256
    print("[ FUNGSI HASH: SHA-256 ]")
    mac_sha256 = hitung_naive_mac(kunci_rahasia, pesan_asli, 'sha256')
    hmac_sha256 = hitung_hmac(kunci_rahasia, pesan_asli, 'sha256')
    print(f"-> Naive MAC (SHA)  : {mac_sha256}")
    print(f"-> HMAC (SHA-256)   : {hmac_sha256}")
    print("=" * 70)

    # 4. Simulasi Verifikasi di Sisi Penerima (Kasus Sukses)
    print("\n[ SIMULASI VERIFIKASI HMAC SHA-256 - PESAN AMAN ]")
    pesan_diterima = pesan_asli
    hmac_diterima = hmac_sha256

    # Penerima menghitung ulang HMAC dengan kunci yang sama
    hmac_hitung_ulang = hitung_hmac(kunci_rahasia, pesan_diterima, 'sha256')
    
    print(f"HMAC Diterima     : {hmac_diterima}")
    print(f"HMAC Dihitung     : {hmac_hitung_ulang}")
    if hmac.compare_digest(hmac_diterima, hmac_hitung_ulang):
        print("Hasil Verifikasi  : VALID (Pesan Otentik & Integritas Terjamin)")
    else:
        print("Hasil Verifikasi  : INVALID (Pesan atau Kunci Telah Berubah!)")
    print("=" * 70)

    # 5. Simulasi Verifikasi di Sisi Penerima (Kasus Man-in-the-Middle / Perubahan Data)
    print("\n[ SIMULASI VERIFIKASI HMAC SHA-256 - PESAN DIUBAH PENYERANG ]")
    pesan_palsu = b"Transfer dana sebesar Rp 90.000.000 ke rekening Budi." # Nominal diubah
    
    hmac_hitung_palsu = hitung_hmac(kunci_rahasia, pesan_palsu, 'sha256')
    
    print(f"HMAC Diterima     : {hmac_diterima} (Dari pesan asli)")
    print(f"HMAC Dihitung     : {hmac_hitung_palsu} (Dari pesan palsu)")
    if hmac.compare_digest(hmac_diterima, hmac_hitung_palsu):
        print("Hasil Verifikasi  : VALID")
    else:
        print("Hasil Verifikasi  : INVALID! PERINGATAN: Data telah dimanipulasi!")
    print("=" * 70)