let locationId = null;

$('#locationForm').on('submit', function(event) {
    event.preventDefault();
    locationId = $('#locationId').val();
});

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
        document.getElementById('clientIp').textContent = data.clientIp;
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

        if (data.statusClient === 'Subscribe'){
            statusResult = 'OK'
            document.getElementById('statusResult')
        } else {
            statusResult = 'Bad'
        }

        if (data.tUpload < minUploadIdeal){
            tUploadResult = 'Low Traffic'
        } else if (data.tUpload > maxUploadIdeal){
            tUploadResult = 'Full Traffic'
        } else if (data.tUpload > minUploadIdeal && data.tUpload < maxUploadIdeal){
            tUploadResult = 'OK'
        } else {
            tUploadResult = 'Bad'
        }

        if (data.tDownload < minDownloadIdeal){
            tDownloadResult = 'Low Traffic'
        } else if (data.tDownload > maxDownloadIdeal){
            tDownloadResult = 'Full Traffic'
        } else if (data.tDownload > minDownloadIdeal && data.tDownload < maxDownloadIdeal){
            tDownloadResult = 'OK'
        } else {
            tDownloadResult = 'Bad'
        }

        if (data.latency < 10){
            latencyResult = 'OK'
        } else {
            latencyResult = 'Bad'
        }

        if (data.state === 'Working'){
            stateResult = 'OK'
        } else {
            stateResult = 'Bad'
        }

        if (data.redaman > -29){
            redamanResult = 'OK'
        } else {
            redamanResult = 'Bad'
        }

        document.getElementById('statusResult').textContent = statusResult;
        document.getElementById('tUploadResult').textContent = tUploadResult;
        document.getElementById('tDownloadResult').textContent = tDownloadResult;
        document.getElementById('latencyResult').textContent = latencyResult;
        document.getElementById('stateResult').textContent = stateResult;
        document.getElementById('redamanResult').textContent = redamanResult;

    });
}

setInterval(updateTrafficData, 2000);