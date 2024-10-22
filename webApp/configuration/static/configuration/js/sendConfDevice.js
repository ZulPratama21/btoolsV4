document.getElementById("deviceTableFilter").addEventListener("keyup", function() {
    var input = document.getElementById("deviceTableFilter");
    var filter = input.value.toLowerCase();
    var table = document.getElementById("deviceTable");
    var tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (var i = 1; i < tr.length; i++) {  // Mulai dari 1 untuk melewatkan header
        var tds = tr[i].getElementsByTagName("td");
        var rowMatch = false;

        // Loop through all cells in the current row
        for (var j = 0; j < tds.length; j++) {
            var td = tds[j];
            if (td) {
                var cellText = td.textContent || td.innerText;
                // Cek apakah ada kolom yang mengandung teks pencarian
                if (cellText.toLowerCase().indexOf(filter) > -1) {
                    rowMatch = true;
                    break; // Jika ada kecocokan, keluar dari loop kolom
                }
            }
        }

        // Tampilkan atau sembunyikan baris berdasarkan hasil pencarian
        if (rowMatch) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
});

function toggleSelectAll(tableId, source) {
    var checkboxes = document.querySelectorAll('#' + tableId + ' input[type="checkbox"]:not(#' + source.id + ')');
    checkboxes.forEach(checkbox => {
      checkbox.checked = source.checked;
    });
  }
  
  function checkSelectAll(tableId, selectAllId) {
    var selectAll = document.getElementById(selectAllId);
    var checkboxes = document.querySelectorAll('#' + tableId + ' input[type="checkbox"]:not(#' + selectAllId + ')');
    selectAll.checked = Array.prototype.slice.call(checkboxes).every(checkbox => checkbox.checked);
  }
  
  function validateForm() {
    // Check device checkboxes
    var deviceCheckboxes = document.querySelectorAll('#deviceTable input[type="checkbox"]:not(#selectAllDevices)');
    var deviceChecked = Array.prototype.slice.call(deviceCheckboxes).some(function(checkbox) {
      return checkbox.checked;
    });
  
    // Validate
    if (userChecked && deviceChecked) {
      return true; // Form submission allowed
    } else {
      alert('Please select at least one user and one device.');
      return false; // Form submission prevented
    }
  }