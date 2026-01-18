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

// Função para abrir o modal de criação de funcionário
function abrirModalCriarFuncionario() {
    const modal = new bootstrap.Modal(document.getElementById('criarFuncionarioModal'));
    modal.show();
}

// Função para criar funcionário
function criarFuncionario() {
    const nomeCompleto = document.getElementById('nomeCompleto').value.trim();
    const username = document.getElementById('username').value.trim().toLowerCase();
    const turno = document.getElementById('turno').value;
    const lvl = document.getElementById('permissao').value;

    // Validação básica
    if (!nomeCompleto || !username || !turno || !lvl) {
        alert('Por favor, preencha todos os campos obrigatórios.');
        return;
    }

    // Dados para envio
    const dadosFuncionario = {
        nome_completo: nomeCompleto,
        username: username,
        turno: turno,
        lvl: lvl
    };

    // Enviar requisição
    fetchWithCSRF('/api/criar_funcionario', {
        method: 'POST',
        body: JSON.stringify(dadosFuncionario)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Limpar formulário
                document.getElementById('formCriarFuncionario').reset();

                // Fechar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('criarFuncionarioModal'));
                modal.hide();

                // Mostrar mensagem de sucesso
                alert(`Funcionário criado com sucesso!\n\nNome: ${data.funcionario.nome_completo}\nUsername: ${data.funcionario.username}\nTurno: ${data.funcionario.turno}\nNível: ${data.funcionario.lvl}`);

                // Recarregar lista de funcionários
                carregarFuncionarios();
            } else {
                alert('Erro ao criar funcionário: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao criar funcionário. Tente novamente.');
        });
}

