document.getElementById('numPacket').addEventListener('change', function () {
    const numPackets = parseInt(this.value); // Ambil nilai jumlah paket
    const neCodeContainer = document.getElementById('neCodeContainer');

    // Hapus semua input NE Code yang ada sebelumnya
    neCodeContainer.innerHTML = '';

    // Generate input NE Code sesuai dengan jumlah paket
    for (let i = 1; i <= numPackets; i++) {
        const neCodeDiv = document.createElement('div');
        neCodeDiv.classList.add('col-md-4');
        neCodeDiv.innerHTML = `
            <div class="mb-3">
                <label for="neCode${i}" class="form-label">NE Code ${i}</label>
                <input type="text" class="form-control" id="neCode${i}" placeholder="Masukkan ID NE ${i}" required>
            </div>
        `;
        neCodeContainer.appendChild(neCodeDiv); // Tambahkan input ke container
    }
});

function sendData(event) {
    event.preventDefault();  // Mencegah form dari submit secara default

    // Mengambil data dari input form
    const vlanGw = document.getElementById('vlanGw').value;
    const modemType = document.getElementById('modemType').value;
    const sn = document.getElementById('sn').value;
    const ipAddress = document.getElementById('ipAddress').value;
    const limitasi = document.getElementById('limitasi').value;

    // Ambil semua input NE Code yang dinamis
    const neCodes = [];
    const numPackets = parseInt(document.getElementById('numPacket').value); // Ambil jumlah paket yang dipilih
    for (let i = 1; i <= numPackets; i++) {
        const neCodeInput = document.getElementById(`neCode${i}`);
        console.log(`Mencari neCode${i}:`, neCodeInput);  // Debugging apakah elemen ditemukan
        if (neCodeInput && neCodeInput.value) {
            neCodes.push(neCodeInput.value);  // Simpan nilai NE Code ke dalam array
        } else {
            alert(`NE Code ${i} tidak ditemukan atau belum diisi!`);
            return;  // Hentikan proses jika ada input NE Code yang kosong atau tidak ditemukan
        }
    }

    // Validasi manual menggunakan JavaScript
    if (!vlanGw || !sn || limitasi === 'Pilih Limitasi' || neCodes.length < numPackets || modemType === 'Pilih Tipe Modem' || !ipAddress) {
        alert('Semua kolom harus diisi dengan benar dan jumlah NE Code harus sesuai!');
        return;  // Hentikan proses jika ada field yang kosong
    }

    // Jika validasi lolos, buat objek data
    const data = {
        vlanGw: vlanGw,
        modemType: modemType,
        sn: sn,
        ipAddress: ipAddress,
        limitasi: limitasi,
        neCodes: neCodes,  // Kirim array NE Code
    };

    // Melakukan fetch request dengan method POST
    fetch('/configuration/apiConfC320OnuManyPacket', {
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