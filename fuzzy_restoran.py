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