/*!
* Start Bootstrap - Simple Sidebar v6.0.6 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
// 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

document.getElementById('sidebarToggle').addEventListener('click', function() {
    const icon = document.getElementById('toggleIcon');

    // Cek apakah ikon saat ini adalah "bi-toggle-on", lalu ganti menjadi "bi-toggle-off"
    if (icon.classList.contains('bi-backspace-fill')) {
        icon.classList.remove('bi-backspace-fill');
        icon.classList.add('bi-arrow-right-circle-fill');
    } else {
        // Jika ikon adalah "bi-toggle-off", kembalikan ke "bi-toggle-on"
        icon.classList.remove('bi-arrow-right-circle-fill');
        icon.classList.add('bi-backspace-fill');
    }
});
