document.addEventListener('DOMContentLoaded', function () {
    // Variável para controlar se deve mostrar o modal
    const shouldShowModal = document.body.dataset.showStarModal === 'true';
    // Controle do modal Star
    const starPasswordModal = new bootstrap.Modal(document.getElementById('starPasswordModal'));
    const confirmStarPassword = document.getElementById('confirmStarPassword');
    const starPasswordInput = document.getElementById('starPasswordInput');
    const confirmPasswordInput = document.getElementById('confirmPasswordInput');
    const starPasswordForm = document.getElementById('starPasswordForm');
    const mainForm = document.querySelector('form[action=""]');

    // Mostrar modal automaticamente se necessário (após tentativa de login)
    if (shouldShowModal) {
        // Preencher o campo username com o valor do backend se disponível
        const usernameFromBackend = document.getElementById('hiddenUsername').value;
        if (usernameFromBackend) {
            document.getElementById('username').value = usernameFromBackend;
        }

        // Verificar se é definição de nova senha ou validação de senha existente
        const errorMessage = document.body.dataset.errorMessage || '';
        const isExistingPassword = errorMessage.includes('Digite sua senha administrativa') || errorMessage.includes('Senha admin incorreta');

        if (isExistingPassword) {
            // Usuário já tem senha - apenas solicitar
            document.getElementById('modalMessage').textContent = 'Digite sua senha administrativa para continuar.';
            document.getElementById('starPasswordModalLabel').innerHTML = '<i class="fas fa-key me-2"></i>Senha Administrativa';
            document.getElementById('starPasswordInput').placeholder = 'Senha Administrativa';
            document.querySelector('label[for="starPasswordInput"]').innerHTML = '<i class="fas fa-key me-2"></i>Senha Administrativa';
            document.getElementById('confirmPasswordInput').style.display = 'none';
            document.querySelector('label[for="confirmPasswordInput"]').style.display = 'none';
            document.getElementById('confirmStarPassword').innerHTML = '<i class="fas fa-sign-in-alt me-2"></i>Entrar';
        }

        starPasswordModal.show();
    }

    // Confirmar criação de senha Star
    confirmStarPassword.addEventListener('click', function () {
        const password = starPasswordInput.value.trim();
        const confirmPassword = confirmPasswordInput.value.trim();
        const errorMessage = document.body.dataset.errorMessage || '';
        const isExistingPassword = errorMessage.includes('Digite sua senha administrativa') || errorMessage.includes('Senha admin incorreta');

        if (!password) {
            alert(isExistingPassword ? 'Por favor, digite sua senha administrativa.' : 'Por favor, digite a nova senha administrativa.');
            starPasswordInput.focus();
            return;
        }

        if (!isExistingPassword) {
            // Validações apenas para nova senha
            if (password.length < 6) {
                alert('A senha deve ter pelo menos 6 caracteres.');
                starPasswordInput.focus();
                return;
            }

            if (password !== confirmPassword) {
                alert('As senhas não coincidem. Por favor, verifique.');
                confirmPasswordInput.focus();
                return;
            }
        }

        // Copiar dados do formulário principal para o modal
        const username = document.getElementById('username').value.trim();
        const setor = document.getElementById('setor').value;

        // Debug: verificar se os valores estão sendo capturados
        console.log('Username capturado:', username);
        console.log('Setor capturado:', setor);

        if (!username) {
            alert('Por favor, digite seu nome antes de definir a senha.');
            document.getElementById('username').focus();
            starPasswordModal.hide();
            return;
        }

        document.getElementById('hiddenUsername').value = username;
        document.getElementById('hiddenSetor').value = setor;

        // Submeter formulário do modal
        starPasswordForm.submit();
    });

    // Enter nos campos de senha
    starPasswordInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            confirmPasswordInput.focus();
        }
    });

    confirmPasswordInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            confirmStarPassword.click();
        }
    });

    // Limpar senhas ao fechar modal
    document.getElementById('starPasswordModal').addEventListener('hidden.bs.modal', function () {
        starPasswordInput.value = '';
        confirmPasswordInput.value = '';
    });

    // Corrigir comportamento dos form-floating labels
    const floatingInputs = document.querySelectorAll('.form-floating input, .form-floating select');

    floatingInputs.forEach(input => {
        // Verificar se já tem valor ao carregar
        if (input.value) {
            input.classList.add('filled');
        }

        // Adicionar/remover classe quando o valor muda
        input.addEventListener('input', function () {
            if (this.value) {
                this.classList.add('filled');
            } else {
                this.classList.remove('filled');
            }
        });
    });
});
