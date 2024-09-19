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

        let maxUpload = parseFloat(data.maxUpload) || 0;
        let maxDownload = parseFloat(data.maxDownload) || 0;

        let minUploadIdeal = (0.05 * maxUpload).toFixed(2);
        let maxUploadIdeal = (0.80 * maxUpload).toFixed(2);
        let minDownloadIdeal = (0.10 * maxDownload).toFixed(2);
        let maxDownloadIdeal = (0.80 * maxDownload).toFixed(2);

        document.getElementById('minUpload').textContent = minUploadIdeal;
        document.getElementById('maxUpload').textContent = maxUploadIdeal;
        document.getElementById('minDownload').textContent = minDownloadIdeal;
        document.getElementById('maxDownload').textContent = maxDownloadIdeal;

    });
}

setInterval(updateTrafficData, 5000);
