document.getElementById("deviceTableFilter").addEventListener("keyup", function() {
    var input = document.getElementById("deviceTableFilter");
    var filter = input.value.toLowerCase();
    var table = document.getElementById("deviceTable");
    var tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (var i = 1; i < tr.length; i++) {  // Mulai dari 1 untuk melewatkan header
        var tdIdentity = tr[i].getElementsByTagName("td")[1];
        var tdLayer = tr[i].getElementsByTagName("td")[2];
        var tdIP = tr[i].getElementsByTagName("td")[3];
        if (tdIdentity || tdLayer || tdIP) {
            var identityText = tdIdentity.textContent || tdIdentity.innerText;
            var layerText = tdLayer.textContent || tdLayer.innerText;
            var ipText = tdIP.textContent || tdIP.innerText;

            // Cek apakah salah satu kolom mengandung teks pencarian
            if (identityText.toLowerCase().indexOf(filter) > -1 || 
                layerText.toLowerCase().indexOf(filter) > -1 || 
                ipText.toLowerCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
});

// Filter untuk User Table
document.getElementById("userTableFilter").addEventListener("keyup", function() {
    var input = document.getElementById("userTableFilter");
    var filter = input.value.toLowerCase();
    var table = document.getElementById("userTable");
    var tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (var i = 1; i < tr.length; i++) {  // Mulai dari 1 untuk melewatkan header
        var tdUser = tr[i].getElementsByTagName("td")[1];
        var tdGroup = tr[i].getElementsByTagName("td")[2];
        if (tdUser || tdGroup) {
            var userText = tdUser.textContent || tdUser.innerText;
            var groupText = tdGroup.textContent || tdGroup.innerText;

            // Cek apakah salah satu kolom mengandung teks pencarian
            if (userText.toLowerCase().indexOf(filter) > -1 || 
                groupText.toLowerCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
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
  // Check user checkboxes
  var userCheckboxes = document.querySelectorAll('#userTable input[type="checkbox"]:not(#selectAllUsers)');
  var userChecked = Array.prototype.slice.call(userCheckboxes).some(function(checkbox) {
    return checkbox.checked;
  });

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