// jumbo.js
// Funcionalidades da página jumbo.html

// Corrigir comportamento dos form-floating labels
document.addEventListener('DOMContentLoaded', function () {
    const floatingInputs = document.querySelectorAll('.form-floating input, .form-floating select');

    floatingInputs.forEach(input => {
        // Função para verificar se o input tem valor e ajustar o label
        function checkFloatingLabel() {
            const parent = input.closest('.form-floating');
            const label = parent.querySelector('label');

            if (input.value && input.value.trim() !== '' && input.value !== '0') {
                parent.classList.add('has-value');
                // Forçar o label para cima
                if (label) {
                    label.style.transform = 'scale(0.85) translateY(-0.5rem) translateX(0.15rem)';
                    label.style.opacity = '0.65';
                }
            } else {
                parent.classList.remove('has-value');
                // Resetar o label
                if (label && input.value === '') {
                    label.style.transform = '';
                    label.style.opacity = '';
                }
            }
        }

        // Verificar no carregamento da página
        checkFloatingLabel();

        // Verificar quando o usuário digita
        input.addEventListener('input', checkFloatingLabel);
        input.addEventListener('focus', function () {
            const parent = input.closest('.form-floating');
            const label = parent.querySelector('label');
            if (label) {
                label.style.transform = 'scale(0.85) translateY(-0.5rem) translateX(0.15rem)';
                label.style.opacity = '0.65';
            }
        });
        input.addEventListener('blur', checkFloatingLabel);
        input.addEventListener('change', checkFloatingLabel);
    });
});
