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

    // Forçar comportamento hover nos dropdowns principais
    const dropdowns = document.querySelectorAll('.navbar .dropdown');
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
                    // Fechar todos os submenus quando o menu principal fechar
                    const submenus = menu.querySelectorAll('.dropdown-submenu .dropdown-menu');
                    submenus.forEach(submenu => submenu.classList.remove('show'));
                }, 300); // 300ms de delay
            });

            // Manter aberto quando mouse está sobre o menu
            menu.addEventListener('mouseenter', function () {
                clearTimeout(timeoutId);
            });

            menu.addEventListener('mouseleave', function () {
                timeoutId = setTimeout(function () {
                    menu.classList.remove('show');
                    // Fechar todos os submenus quando sair do menu
                    const submenus = menu.querySelectorAll('.dropdown-submenu .dropdown-menu');
                    submenus.forEach(submenu => submenu.classList.remove('show'));
                }, 300);
            });
        }
    });

    // Controlar submenus (dropdowns aninhados)
    const submenus = document.querySelectorAll('.dropdown-submenu');
    submenus.forEach(submenu => {
        const submenuToggle = submenu.querySelector('.dropdown-toggle');
        const submenuMenu = submenu.querySelector('.dropdown-menu');
        let submenuTimeoutId;

        if (submenuToggle && submenuMenu) {
            // Prevenir click no submenu toggle
            submenuToggle.addEventListener('click', function (e) {
                e.preventDefault();
                return false;
            });

            // Mostrar submenu no hover
            submenu.addEventListener('mouseenter', function () {
                clearTimeout(submenuTimeoutId);
                submenuMenu.classList.add('show');
            });

            // Esconder submenu ao sair
            submenu.addEventListener('mouseleave', function () {
                submenuTimeoutId = setTimeout(function () {
                    submenuMenu.classList.remove('show');
                }, 200);
            });
        }
    });
});
