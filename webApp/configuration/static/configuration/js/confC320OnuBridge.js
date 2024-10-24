function sendData(event) {
    event.preventDefault();  // Mencegah form dari submit secara default

    // Mengambil data dari input form
    const sn = document.getElementById('sn').value;
    const ipAddress = document.getElementById('ipAddress').value;
    const limitasi = document.getElementById('limitasi').value;
    const neCode = document.getElementById('neCode').value;
    const subnetMask = document.getElementById('subnetMask').value;
    const modemType = document.getElementById('modemType').value;

    // Validasi manual menggunakan JavaScript
    if (!sn || !ipAddress || limitasi === 'Pilih Limitasi' || !neCode || !subnetMask || modemType === 'Pilih Tipe Modem') {
        alert('Semua kolom harus diisi dengan benar!');
        return;  // Hentikan proses jika ada field yang kosong
    }

    // Jika validasi lolos, buat objek data
    const data = {
        sn: sn,
        ipAddress: ipAddress,
        limitasi: limitasi,
        neCode: neCode,
        subnetMask: subnetMask,
        modemType: modemType
    };

    // Melakukan fetch request dengan method POST
    fetch('/configuration/apiConfC320OnuBridge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Menampilkan hasil di elemen pre dengan ID result
        document.getElementById('result').textContent = data.message;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Terjadi kesalahan saat mengirim data');
    });
}


function copyText() {
    // Buat elemen textarea secara dinamis
    const textToCopy = document.getElementById('result').innerText;
    const tempTextArea = document.createElement('textarea');
    tempTextArea.value = textToCopy;
    
    // Tambahkan textarea ke body
    document.body.appendChild(tempTextArea);
    
    // Pilih teks dalam textarea
    tempTextArea.select();
    tempTextArea.setSelectionRange(0, 99999); // Untuk perangkat mobile
    
    // Salin teks ke clipboard
    document.execCommand('copy');
    
    // Hapus textarea setelah teks disalin
    document.body.removeChild(tempTextArea);
    
    // Tampilkan pesan sukses
    alert("Konfigurasi berhasil di salin");
}