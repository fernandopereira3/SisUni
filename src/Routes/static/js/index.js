// index.js - JavaScript para a página index.html

document.addEventListener('DOMContentLoaded', function () {
    console.log("Verificando tabela de trabalho...");
    const tableElement = document.querySelector('#tabela-trabalho, .table');
    if (tableElement) {
        console.log("Tabela encontrada:", tableElement);
        console.log("Número de linhas na tabela:", tableElement.querySelectorAll('tbody tr').length);
    } else {
        console.log("Tabela não encontrada!");
        console.log("Conteúdo do container:", document.querySelector('.container').innerHTML);
    }

    // Forçar comportamento hover nos dropdowns
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');
        let timeoutId;

        if (toggle && menu) {
            // Remover qualquer evento de click
            toggle.removeAttribute('data-bs-toggle');
            toggle.addEventListener('click', function (e) {
                e.preventDefault();
                return false;
            });

            // Forçar hover com delay
            dropdown.addEventListener('mouseenter', function () {
                clearTimeout(timeoutId);
                menu.classList.add('show');
            });

            dropdown.addEventListener('mouseleave', function () {
                timeoutId = setTimeout(function () {
                    menu.classList.remove('show');
                }, 300); // 300ms de delay
            });

            // Manter aberto quando mouse está sobre o menu
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
