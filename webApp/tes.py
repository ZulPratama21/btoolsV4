import mysql.connector

# Membuat koneksi ke database MySQL
conn = mysql.connector.connect(
    host="localhost",      # Ganti dengan host MySQL-mu (misalnya: '127.0.0.1')
    user="root",           # Ganti dengan username MySQL-mu
    password="password",   # Ganti dengan password MySQL-mu
    database="nama_database"  # Ganti dengan nama database-mu
)

# Membuat cursor untuk menjalankan query
cursor = conn.cursor()

# Query SQL untuk menambahkan data
sql = "INSERT INTO nama_tabel (kolom1, kolom2, kolom3) VALUES (%s, %s, %s)"
values = ("data1", "data2", "data3")

# Eksekusi query
cursor.execute(sql, values)

# Commit perubahan ke database
conn.commit()

print(f"{cursor.rowcount} record berhasil dimasukkan.")

# Menutup koneksi
cursor.close()
conn.close()
