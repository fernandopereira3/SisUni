// pesquisa.js
// Funcionalidades da página pesquisa.html

// Adiciona botões de detalhes na tabela quando carrega
document.addEventListener('DOMContentLoaded', function () {
    adicionarBotoesDetalhes();
    atualizarEstatisticas();
});

function adicionarBotoesDetalhes() {
    // Procurar por tabelas de sentenciados ou excluidos
    const tabelaSentenciados = document.getElementById('tabela-sentenciados');
    const tabelaExcluidos = document.getElementById('tabela-excluidos');
    const tabela = tabelaSentenciados || tabelaExcluidos;

    if (!tabela) return;

    tabela.querySelectorAll('tbody tr').forEach(linha => {
        const colunaAcoes = linha.querySelector('td:last-child');
        if (colunaAcoes && !colunaAcoes.querySelector('.btn-info')) {
            const matricula = linha.querySelector('td:first-child').textContent.trim();

            const botao = document.createElement('button');
            botao.className = 'btn btn-sm btn-info ms-1';
            botao.innerHTML = 'Detalhes';

            // Determinar qual rota usar baseado no ID da tabela
            const isExcluidos = tabela.id === 'tabela-excluidos';
            botao.onclick = () => carregarDetalhes(matricula, isExcluidos);

            colunaAcoes.appendChild(botao);
        }
    });
}

// Função para atualizar estatísticas
function atualizarEstatisticas() {
    const tabelaSentenciados = document.getElementById('tabela-sentenciados');
    const tabelaExcluidos = document.getElementById('tabela-excluidos');
    const tabela = tabelaSentenciados || tabelaExcluidos;

    if (tabela) {
        const totalLinhas = tabela.querySelectorAll('tbody tr').length;
        document.getElementById('total-registros').textContent = totalLinhas;
    } else {
        document.getElementById('total-registros').textContent = '0';
    }

    // Atualizar horário da última pesquisa
    const agora = new Date();
    const horario = agora.toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit'
    });
    document.getElementById('ultima-pesquisa').textContent = horario;
}

// Função para carregar os detalhes do sentenciado via AJAX
function carregarDetalhes(matricula, isExcluidos = false) {
    console.log('Iniciando carregamento para matricula:', matricula, 'isExcluidos:', isExcluidos);

    // Mostrar a modal
    var myModal = new bootstrap.Modal(document.getElementById('detalhesSentenciadoModal'));

    // Atualizar o título da modal baseado no tipo
    const modalTitle = document.getElementById('detalhesSentenciadoModalLabel');
    modalTitle.textContent = isExcluidos ? 'Detalhes do Excluído' : 'Detalhes do Sentenciado';

    myModal.show();

    // Determinar a rota baseada no tipo
    const rota = isExcluidos ? `/excluido_detalhes/${matricula}` : `/sentenciado_detalhes/${matricula}`;

    // Fazer a requisição AJAX para obter os detalhes
    fetch(rota)
        .then(response => {
            console.log('Status da resposta:', response.status);
            console.log('Response OK:', response.ok);

            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status} - ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Dados recebidos completos:', data);
            console.log('Tipo dos dados:', typeof data);

            // Verificação mais robusta
            if (!data || (typeof data === 'object' && Object.keys(data).length === 0)) {
                throw new Error('Nenhum dado válido recebido do servidor');
            }

            // Se há erro na resposta
            if (data.erro) {
                throw new Error(data.erro);
            }

            // Preencher a modal com os detalhes
            const conteudo = criarConteudoDetalhes(data, isExcluidos);
            document.getElementById('detalhesSentenciadoConteudo').innerHTML = conteudo;

            // Carregar a foto do sentenciado (se existir)
            if (data.matricula) {
                carregarFotoSentenciado(data.matricula);
            }
        })
        .catch(error => {
            console.error('Erro completo:', error);
            document.getElementById('detalhesSentenciadoConteudo').innerHTML =
                `<div class="alert alert-danger">
                    <h5>Erro ao carregar detalhes:</h5>
                    <p>${error.message}</p>
                    <small>Matrícula solicitada: ${matricula}</small>
                </div>`;
        });
}

