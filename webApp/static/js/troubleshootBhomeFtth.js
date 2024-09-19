let locationId = null;

// Mengambil inputan location ID dari user
$('#locationForm').on('submit', function(event) {
    event.preventDefault();
    locationId = $('#locationId').val();
});

// Function untuk menampilkan data
function updateTrafficData() {
    fetch(`/troubleshoot/getData/?locationId=${locationId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('status').textContent = data.statusClient;
            document.getElementById('maxUpload').textContent = data.maxUpload;
            document.getElementById('maxDownload').textContent = data.maxDownload;
            document.getElementById('tUpload').textContent = data.tUpload;
            document.getElementById('tDownload').textContent = data.tDownload;
            document.getElementById('latency').textContent = data.latency;
            document.getElementById('state').textContent = data.state;
            document.getElementById('redaman').textContent = data.redaman;
            document.getElementById('authpass').textContent = data.authpass;
            document.getElementById('offline').textContent = data.offline;
            document.getElementById('type').textContent = data.type;
            document.getElementById('name').textContent = data.name;
            document.getElementById('serialNumber').textContent = data.serialNumber;
        });
}
// update setiap 5 detik
setInterval(updateTrafficData, 2500);
