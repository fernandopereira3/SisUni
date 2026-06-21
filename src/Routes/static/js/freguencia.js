// freguencia.js - Gerenciamento de Frequência de Reeducandos

document.addEventListener('DOMContentLoaded', function () {
    // Inicializar a página
    inicializarPagina();

    // Event listeners para os botões
    document.getElementById('btnMarcarPresenca').addEventListener('click', marcarPresenca);
    document.getElementById('btnMarcarFalta').addEventListener('click', marcarFalta);
    document.getElementById('btnMarcarRetorno').addEventListener('click', marcarRetorno);

    // Event listener para o botão de pesquisa
    document.getElementById('btnAbrirPesquisa').addEventListener('click', function () {
        const pesquisaModal = new bootstrap.Modal(document.getElementById('pesquisaModal'));
        pesquisaModal.show();
    });
});

function inicializarPagina() {
    // Verificar se há dados na sessão ou URL
    const urlParams = new URLSearchParams(window.location.search);
    const matricula = urlParams.get('matricula');

    if (matricula) {
        carregarDadosReeducando(matricula);
    }
}

function pesquisarReeducando() {
    const matricula = document.getElementById('pesquisaMatricula').value.trim();
    const nome = document.getElementById('pesquisaNome').value.trim();

    if (!matricula && !nome) {
        alert('Por favor, informe a matrícula ou o nome para pesquisar.');
        return;
    }

    // Fechar modal
    const pesquisaModal = bootstrap.Modal.getInstance(document.getElementById('pesquisaModal'));
    pesquisaModal.hide();

    // Carregar dados
    if (matricula) {
        carregarDadosReeducando(matricula);
    } else {
        buscarPorNome(nome);
    }
}

function carregarDadosReeducando(matricula) {
    // Mostrar loading
    mostrarLoading();

    fetch(`/api/reeducando/${matricula}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Reeducando não encontrado');
            }
            return response.json();
        })
        .then(data => {
            preencherDados(data);
            carregarFrequencia(matricula);
        })
        .catch(error => {
            console.error('Erro ao carregar dados:', error);
            alert('Erro ao carregar dados do reeducando. Por favor, tente novamente.');
        })
        .finally(() => {
            esconderLoading();
        });
}

function buscarPorNome(nome) {
    // Implementar busca por nome
    mostrarLoading();

    fetch(`/api/reeducando/buscar?nome=${encodeURIComponent(nome)}`)
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                alert('Nenhum reeducando encontrado com esse nome.');
                return;
            }

            if (data.length === 1) {
                preencherDados(data[0]);
                carregarFrequencia(data[0].matricula);
            } else {
                // Mostrar lista para seleção
                mostrarListaSelecao(data);
            }
        })
        .catch(error => {
            console.error('Erro ao buscar:', error);
            alert('Erro ao buscar reeducando. Por favor, tente novamente.');
        })
        .finally(() => {
            esconderLoading();
        });
}

function preencherDados(data) {
    // Preencher foto
    const fotoContainer = document.getElementById('fotoContainer');
    if (data.foto) {
        fotoContainer.innerHTML = `<img src="${data.foto}" alt="Foto do reeducando">`;
    }

    // Preencher informações pessoais
    document.getElementById('nome').textContent = data.nome || '-';
    document.getElementById('nascimento').textContent = formatarData(data.nascimento) || '-';
    document.getElementById('matricula').textContent = data.matricula || '-';
    document.getElementById('inclusao').textContent = formatarData(data.inclusao) || '-';
    document.getElementById('procedencia').textContent = data.procedencia || '-';
    document.getElementById('localizacaoHabitacional').textContent = data.localizacao_habitacional || '-';
    document.getElementById('ultimaMovimentacao').textContent = formatarDataHora(data.ultima_movimentacao) || '-';
    document.getElementById('localizacaoAtual').textContent = data.localizacao_atual || '-';
    document.getElementById('localTrabalho').textContent = data.local_trabalho || '-';
}

function carregarFrequencia(matricula) {
    fetch(`/api/frequencia/${matricula}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('presentes').textContent = data.presentes || 0;
            document.getElementById('faltas').textContent = data.faltas || 0;
            document.getElementById('retorno').textContent = data.retorno || 0;
        })
        .catch(error => {
            console.error('Erro ao carregar frequência:', error);
        });
}

function marcarPresenca() {
    const matricula = document.getElementById('matricula').textContent;

    if (matricula === '-') {
        alert('Por favor, pesquise um reeducando primeiro.');
        return;
    }

    if (!confirm('Confirma a marcação de presença?')) {
        return;
    }

    registrarFrequencia(matricula, 'presenca');
}

function marcarFalta() {
    const matricula = document.getElementById('matricula').textContent;

    if (matricula === '-') {
        alert('Por favor, pesquise um reeducando primeiro.');
        return;
    }

    if (!confirm('Confirma a marcação de falta?')) {
        return;
    }

    registrarFrequencia(matricula, 'falta');
}

function marcarRetorno() {
    const matricula = document.getElementById('matricula').textContent;

    if (matricula === '-') {
        alert('Por favor, pesquise um reeducando primeiro.');
        return;
    }

    if (!confirm('Confirma a marcação de retorno?')) {
        return;
    }

    registrarFrequencia(matricula, 'retorno');
}

function registrarFrequencia(matricula, tipo) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    mostrarLoading();

    fetch('/api/frequencia/registrar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            matricula: matricula,
            tipo: tipo,
            data_hora: new Date().toISOString()
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao registrar frequência');
            }
            return response.json();
        })
        .then(data => {
            alert(`${tipo.charAt(0).toUpperCase() + tipo.slice(1)} registrada com sucesso!`);
            carregarFrequencia(matricula);
        })
        .catch(error => {
            console.error('Erro ao registrar frequência:', error);
            alert('Erro ao registrar frequência. Por favor, tente novamente.');
        })
        .finally(() => {
            esconderLoading();
        });
}

function formatarData(data) {
    if (!data) return null;

    const d = new Date(data);
    const dia = String(d.getDate()).padStart(2, '0');
    const mes = String(d.getMonth() + 1).padStart(2, '0');
    const ano = d.getFullYear();

    return `${dia}/${mes}/${ano}`;
}

function formatarDataHora(dataHora) {
    if (!dataHora) return null;

    const d = new Date(dataHora);
    const dia = String(d.getDate()).padStart(2, '0');
    const mes = String(d.getMonth() + 1).padStart(2, '0');
    const ano = d.getFullYear();
    const hora = String(d.getHours()).padStart(2, '0');
    const minuto = String(d.getMinutes()).padStart(2, '0');

    return `${dia}/${mes}/${ano} ${hora}:${minuto}`;
}

function mostrarLoading() {
    // Implementar loading overlay se necessário
    document.body.style.cursor = 'wait';
}

function esconderLoading() {
    document.body.style.cursor = 'default';
}

function mostrarListaSelecao(lista) {
    // Implementar modal de seleção quando houver múltiplos resultados
    console.log('Múltiplos resultados encontrados:', lista);
    alert('Múltiplos reeducandos encontrados. Por favor, refine sua busca usando a matrícula.');
}