// Função para criar o HTML dos detalhes
function criarConteudoDetalhes(sentenciado, isExcluidos = false) {
    // Seção de destaque para data de exclusão
    const dataExclusaoDestaque = isExcluidos && sentenciado.exclusao ? `
        <div class="alert alert-danger border-danger mb-4" style="border-width: 3px !important;">
            <div class="row align-items-center">
                <div class="col-auto">
                    <i class="fas fa-exclamation-triangle fa-2x text-danger"></i>
                </div>
                <div class="col">
                    <h5 class="alert-heading mb-1 text-danger">REGISTRO EXCLUÍDO</h5>
                    <p class="mb-1"><strong>Data de Exclusão:</strong> <span class="badge bg-danger fs-6">${sentenciado.exclusao}</span></p>
                    ${sentenciado.motivo_exclusao ? `<p class="mb-0"><strong>Motivo:</strong> ${sentenciado.motivo_exclusao}</p>` : ''}
                    ${sentenciado.destino ? `<p class="mb-0"><strong>Destino:</strong> ${sentenciado.destino}</p>` : ''}
                </div>
            </div>
        </div>
    ` : '';

    return `
        ${dataExclusaoDestaque}
        <div class="row">
            <!-- Coluna da Foto -->
            <div class="col-md-4 mb-3">
                <div class="card shadow-sm">
                    <div class="card-header bg-dark text-white">
                        <i class="fas fa-camera me-2"></i>Fotografia
                    </div>
                    <div class="card-body text-center p-3">
                        <div class="d-grid gap-2">
                            <label for="inputFoto" class="btn btn-primary">
                                <i class="fas fa-upload me-2"></i>Selecionar Foto
                            </label>
                            <input type="file" id="inputFoto" accept="image/*" style="display: none;" onchange="previewFoto(event)">
                            <button class="btn btn-outline-danger" onclick="removerFoto()" id="btnRemoverFoto" style="display: none;">
                                <i class="fas fa-trash me-2"></i>Remover Foto
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Coluna das Informações -->
            <div class="col-md-8">
                <!-- Card de Informações Pessoais -->
                <div class="card shadow-sm mb-3">
                    <div class="card-header bg-primary text-white">
                        <i class="fas fa-id-card me-2"></i>Informações Pessoais
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="text-muted small mb-1">MATRÍCULA</label>
                                <div class="fw-bold fs-5">${sentenciado.matricula || 'N/A'}</div>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="text-muted small mb-1">RG</label>
                                <div class="fw-bold">${sentenciado.rg || 'N/A'}</div>
                            </div>
                            <div class="col-12 mb-3">
                                <label class="text-muted small mb-1">NOME COMPLETO</label>
                                <div class="fw-bold fs-5">${sentenciado.nome || 'N/A'}</div>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="text-muted small mb-1">DATA DE NASCIMENTO</label>
                                <div class="fw-bold">${sentenciado.nascimento || 'N/A'}</div>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="text-muted small mb-1">ALOJAMENTO/PAVILHÃO</label>
                                <div class="fw-bold">${sentenciado.alojamento || sentenciado.pavilhao || 'N/A'}</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Card de Informações Processuais -->
                <div class="card shadow-sm">
                    <div class="card-header bg-success text-white">
                        <i class="fas fa-gavel me-2"></i>Informações Processuais
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="text-muted small mb-1">DATA DE INCLUSÃO</label>
                                <div class="fw-bold">${sentenciado.inclusao || 'N/A'}</div>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="text-muted small mb-1">PROCEDÊNCIA</label>
                                <div class="fw-bold">${sentenciado.procedencia || 'N/A'}</div>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="text-muted small mb-1">PROCESSO</label>
                                <div class="fw-bold">${sentenciado.processo || 'N/A'}</div>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="text-muted small mb-1">ARTIGO</label>
                                <div class="fw-bold">${sentenciado.artigo || 'N/A'}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        ${sentenciado.observacoes ? `
        <div class="row mt-3">
            <div class="col-12">
                <div class="card shadow-sm">
                    <div class="card-header bg-warning">
                        <i class="fas fa-sticky-note me-2"></i>Observações
                    </div>
                    <div class="card-body">
                        <p class="mb-0">${sentenciado.observacoes}</p>
                    </div>
                </div>
            </div>
        </div>` : ''}
        
        <div class="alert alert-info mt-3 mb-0">
            <i class="fas fa-info-circle me-2"></i>
            <small>Estas informações estão limitadas aos dados disponibilizados pelo Siscar/SIA. Este programa ainda não possui banco de dados próprio.</small>
        </div>
    `;
}

// Função para preview da foto
function previewFoto(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const preview = document.getElementById('fotoPreview');
            preview.innerHTML = `<img src="${e.target.result}" class="img-fluid rounded" style="max-height: 100%; max-width: 100%; object-fit: contain;" alt="Foto do sentenciado">`;

            // Mostrar botão de remover
            document.getElementById('btnRemoverFoto').style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

// Função para remover foto
function removerFoto() {
    const preview = document.getElementById('fotoPreview');
    preview.innerHTML = `<img src="/static/img/default_avatar.png" class="img-fluid rounded" style="max-height: 100%; max-width: 100%; object-fit: contain;" alt="Foto padrão">`;
    document.getElementById('inputFoto').value = '';
    document.getElementById('btnRemoverFoto').style.display = 'none';
}

// Função para carregar foto do sentenciado do servidor
function carregarFotoSentenciado(matricula) {
    if (!matricula) {
        console.warn('Matrícula não fornecida para carregar foto');
        return;
    }

    const preview = document.getElementById('fotoPreview');
    if (!preview) {
        console.warn('Elemento fotoPreview não encontrado');
        return;
    }

    // Tentar carregar a foto do servidor
    // Procurar por diferentes extensões possíveis
    const extensoes = ['jpg', 'jpeg', 'png', 'gif', 'webp'];
    let fotoEncontrada = false;

    // Função para tentar carregar uma imagem
    const tentarCarregarImagem = (index) => {
        if (index >= extensoes.length) {
            // Nenhuma foto encontrada, usar padrão
            if (!fotoEncontrada) {
                preview.innerHTML = `<img src="/static/img/default_avatar.png" class="rounded" style="max-height: 100%; max-width: 100%; object-fit: contain;" alt="Foto padrão">`;
            }
            return;
        }

        const img = new Image();
        const caminhoFoto = `/static/fotos_sentenciados/${matricula}.${extensoes[index]}`;

        img.onload = function () {
            // Foto encontrada e carregada com sucesso
            fotoEncontrada = true;
            preview.innerHTML = `<img src="${caminhoFoto}" class="img-fluid rounded" style="max-height: 100%; max-width: 100%; object-fit: contain;" alt="Foto do sentenciado">`;
            console.log(`Foto carregada: ${caminhoFoto}`);
        };

        img.onerror = function () {
            // Foto não encontrada, tentar próxima extensão
            tentarCarregarImagem(index + 1);
        };

        img.src = caminhoFoto;
    };

    // Iniciar tentativa de carregamento
    tentarCarregarImagem(0);
}
