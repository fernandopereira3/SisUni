// folgas.js - JavaScript para a página de agendamento de folgas

// Função para obter o token CSRF
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Função para fazer requisições com CSRF
function fetchWithCSRF(url, options = {}) {
    options.headers = options.headers || {};
    options.headers['X-CSRFToken'] = getCSRFToken();
    return fetch(url, options);
}

let currentDate = new Date();
let selectedDate = null;
let folgasData = [];
let todasFolgasData = {}; // Para armazenar folgas de todos os usuários

// Inicializar calendário
document.addEventListener('DOMContentLoaded', async function () {
    // Carregar dados de folgas do elemento script
    const folgasDataElement = document.getElementById('folgas-data');
    if (folgasDataElement) {
        folgasData = JSON.parse(folgasDataElement.textContent || '[]');
    }

    await carregarFolgasDoMes();
    renderCalendar();

    // Event listener para o formulário
    const formFolga = document.getElementById('formFolga');
    if (formFolga) {
        formFolga.addEventListener('submit', function (e) {
            e.preventDefault();
            agendarFolga();
        });
    }

    // Event listener para botões de cancelar folga
    document.addEventListener('click', function (e) {
        if (e.target.closest('.btn-cancelar-folga')) {
            const button = e.target.closest('.btn-cancelar-folga');
            const dataFolga = button.getAttribute('data-folga-data');
            cancelarFolga(dataFolga);
        }
    });
});

// Função para carregar folgas de todos os usuários do mês
async function carregarFolgasDoMes() {
    try {
        const ano = currentDate.getFullYear();
        const mes = currentDate.getMonth() + 1;

        const response = await fetch(`/api/folgas_mes?ano=${ano}&mes=${mes}`);
        const data = await response.json();

        if (data.status === 'success') {
            // Organizar folgas por data
            todasFolgasData = {};
            data.folgas.forEach(folga => {
                if (!todasFolgasData[folga.data]) {
                    todasFolgasData[folga.data] = [];
                }
                todasFolgasData[folga.data].push(folga);
            });
        } else {
            console.error('Erro na resposta da API:', data);
        }
    } catch (error) {
        console.error('Erro ao carregar folgas do mês:', error);
    }
}

function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    // Atualizar título do mês
    const monthNames = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ];
    document.getElementById('currentMonth').textContent = `${monthNames[month]} ${year}`;

    // Primeiro dia do mês e último dia
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDate = new Date(firstDay);
    startDate.setDate(startDate.getDate() - firstDay.getDay());

    const calendarDays = document.getElementById('calendar-days');
    calendarDays.innerHTML = '';

    // Gerar semanas (máximo 6 semanas)
    for (let week = 0; week < 6; week++) {
        const weekRow = document.createElement('tr');

        for (let day = 0; day < 7; day++) {
            const date = new Date(startDate);
            date.setDate(startDate.getDate() + (week * 7) + day);

            const dayCell = document.createElement('td');
            dayCell.className = 'text-center p-2';
            dayCell.style.cursor = 'pointer';
            dayCell.style.height = '60px';
            dayCell.onclick = () => selectDate(date);

            // Verificar se é do mês atual
            if (date.getMonth() !== month) {
                dayCell.classList.add('text-muted', 'bg-light');
            }

            // Verificar se há pessoas de folga neste dia
            const currentDateStr = date.toISOString().split('T')[0];
            const pessoasDefolga = todasFolgasData[currentDateStr] || [];

            let folgasHtml = '';
            if (pessoasDefolga.length > 0) {
                folgasHtml = pessoasDefolga.map(f => {
                    const statusClass = f.status === 'aprovada' ? 'text-success' : 'text-warning';
                    const statusIcon = f.status === 'aprovada' ? '✓' : '⏳';
                    return `<small class="d-block text-truncate ${statusClass}" title="${f.nome_completo} (${f.status})">${statusIcon} ${f.nome_completo}</small>`;
                }).join('');

                // Adicionar cor de fundo suave para dias com folgas
                dayCell.classList.add('bg-light', 'border-success');
            }

            dayCell.innerHTML = `
                <div class="calendar-day-number">${date.getDate()}</div>
                <div class="folgas-list">${folgasHtml}</div>
            `;

            weekRow.appendChild(dayCell);
        }

        calendarDays.appendChild(weekRow);

        // Parar se já passou do mês atual
        if (week > 0 && new Date(startDate.getTime() + (week * 7 + 6) * 24 * 60 * 60 * 1000).getMonth() !== month) {
            break;
        }
    }
}

function selectDate(date) {
    // Remover seleção anterior
    document.querySelectorAll('td.table-primary').forEach(el => {
        el.classList.remove('table-primary');
    });

    // Selecionar nova data
    event.target.closest('td').classList.add('table-primary');
    selectedDate = date;

    // Atualizar campo de data
    const dateStr = date.toISOString().split('T')[0];
    document.getElementById('dataFolga').value = dateStr;
}

async function previousMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    await carregarFolgasDoMes();
    renderCalendar();
}

async function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    await carregarFolgasDoMes();
    renderCalendar();
}

