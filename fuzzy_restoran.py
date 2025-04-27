import pandas as pd

# Fungsi keanggotaan segitiga
def segitiga(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif x == b:
        return 1
    elif x < b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)

# Fuzzifikasi untuk servis
def fuzzifikasi_servis(servis):
    return {
        'buruk': segitiga(servis, 0, 0, 50),
        'sedang': segitiga(servis, 30, 50, 70),
        'baik': segitiga(servis, 60, 100, 100)
    }

# Fuzzifikasi untuk harga
def fuzzifikasi_harga(harga):
    return {
        'murah': segitiga(harga, 25000, 25000, 35000),
        'sedang': segitiga(harga, 30000, 40000, 50000),
        'mahal': segitiga(harga, 45000, 55000, 55000)
    }

# Aturan fuzzy
def inferensi(fz_servis, fz_harga):
    rules = []
    rules.append((min(fz_servis['buruk'], fz_harga['mahal']), 20))
    rules.append((min(fz_servis['buruk'], fz_harga['sedang']), 30))
    rules.append((min(fz_servis['buruk'], fz_harga['murah']), 40))
    rules.append((min(fz_servis['sedang'], fz_harga['mahal']), 40))
    rules.append((min(fz_servis['sedang'], fz_harga['sedang']), 60))
    rules.append((min(fz_servis['sedang'], fz_harga['murah']), 70))
    rules.append((min(fz_servis['baik'], fz_harga['mahal']), 60))
    rules.append((min(fz_servis['baik'], fz_harga['sedang']), 80))
    rules.append((min(fz_servis['baik'], fz_harga['murah']), 90))
    return rules

# Defuzzifikasi
def defuzzifikasi(rules):
    numerator = sum(mu * z for mu, z in rules)
    denominator = sum(mu for mu, _ in rules)
    return numerator / denominator if denominator != 0 else 0

# Menentukan kualitas pelayanan dari nilai servis
def kualitas_pelayanan(servis):
    if servis >= 60:
        return "Baik"
    elif servis >= 30:
        return "Sedang"
    else:
        return "Buruk"

# Fungsi utama fuzzy system
def sistem_fuzzy(data):
    hasil = []
    for i, row in data.iterrows():
        servis = row['Pelayanan']
        harga = row['harga']
        fz_servis = fuzzifikasi_servis(servis)
        fz_harga = fuzzifikasi_harga(harga)
        rules = inferensi(fz_servis, fz_harga)
        skor = defuzzifikasi(rules)
        hasil.append({
            'ID_Restoran': row['id Pelanggan'],
            'Skor': round(skor, 2),
            'Kualitas Pelayanan': kualitas_pelayanan(servis),
            'Harga': harga
        })
    return pd.DataFrame(hasil)

if __name__ == "__main__":
    df = pd.read_excel('restoran.xlsx')

    print("Kolom yang terbaca:")
    print(df.columns)

    hasil = sistem_fuzzy(df)
    hasil_terbaik = hasil.sort_values(by='Skor', ascending=False).head(5)

    # Print ke terminal seperti format contoh
    print("\n5 Restoran Terbaik di Kota Bandung:")
    print(f"{'ID':<10}{'Skor':<10}{'Pelayanan':<10}{'Harga'}")
    for idx, row in hasil_terbaik.iterrows():
        print(f"{row['ID_Restoran']:<10}{row['Skor']:<10}{row['Kualitas Pelayanan']:<10}{row['Harga']}")

    # Simpan ke file
    hasil_terbaik.to_excel('peringkat.xlsx', index=False)
    print("\nFile 'peringkat.xlsx' berhasil dibuat dengan Top-5 restoran.")
