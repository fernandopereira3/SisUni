// entrada_saida.js
// Funcionalidades da página entrada_saida.html

// Adiciona botões de detalhes na tabela quando carrega
document.addEventListener('DOMContentLoaded', function () {
    adicionarBotoesDetalhes();
});

function adicionarBotoesDetalhes() {
    const tabela = document.getElementById('tabela-sentenciados');
    if (!tabela) return;

    tabela.querySelectorAll('tbody tr').forEach(linha => {
        const colunaAcoes = linha.querySelector('td:last-child');
        if (colunaAcoes && !colunaAcoes.querySelector('.btn-info')) {
            const matricula = linha.querySelector('td:first-child').textContent.trim();

            const botao = document.createElement('button');
            botao.className = 'btn btn-sm btn-success ms-1';
            botao.innerHTML = 'Adicionar';
            botao.onclick = () => adicionar(matricula);

            colunaAcoes.appendChild(botao);
        }
    });
}

// Função para obter o token CSRF
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Configurar headers padrão para todas as requisições fetch
function fetchWithCSRF(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        }
    };

    // Merge das opções
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };

    return fetch(url, mergedOptions);
}

// Função para atualizar o resumo sem recarregar a página
function atualizarResumo() {
    fetch('/api/resumo')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-matriculas').textContent = data.matriculas;
            document.getElementById('total-garrafas').textContent = data.garrafas;
            document.getElementById('total-homens').textContent = data.homens;
            document.getElementById('total-mulheres').textContent = data.mulheres;
            document.getElementById('total-criancas').textContent = data.criancas;
            document.getElementById('total-visitantes').textContent = data.total_visitantes;
        })
        .catch(error => {
            console.error('Erro ao atualizar resumo:', error);
        });
}

// Função para adicionar sentenciado à lista
function adicionar(matricula) {
    // Obter valores dos inputs
    var nome = document.getElementById('nome').value;
    var garrafas = document.getElementById('garrafas').value || 0;
    var homens = document.getElementById('homens').value || 0;
    var mulheres = document.getElementById('mulheres').value || 0;
    var criancas = document.getElementById('criancas').value || 0;

    // Preparar dados para enviar
    var dados = {
        garrafas: garrafas,
        homens: homens,
        mulheres: mulheres,
        criancas: criancas
    };

    // Fazer a requisição AJAX usando fetch
    fetchWithCSRF('/adicionar/' + matricula, {
        method: 'POST',
        body: JSON.stringify(dados)
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            // Verificar se houve sucesso
            if (data.status === 'success') {
                // Verificar se o sentenciado tem trabalho alocado
                if (data.tem_trabalho) {
                    alert("ATENÇÃO: este sentenciado está TRABALHANDO na " + data.setor);
                }

                // Mostrar mensagem de sucesso
                alert(data.message);

                // ATUALIZAR O RESUMO EM TEMPO REAL
                atualizarResumo();

                // Limpar os campos do formulário
                document.getElementById('garrafas').value = '0';
                document.getElementById('homens').value = '0';
                document.getElementById('mulheres').value = '0';
                document.getElementById('criancas').value = '0';

                // Opcional: recarregar a página após um pequeno atraso se necessário
                // setTimeout(function() {
                //     window.location.reload();
                // }, 1000);
            } else {
                // Mostrar mensagem de erro
                alert(data.message);
            }
        })
        .catch(function (error) {
            console.error('Erro:', error);
            alert('Erro ao processar a requisição');
        });

    // Impedir comportamento padrão do botão/formulário
    return false;
}

// Atualizar resumo automaticamente a cada 30 segundos
setInterval(atualizarResumo, 30000);

// Corrigir comportamento dos form-floating labels
document.addEventListener('DOMContentLoaded', function () {
    const floatingInputs = document.querySelectorAll('.form-floating input');

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
