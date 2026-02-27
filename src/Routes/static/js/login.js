document.addEventListener('DOMContentLoaded', function () {
    // Variável para controlar se deve mostrar o modal
    const shouldShowModal = document.body.dataset.showStarModal === 'true';
    // true = criando senha pela primeira vez; false = autenticando com senha existente
    const isCreatePassword = document.body.dataset.createPassword === 'true';

    // Controle do modal Star
    const starPasswordModal = new bootstrap.Modal(document.getElementById('starPasswordModal'));
    const confirmStarPassword = document.getElementById('confirmStarPassword');
    const starPasswordInput = document.getElementById('starPasswordInput');
    const confirmPasswordInput = document.getElementById('confirmPasswordInput'); // pode ser null no modo autenticação
    const starPasswordForm = document.getElementById('starPasswordForm');

    // Mostrar modal automaticamente se necessário (após tentativa de login)
    if (shouldShowModal) {
        // Preencher o campo username com o valor do backend se disponível
        const usernameFromBackend = document.getElementById('hiddenUsername').value;
        if (usernameFromBackend) {
            document.getElementById('username').value = usernameFromBackend;
        }
        starPasswordModal.show();
    }

    // Confirmar criação/digitação de senha
    confirmStarPassword.addEventListener('click', function () {
        const password = starPasswordInput.value.trim();

        if (!password) {
            alert(isCreatePassword
                ? 'Por favor, digite a nova senha administrativa.'
                : 'Por favor, digite sua senha administrativa.');
            starPasswordInput.focus();
            return;
        }

        if (isCreatePassword) {
            // Validações apenas para nova senha
            if (password.length < 6) {
                alert('A senha deve ter pelo menos 6 caracteres.');
                starPasswordInput.focus();
                return;
            }

            if (confirmPasswordInput) {
                const confirmPassword = confirmPasswordInput.value.trim();
                if (password !== confirmPassword) {
                    alert('As senhas não coincidem. Por favor, verifique.');
                    confirmPasswordInput.focus();
                    return;
                }
            }
        }

        // Copiar dados do formulário principal para o modal
        const username = document.getElementById('username').value.trim();
        const setor = document.getElementById('setor').value;

        if (!username) {
            alert('Por favor, digite seu nome antes de continuar.');
            document.getElementById('username').focus();
            starPasswordModal.hide();
            return;
        }

        document.getElementById('hiddenUsername').value = username;
        document.getElementById('hiddenSetor').value = setor;

        // Submeter formulário do modal
        starPasswordForm.submit();
    });

    // Enter no campo de senha principal
    starPasswordInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            if (isCreatePassword && confirmPasswordInput) {
                confirmPasswordInput.focus();
            } else {
                confirmStarPassword.click();
            }
        }
    });

    // Enter no campo de confirmação (só existe no modo criação)
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                confirmStarPassword.click();
            }
        });
    }

    // Limpar senhas ao fechar modal
    document.getElementById('starPasswordModal').addEventListener('hidden.bs.modal', function () {
        starPasswordInput.value = '';
        if (confirmPasswordInput) confirmPasswordInput.value = '';
    });

    // Corrigir comportamento dos form-floating labels
    const floatingInputs = document.querySelectorAll('.form-floating input, .form-floating select');

    floatingInputs.forEach(input => {
        if (input.value) {
            input.classList.add('filled');
        }
        input.addEventListener('input', function () {
            if (this.value) {
                this.classList.add('filled');
            } else {
                this.classList.remove('filled');
            }
        });
    });
});
