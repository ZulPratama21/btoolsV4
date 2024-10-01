let locationId = null;
let lineChart = null;
let intervalId = null;
let counter = 0;
const maxPolls = 10;

const config = {
    type: "line",
    data: {
       labels: [],
       datasets: [
          {
             label: "Upload",
             backgroundColor: '#9ad0f5',
             borderColor: '#9ad0f5',
             data: [],
             borderWidth: 1,
             fill: false
          },
          {
             label: "Download",
             backgroundColor: '#ffb1c1',
             borderColor: '#ffb1c1',
             data: [],
             borderWidth: 1,
             fill: false
          }
       ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
       title: {
          display: true,
          text: "Realtime Traffic User"
       },
       tooltips: {
          mode: "index",
          intersect: false,
       },
       hover: {
          mode: "nearest",
          intersect: true
       },
       scales: {
          xAxes: [{
             display: true,
             scaleLabel: {
                display: true,
                labelString: "Waktu"
             }
          }],
          yAxes: [{
             display: true,
             scaleLabel: {
                display: true,
                labelString: "Throughput (MB)"
             },
             ticks: {
                min: 0
             }
          }]
       }
    }
};

$('#locationForm').on('submit', function(event) {
    event.preventDefault();
    locationId = $('#locationId').val();

    if (lineChart) {
        lineChart.destroy();
    }
    
    const context = document.getElementById('trafficChart').getContext('2d');
    lineChart = new Chart(context, config);

    if (intervalId) {
        clearInterval(intervalId);
    }

    counter = 0;
    intervalId = setInterval(() => {
        updateTrafficData();
        counter++;
        if (counter >= maxPolls) {
            clearInterval(intervalId);
        }
    }, 2000);
});

function updateTrafficData() {
    fetch(`/troubleshoot/getDataBhomeFtth/?locationId=${locationId}`)
    .then(response => response.json())
    .then(data => {
        if (data.statusClient === 'Null'){
            clearInterval(intervalId)
            alert('ID Lokasi tidak ditermukan')
        }

        document.getElementById('clientDetail').textContent = data.comment;
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
        document.getElementById('ssid5').textContent = data.ssid['5.8'];
        document.getElementById('ssid2').textContent = data.ssid['2.4'];
        document.getElementById('passWifi5').textContent = data.passWifi['5.8'];
        document.getElementById('passWifi2').textContent = data.passWifi['2.4'];

        let maxUpload = parseFloat(data.maxUpload) || 0;
        let maxDownload = parseFloat(data.maxDownload) || 0;

        let minUploadIdeal = (0.025 * maxUpload).toFixed(2);
        let maxUploadIdeal = (0.80 * maxUpload).toFixed(2);
        let minDownloadIdeal = (0.05 * maxDownload).toFixed(2);
        let maxDownloadIdeal = (0.80 * maxDownload).toFixed(2);

        document.getElementById('minUpload').textContent = minUploadIdeal;
        document.getElementById('maxUpload').textContent = maxUploadIdeal;
        document.getElementById('minDownload').textContent = minDownloadIdeal;
        document.getElementById('maxDownload').textContent = maxDownloadIdeal;

        let statusResult, tUploadResult, tDownloadResult, latencyResult, stateResult, redamanResult;

        // Determine status result
        if (data.statusClient === 'Null'){
            statusResult = '';
        } else if (data.statusClient === 'Subscribe'){
            statusResult = 'OK';
        } else {
            statusResult = 'Bad';
        }

        // Determine upload traffic result
        if (data.tUpload === 'X'){
            tUploadResult = '';
        } else if (data.tUpload < minUploadIdeal) {
            tUploadResult = 'Low Traffic';
        } else if (data.tUpload > maxUploadIdeal) {
            tUploadResult = 'Full Traffic';
        } else {
            tUploadResult = 'OK';
        }

        // Determine download traffic result
        if (data.tDownload === 'X'){
            tUploadResult = '';
        } else if (data.tDownload < minDownloadIdeal) {
            tDownloadResult = 'Low Traffic';
        } else if (data.tDownload > maxDownloadIdeal) {
            tDownloadResult = 'Full Traffic';
        } else {
            tDownloadResult = 'OK';
        }

        // Determine latency result
        if (data.latency === 'X') {
            latencyResult = '';
        } else if(data.latency < 10){
            latencyResult = 'OK';
        } else {
            latencyResult = 'Bad';
        }

        // Determine state result
        if (data.state === undefined) {
            stateResult = '';
        } else if (data.state === 'Working'){
            stateResult = 'OK';
        } else {
            stateResult = 'Bad';
        }

        // Determine redaman result
        //redamanResult = data.redaman > -29 ? 'OK' : 'High dB';
        if (data.redaman === undefined){
            redamanResult = '';
        } else if (data.redaman > -29){
            redamanResult = 'OK';
        } else {
            redamanResult = 'High dB';
        }

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

        // Update the chart data
        if (config.data.labels.length == 20) {
            config.data.labels.shift();
            config.data.datasets[0].data.shift();
            config.data.datasets[1].data.shift();
        }

        const now = new Date();
        const hours = now.getHours();
        const minutes = now.getMinutes();
        const seconds = now.getSeconds();
        
        config.data.labels.push(`${hours}:${minutes}:${seconds}`);
        config.data.datasets[0].data.push(data.tUpload);
        config.data.datasets[1].data.push(data.tDownload);

        lineChart.update();

        const clientLink = document.getElementById('clientLink');
        clientLink.href = `http://${data.clientIp}`;

        const dataConn = data.connectedDevice;
        const tableBody = document.getElementById('deviceTable');
        
        // Kosongkan tabel sebelum menambahkan data baru
        tableBody.innerHTML = '';
        
        // Looping melalui data dan membuat baris tabel
        dataConn.forEach(device => {
            const row = document.createElement('tr');
        
            const hostName = device.hostName ? device.hostName : 'Unknown';
            const ipAddress = device.ipAddress;
            const macAddress = device.macAddress;
        
            row.innerHTML = `
                <td>${hostName}</td>
                <td>${ipAddress}</td>
                <td>${macAddress}</td>
            `;
        
            tableBody.appendChild(row);
        });
        
    });
}