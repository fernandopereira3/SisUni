// trabalho.js
// Funcionalidades da página trabalho.html

// Função para carregar dados da API
function carregarDados() {
    fetch('/trabalho/api')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                exibirTabela(data.data);
                atualizarEstatisticas(data.data);
            } else {
                exibirErro(data.message || 'Erro ao carregar dados');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            exibirErro('Erro de conexão com o servidor');
        });
}

// Função para exibir a tabela
function exibirTabela(dados) {
    const container = document.getElementById('tabela-trabalho-container');

    if (!dados || dados.length === 0) {
        container.innerHTML = '<p class="alert alert-info">Nenhum trabalhador cadastrado.</p>';
        return;
    }

    let html = `
        <table class="table table-striped table-hover" id="tabela-trabalho">
            <thead class="table-dark">
                <tr>
                    <th>Matrícula</th>
                    <th>Nome</th>
                    <th>Setor</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
    `;

    dados.forEach(item => {
        html += `
            <tr>
                <td>${item.matricula || ''}</td>
                <td>${item.nome || ''}</td>
                <td>${item.setor || 'Não especificado'}</td>
                <td>
                    <button class="btn btn-sm btn-info" onclick="verDetalhes('${item.matricula}')">
                        <i class="fas fa-eye"></i> Ver
                    </button>
                </td>
            </tr>
        `;
    });

    html += `
            </tbody>
        </table>
    `;

    container.innerHTML = html;
}

// Função para atualizar estatísticas
function atualizarEstatisticas(dados) {
    const totalTrabalhadores = dados.length;
    const setoresUnicos = [...new Set(dados.map(item => item.setor).filter(setor => setor))];
    const totalSetores = setoresUnicos.length;

    document.getElementById('total-trabalhadores').textContent = totalTrabalhadores;
    document.getElementById('total-setores').textContent = totalSetores;
    document.getElementById('ultima-atualizacao').textContent = new Date().toLocaleString('pt-BR');
}

// Função para exibir erro
function exibirErro(mensagem) {
    const container = document.getElementById('tabela-trabalho-container');
    container.innerHTML = `<p class="alert alert-danger">${mensagem}</p>`;
}

// Função para atualizar dados
function atualizarDados() {
    const container = document.getElementById('tabela-trabalho-container');
    container.innerHTML = `
        <div class="text-center p-4">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Atualizando...</span>
            </div>
            <p class="mt-2">Atualizando dados...</p>
        </div>
    `;
    carregarDados();
}

// Função para ver detalhes
function verDetalhes(matricula) {
    alert(`Detalhes do trabalhador com matrícula: ${matricula}\n\nEsta funcionalidade será implementada em breve.`);
}

// Carregar dados ao inicializar a página
document.addEventListener('DOMContentLoaded', function () {
    carregarDados();
});
