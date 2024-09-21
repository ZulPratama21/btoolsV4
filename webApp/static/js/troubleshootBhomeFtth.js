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

        let statusResult, tUploadResult, tDownloadResult, latencyResult, stateResult, redamanResult;

        // Determine status result
        statusResult = data.statusClient === 'Subscribe' ? 'OK' : 'Bad';

        // Determine upload traffic result
        if (data.tUpload < minUploadIdeal) {
            tUploadResult = 'Low Traffic';
        } else if (data.tUpload > maxUploadIdeal) {
            tUploadResult = 'Full Traffic';
        } else {
            tUploadResult = 'OK';
        }

        // Determine download traffic result
        if (data.tDownload < minDownloadIdeal) {
            tDownloadResult = 'Low Traffic';
        } else if (data.tDownload > maxDownloadIdeal) {
            tDownloadResult = 'Full Traffic';
        } else {
            tDownloadResult = 'OK';
        }

        // Determine latency result
        latencyResult = data.latency < 10 ? 'OK' : 'Bad';

        // Determine state result
        stateResult = data.state === 'Working' ? 'OK' : 'Bad';

        // Determine redaman result
        redamanResult = data.redaman > -29 ? 'OK' : 'Bad';

        // Update text content for results
        document.getElementById('statusResult').textContent = statusResult;
        document.getElementById('tUploadResult').textContent = tUploadResult;
        document.getElementById('tDownloadResult').textContent = tDownloadResult;
        document.getElementById('latencyResult').textContent = latencyResult;
        document.getElementById('stateResult').textContent = stateResult;
        document.getElementById('redamanResult').textContent = redamanResult;

        // Helper function to update badge color
        function updateBadgeColor(elementId, result) {
            const element = document.getElementById(elementId);
            element.classList.remove('bg-success', 'bg-danger', 'bg-warning');
            if (result === 'OK') {
                element.classList.add('bg-success');
            } else if (result === 'Low Traffic') {
                element.classList.add('bg-warning');
            } else {
                element.classList.add('bg-danger');
            }
        }

        // Update badge colors
        updateBadgeColor('statusResult', statusResult);
        updateBadgeColor('tUploadResult', tUploadResult);
        updateBadgeColor('tDownloadResult', tDownloadResult);
        updateBadgeColor('latencyResult', latencyResult);
        updateBadgeColor('stateResult', stateResult);
        updateBadgeColor('redamanResult', redamanResult);
    });
}

// Call updateTrafficData every 2 seconds
setInterval(updateTrafficData, 2000);