function agendarFolga() {
    const data = document.getElementById('dataFolga').value;
    const motivo = document.getElementById('motivoFolga').value;

    if (!data) {
        alert('Por favor, selecione uma data.');
        return;
    }

    // Verificar se a data não é no passado
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    const dataFolga = new Date(data);

    if (dataFolga < hoje) {
        alert('Não é possível agendar folga para datas passadas.');
        return;
    }

    const dados = {
        data: data,
        motivo: motivo
    };

    fetchWithCSRF('/api/agendar_folga', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dados)
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Folga agendada com sucesso!');
                location.reload(); // Recarregar página para atualizar a lista
            } else {
                alert('Erro: ' + data.message);
            }
        })
        .catch(error => {
            alert('Erro de conexão: ' + error.message);
        });
}

function cancelarFolga(dataFolga) {
    if (!confirm('Tem certeza que deseja cancelar esta folga?')) {
        return;
    }

    fetchWithCSRF('/api/cancelar_folga', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: dataFolga })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Folga cancelada com sucesso!');
                location.reload(); // Recarregar página para atualizar a lista
            } else {
                alert('Erro: ' + data.message);
            }
        })
        .catch(error => {
            alert('Erro de conexão: ' + error.message);
        });
}

function abrirModalAprovacao() {
    // Buscar folgas pendentes
    carregarFolgasPendentes();
    const modal = new bootstrap.Modal(document.getElementById('modalAprovacao'));
    modal.show();
}

async function carregarFolgasPendentes() {
    try {
        console.log('Carregando folgas pendentes...');
        const response = await fetch('/api/folgas_pendentes');
        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Data received:', data);

        if (data.status === 'success') {
            const lista = document.getElementById('listaFolgasPendentes');
            lista.innerHTML = '';

            if (data.folgas.length === 0) {
                lista.innerHTML = '<p class="text-muted">Nenhuma folga pendente para aprovação.</p>';
                return;
            }

            data.folgas.forEach(folga => {
                const item = document.createElement('div');
                item.className = 'card mb-2';
                item.innerHTML = `
                    <div class="card-body p-2">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <strong>${folga.nome_completo}</strong><br>
                                <small class="text-muted">Data: ${folga.data}</small><br>
                                ${folga.motivo ? `<small>Motivo: ${folga.motivo}</small>` : ''}
                            </div>
                            <button class="btn btn-success btn-sm" onclick="aprovarFolga('${folga.username}', '${folga.data}')">
                                <i class="fas fa-check"></i> Aprovar
                            </button>
                        </div>
                    </div>
                `;
                lista.appendChild(item);
            });
        } else {
            console.error('Erro ao carregar folgas pendentes:', data.message);
            const lista = document.getElementById('listaFolgasPendentes');
            lista.innerHTML = '<p class="text-danger">Erro: ' + data.message + '</p>';
        }
    } catch (error) {
        console.error('Erro de conexão:', error);
        const lista = document.getElementById('listaFolgasPendentes');
        lista.innerHTML = '<p class="text-danger">Erro de conexão: ' + error.message + '</p>';
    }
}

async function aprovarFolga(username, data) {
    try {
        const response = await fetchWithCSRF('/api/aprovar_folga', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                data: data
            })
        });

        const result = await response.json();

        if (result.status === 'success') {
            alert('Folga aprovada com sucesso!');
            carregarFolgasPendentes(); // Recarregar lista
            carregarFolgasDoMes(); // Atualizar calendário
            renderCalendar();
        } else {
            alert('Erro: ' + result.message);
        }
    } catch (error) {
        alert('Erro de conexão: ' + error.message);
    }
}

// Função para abrir modal de agendar para funcionário
function abrirModalAgendarFuncionario() {
    const modal = new bootstrap.Modal(document.getElementById('modalAgendarFuncionario'));
    modal.show();
}

// Função para agendar folga para funcionário
async function agendarFolgaFuncionario() {
    const username = document.getElementById('usernameFuncionario').value.trim();
    const dataFolga = document.getElementById('dataFolgaFuncionario').value;
    const motivo = document.getElementById('motivoFolgaFuncionario').value.trim();
    const acao = document.querySelector('input[name="acaoFuncionario"]:checked').value;

    // Validação baseada na ação
    if (!username || !dataFolga) {
        alert('Por favor, preencha o username e a data.');
        return;
    }

    if (acao === 'criar' && !motivo) {
        alert('Por favor, preencha o motivo para criar uma nova folga.');
        return;
    }

    try {
        const response = await fetchWithCSRF('/api/editar_folga', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                data_antiga: dataFolga, // Para criar, usamos a mesma data
                data_nova: dataFolga,
                motivo: motivo,
                acao: acao
            })
        });

        const result = await response.json();

        if (result.status === 'success') {
            const mensagem = acao === 'criar' ? 'Folga agendada com sucesso para o funcionário!' : 'Folga removida com sucesso!';
            alert(mensagem);

            // Limpar formulário
            document.getElementById('usernameFuncionario').value = '';
            document.getElementById('dataFolgaFuncionario').value = '';
            document.getElementById('motivoFolgaFuncionario').value = '';
            document.getElementById('acaoCriar').checked = true;

            // Fechar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalAgendarFuncionario'));
            modal.hide();

            // Atualizar calendário
            await carregarFolgasDoMes();
            renderCalendar();
        } else {
            alert('Erro: ' + result.message);
        }
    } catch (error) {
        alert('Erro de conexão: ' + error.message);
    }
}
