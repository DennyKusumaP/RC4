def inisialisasi_array(kunci_bytes):
    larik = list(range(256))
    penanda = 0
    for indeks in range(256):
        penanda = (penanda + larik[indeks] + kunci_bytes[indeks % len(kunci_bytes)]) & 0xFF
        larik[indeks], larik[penanda] = larik[penanda], larik[indeks]
    return larik

def buat_keystream(larik):
    a = b = 0
    while True:
        a = (a + 1) & 0xFF
        b = (b + larik[a]) & 0xFF
        larik[a], larik[b] = larik[b], larik[a]
        yield larik[(larik[a] + larik[b]) & 0xFF]

def proses_rc4(kunci: bytes, teks: bytes) -> bytes:
    aliran = buat_keystream(inisialisasi_array(kunci))
    return bytes([t ^ next(aliran) for t in teks])

def minta_kunci():
    while True:
        kunci = input("  Masukkan kunci rahasia : ")
        if kunci:
            return kunci
        print("  [!] Kunci tidak boleh kosong!\n")

def jalankan_enkripsi():
    print("\n==========================")
    print("        ENKRIPSI         ")
    print("==========================")
    kunci = minta_kunci()
    while True:
        pesan = input("  Masukkan pesan         : ")
        if pesan:
            break
        print("  [!] Pesan tidak boleh kosong!\n")

    hasil = proses_rc4(kunci.encode(), pesan.encode())
    print("\n  >> Hasil Enkripsi")
    print(f"  Kunci      : {kunci}")
    print(f"  Pesan Asli : {pesan}")
    print(f"  Tersandi   : {hasil.hex()}\n")

def jalankan_dekripsi():
    print("\n==========================")
    print("        DEKRIPSI         ")
    print("==========================")
    kunci = minta_kunci()
    while True:
        tersandi = input("  Masukkan teks tersandi  : ")
        if not tersandi:
            print("  [!] Teks tersandi tidak boleh kosong!\n")
            continue
        try:
            bytes.fromhex(tersandi)
            break
        except ValueError:
            print("  [!] Format tidak valid!\n")

    hasil = proses_rc4(kunci.encode(), bytes.fromhex(tersandi))
    print("\n  >> Hasil Dekripsi")
    print(f"  Kunci      : {kunci}")
    print(f"  Tersandi   : {tersandi}")
    print(f"  Pesan Asli : {hasil.decode('utf-8', errors='replace')}\n")

def tampilkan_menu():
    print("\n==========================")
    print("   PROGRAM SANDI RC4     ")
    print("==========================")
    print("  E  →  Enkripsi    ")
    print("  D  →  Dekripsi    ")
    print("  K  →  Keluar           ")
    print("==========================")

def main():
    pilihan_menu = {"E": jalankan_enkripsi, "D": jalankan_dekripsi}
    print("\n  Selamat datang di Program Sandi RC4!")
    while True:
        tampilkan_menu()
        pilihan = input("  Pilih [E/D/K] : ").strip().upper()
        if pilihan == "K":
            print("\n  Program selesai. Sampai jumpa!\n")
            break
        elif pilihan in pilihan_menu:
            pilihan_menu[pilihan]()
        else:
            print("  [!] Pilihan tidak valid!\n")

if __name__ == "__main__":
    main()