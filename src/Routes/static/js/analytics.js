// analytics.js
// Funcionalidades da página analytics.html

// Dropdown hover functionality
document.addEventListener('DOMContentLoaded', function () {
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');
        let timeoutId;

        if (toggle && menu) {
            toggle.removeAttribute('data-bs-toggle');
            toggle.addEventListener('click', function (e) {
                e.preventDefault();
                return false;
            });

            dropdown.addEventListener('mouseenter', function () {
                clearTimeout(timeoutId);
                menu.classList.add('show');
            });

            dropdown.addEventListener('mouseleave', function () {
                timeoutId = setTimeout(function () {
                    menu.classList.remove('show');
                }, 300);
            });

            menu.addEventListener('mouseenter', function () {
                clearTimeout(timeoutId);
            });

            menu.addEventListener('mouseleave', function () {
                timeoutId = setTimeout(function () {
                    menu.classList.remove('show');
                }, 300);
            });
        }
    });
});
