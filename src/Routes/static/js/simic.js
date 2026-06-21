// simic.js - JavaScript para a página SIMIC

document.addEventListener('DOMContentLoaded', function () {
    console.log('SIMIC page loaded');

    // Carregar dados iniciais
    carregarDadosSIMIC();
});

/**
 * Carrega os dados do SIMIC
 */
function carregarDadosSIMIC() {
    // Placeholder - implementar chamada à API
    console.log('Carregando dados do SIMIC...');

    // Simular carregamento de estatísticas
    setTimeout(() => {
        document.getElementById('total-pacientes').textContent = '0';
        document.getElementById('total-consultas').textContent = '0';
        document.getElementById('total-medicamentos').textContent = '0';
        document.getElementById('ultima-atualizacao').textContent = new Date().toLocaleString('pt-BR');

        // Limpar spinner e mostrar mensagem
        const container = document.getElementById('tabela-simic-container');
        container.innerHTML = '<div class="alert alert-info">Nenhum paciente cadastrado no momento.</div>';
    }, 1000);
}

/**
 * Atualiza os dados da página
 */
function atualizarDados() {
    console.log('Atualizando dados...');

    // Mostrar spinner
    const container = document.getElementById('tabela-simic-container');
    container.innerHTML = `
        <div class="text-center p-4">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
            <p class="mt-2">Atualizando dados...</p>
        </div>
    `;

    // Recarregar dados
    carregarDadosSIMIC();
}
