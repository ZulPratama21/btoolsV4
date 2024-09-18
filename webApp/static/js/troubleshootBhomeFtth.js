// Function untuk update chart dan tampilkan data
function updateTrafficData() {
fetch('/troubleshoot/getData/')
    .then(response => response.json())
    .then(data => {
        document.getElementById('status').textContent = data.status;
        document.getElementById('maxUpload').textContent = data.maxUpload;
        document.getElementById('maxDownload').textContent = data.maxDownload;
        document.getElementById('tUpload').textContent = data.tUpload;
        document.getElementById('tDownload').textContent = data.tDownload;
        document.getElementById('latency').textContent = data.latency;
    });
}

// Polling tiap 5 detik
setInterval(updateTrafficData, 5000);