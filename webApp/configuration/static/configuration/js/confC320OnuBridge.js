function sendData(event) {
    // Mencegah form dari submit secara default
    event.preventDefault();

    // Mengambil data dari input form
    const data = {
        sn: document.getElementById('sn').value,
        ipAddress: document.getElementById('ipAddress').value,
        limitasi: document.getElementById('limitasi').value,
        neCode: document.getElementById('neCode').value,
        subnetMask: document.getElementById('subnetMask').value,
        modemType: document.getElementById('modemType').value
    };

    // Melakukan fetch request dengan method POST
    fetch('/configuration/confC320OnuBridge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Menampilkan hasil di elemen span dengan ID result
        document.getElementById('result').textContent = data.message;
    })
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