// debug.js
// Funcionalidades da página debug.html

document.addEventListener('DOMContentLoaded', function () {
    // Gerenciar dropdowns customizados
    const dropdownHeaders = document.querySelectorAll('.dropdown-header');

    dropdownHeaders.forEach(header => {
        header.addEventListener('click', function () {
            const dropdownId = this.getAttribute('data-dropdown');
            const content = document.getElementById(dropdownId + '-dropdown');
            const isActive = this.classList.contains('active');

            // Fechar todos os outros dropdowns
            dropdownHeaders.forEach(h => {
                if (h !== this) {
                    h.classList.remove('active');
                    const otherId = h.getAttribute('data-dropdown');
                    const otherContent = document.getElementById(otherId + '-dropdown');
                    if (otherContent) {
                        otherContent.classList.remove('show');
                    }
                }
            });

            // Toggle do dropdown atual
            if (isActive) {
                this.classList.remove('active');
                content.classList.remove('show');
            } else {
                this.classList.add('active');
                content.classList.add('show');
            }
        });
    });

    // Fechar dropdowns ao clicar fora
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.dropdown-container')) {
            dropdownHeaders.forEach(header => {
                header.classList.remove('active');
                const dropdownId = header.getAttribute('data-dropdown');
                const content = document.getElementById(dropdownId + '-dropdown');
                if (content) {
                    content.classList.remove('show');
                }
            });
        }
    });
});
