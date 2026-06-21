// lista.js
// Funcionalidades da página lista.html

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

function editarMarcadores(matricula, nome, garrafas, homens, mulheres, criancas) {
    // Converter strings para números se necessário
    garrafas = parseInt(garrafas) || 0;
    homens = parseInt(homens) || 0;
    mulheres = parseInt(mulheres) || 0;
    criancas = parseInt(criancas) || 0;

    // Preencher o modal com os dados atuais
    document.getElementById('editMatricula').value = matricula;
    document.getElementById('editNome').textContent = nome;
    document.getElementById('editGarrafas').value = garrafas;
    document.getElementById('editHomens').value = homens;
    document.getElementById('editMulheres').value = mulheres;
    document.getElementById('editCriancas').value = criancas;

    // Mostrar o modal
    const modal = new bootstrap.Modal(document.getElementById('editarModal'));
    modal.show();
}

function atualizarTabela() {
    fetch('/api/lista_dados')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const tbody = document.querySelector('#tabela_entrada tbody');
                if (tbody) {
                    // Limpar tbody atual
                    tbody.innerHTML = '';

                    // Adicionar novas linhas
                    data.documentos.forEach(doc => {
                        const row = `
                            <tr id="row-${doc.matricula}">
                                <td>${doc.matricula}</td>
                                <td>${doc.nome}</td>
                                <td id="garrafas-${doc.matricula}">${doc.garrafas}</td>
                                <td id="homens-${doc.matricula}">${doc.homens}</td>
                                <td id="mulheres-${doc.matricula}">${doc.mulheres}</td>
                                <td id="criancas-${doc.matricula}">${doc.criancas}</td>
                                <td>${doc.pavilhao || ''}</td>
                                <td>${doc.data_visita}</td>
                                <td>
                                    <button class="btn btn-sm btn-warning me-1"
                                        onclick="editarMarcadores('${doc.matricula}', '${doc.nome}', '${doc.garrafas}', '${doc.homens}', '${doc.mulheres}', '${doc.criancas}')">
                                        <i class="bi bi-pencil-square"></i>
                                    </button>
                                    <button class="btn btn-sm btn-danger" onclick="removerVisita('${doc.matricula}')">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        `;
                        tbody.innerHTML += row;
                    });
                }
            }
        })
        .catch(error => {
            console.error('Erro ao atualizar tabela:', error);
        });
}

function salvarMarcadores() {
    const matricula = document.getElementById('editMatricula').value;
    const garrafas = parseInt(document.getElementById('editGarrafas').value) || 0;
    const homens = parseInt(document.getElementById('editHomens').value) || 0;
    const mulheres = parseInt(document.getElementById('editMulheres').value) || 0;
    const criancas = parseInt(document.getElementById('editCriancas').value) || 0;

    fetchWithCSRF(`/editar_marcadores/${matricula}`, {
        method: 'PUT',
        body: JSON.stringify({
            garrafas: garrafas,
            homens: homens,
            mulheres: mulheres,
            criancas: criancas
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Fechar modal
                bootstrap.Modal.getInstance(document.getElementById('editarModal')).hide();

                // Mostrar mensagem pedindo para atualizar
                alert('Dados salvos com sucesso! Pressione F5 para ver as alterações na tabela.');
            } else {
                alert('Erro: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao salvar');
        });
}

function removerVisita(matricula) {
    fetchWithCSRF(`/remover_visita_hoje/${matricula}`, {
        method: 'DELETE'
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                document.getElementById(`row-${matricula}`).remove();
                // Atualizar o resumo após remover
                atualizarResumo();
                alert(data.message);
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            alert('Erro ao remover visita');
            console.error('Error:', error);
        });
}

// Forçar comportamento hover nos dropdowns
document.addEventListener('DOMContentLoaded', function () {
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