// Função para carregar lista de funcionários
function carregarFuncionarios() {
    console.log('[DEBUG] Iniciando carregamento de funcionários...');
    fetch('/api/listar_funcionarios')
        .then(response => {
            console.log('[DEBUG] Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('[DEBUG] Dados recebidos:', data);
            if (data.success) {
                const tbody = document.getElementById('tabelaFuncionarios');
                console.log('[DEBUG] Tbody encontrado:', tbody);

                if (!tbody) {
                    console.error('[ERRO] Elemento tabelaFuncionarios não encontrado!');
                    return;
                }

                tbody.innerHTML = '';
                console.log('[DEBUG] Total de funcionários:', data.funcionarios.length);

                data.funcionarios.forEach(funcionario => {
                    const row = tbody.insertRow();

                    // Determinar badge de permissão baseado no nível
                    let permissao = '<span class="badge bg-secondary">Usuário</span>';
                    if (funcionario.lvl === '10' || funcionario.lvl === '0') {
                        permissao = '<span class="badge bg-danger">Super Admin</span>';
                    } else if (parseInt(funcionario.lvl) >= 7) {
                        permissao = '<span class="badge bg-warning">Admin</span>';
                    } else if (parseInt(funcionario.lvl) >= 4) {
                        permissao = '<span class="badge bg-info">Moderador</span>';
                    } else if (parseInt(funcionario.lvl) < 4) {
                        permissao = '<span class="badge bg-info">Usuário</span>';
                    }

                    row.innerHTML = `
                    <td>${funcionario.nome_completo || 'N/A'}</td>
                    <td>${funcionario.username}</td>
                    <td>${funcionario.setor || 'N/A'}</td>
                    <td>${permissao} <span class="badge bg-light text-dark">LVL ${funcionario.lvl || '1'}</span></td>
                    <td>${funcionario.total_logins || 0}</td>
                    <td>${funcionario.ultimo_login || 'Nunca'}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="editarFuncionario('${funcionario.username}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="excluirFuncionario('${funcionario.username}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                });
                console.log('[DEBUG] Tabela carregada com sucesso!');
            } else {
                console.error('[ERRO] API retornou success=false:', data.message);
            }
        })
        .catch(error => {
            console.error('[ERRO] Erro ao carregar funcionários:', error);
        });
}

// Função para editar funcionário
function editarFuncionario(username) {
    // Buscar dados do funcionário
    fetch('/api/listar_funcionarios')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.funcionarios) {
                const funcionario = data.funcionarios.find(f => f.username == username);
                if (funcionario) {
                    // Preencher o modal com os dados do funcionário
                    document.getElementById('editUsername').value = funcionario.username;
                    document.getElementById('editNomeCompleto').value = funcionario.nome_completo || '';
                    document.getElementById('editTurno').value = funcionario.turno || '';
                    document.getElementById('editStar').checked = funcionario.star || false;

                    // Abrir o modal
                    const modal = new bootstrap.Modal(document.getElementById('editarFuncionarioModal'));
                    modal.show();
                } else {
                    alert('Funcionário não encontrado');
                }
            } else {
                alert('Erro ao carregar dados dos funcionários');
            }
        })
        .catch(error => {
            console.error('Erro ao buscar dados do funcionário:', error);
            alert('Erro ao buscar dados do funcionário');
        });
}

// Função para salvar edição do funcionário
function salvarEdicaoFuncionario() {
    const username = document.getElementById('editUsername').value;
    const nome = document.getElementById('editNomeCompleto').value;
    const turno = document.getElementById('editTurno').value;
    const star = document.getElementById('editStar').checked;

    if (!nome || !turno) {
        alert('Por favor, preencha todos os campos obrigatórios.');
        return;
    }

    const dadosAtualizados = {
        nome: nome,
        turno: turno,
        star: star
    };

    fetchWithCSRF(`/api/editar_funcionario/${username}`, {
        method: 'PUT',
        body: JSON.stringify(dadosAtualizados)
    })
        .then(response => {
            return response.json().then(data => ({ status: response.status, data: data }));
        })
        .then(result => {
            alert(result.data.message);
            if (result.status === 200) {
                // Fechar o modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('editarFuncionarioModal'));
                modal.hide();
                // Recarregar a lista de funcionários
                carregarFuncionarios();
            }
        })
        .catch(error => {
            console.error('Erro ao editar funcionário:', error);
            alert('Erro ao editar funcionário');
        });
}

// Função para excluir funcionário
function excluirFuncionario(username) {
    // Buscar dados do funcionário para mostrar o nome no modal de confirmação
    fetch('/api/listar_funcionarios')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.funcionarios) {
                const funcionario = data.funcionarios.find(f => f.username == username);
                if (funcionario) {
                    document.getElementById('nomeExclusao').textContent = funcionario.nome_completo || funcionario.username;
                    document.getElementById('usernameExclusao').value = funcionario.username;

                    // Abrir o modal de confirmação
                    const modal = new bootstrap.Modal(document.getElementById('confirmarExclusaoModal'));
                    modal.show();
                } else {
                    alert('Funcionário não encontrado');
                }
            } else {
                alert('Erro ao carregar dados dos funcionários');
            }
        })
        .catch(error => {
            console.error('Erro ao buscar dados do funcionário:', error);
            alert('Erro ao buscar dados do funcionário');
        });
}

// Função para confirmar exclusão do funcionário
function confirmarExclusaoFuncionario() {
    const username = document.getElementById('usernameExclusao').value;

    fetchWithCSRF(`/api/excluir_funcionario/${username}`, {
        method: 'DELETE'
    })
        .then(response => {
            return response.json().then(data => ({ status: response.status, data: data }));
        })
        .then(result => {
            alert(result.data.message);
            if (result.status === 200) {
                // Fechar o modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('confirmarExclusaoModal'));
                modal.hide();
                // Recarregar a lista de funcionários
                carregarFuncionarios();
            }
        })
        .catch(error => {
            console.error('Erro ao excluir funcionário:', error);
            alert('Erro ao excluir funcionário');
        });
}

// Carregar funcionários ao carregar a página
document.addEventListener('DOMContentLoaded', function () {
    carregarFuncionarios();
});
