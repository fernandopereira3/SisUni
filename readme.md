# SisUni - Sistema Unificado

## Descrição
O SisUni é um sistema web completo desenvolvido especificamente para a gestão de estabelecimentos penitenciários, focado no controle de sentenciados, visitantes e atividades laborais. O sistema oferece uma interface moderna e intuitiva para gerenciar eficientemente o dia a dia de uma unidade prisional, com funcionalidades robustas de pesquisa, controle de visitas e relatórios em tempo real.

### Principais Características
- **Gestão Completa de Sentenciados**: Cadastro, pesquisa e controle de informações dos internos
- **Sistema de Visitas Inteligente**: Controle detalhado de entrada/saída com contadores automáticos
- **Dashboard em Tempo Real**: Visualização instantânea de ocupação por alojamentos
- **Controle de Trabalho**: Gestão de sentenciados aptos ao trabalho por setor
- **Relatórios Automatizados**: Geração de listas e relatórios em PDF
- **Interface Responsiva**: Funciona perfeitamente em desktop, tablet e mobile

## Índice
1. [Funcionalidades](#funcionalidades)
2. [Arquitetura](#arquitetura)
3. [Pré-requisitos](#pré-requisitos)
4. [Instalação](#instalação)
5. [Execução](#execução)
6. [Uso](#uso)
7. [Estrutura do Projeto](#estrutura-do-projeto)
8. [Contribuição](#contribuição)
9. [Licença](#licença)

## Funcionalidades Detalhadas

### 🔍 Sistema de Pesquisa Avançada
- **Busca por Matrícula**: Localização exata ou parcial por número de matrícula
- **Busca por Nome**: Pesquisa insensível a maiúsculas/minúsculas com suporte a nomes parciais
- **Filtros Combinados**: Possibilidade de usar múltiplos critérios simultaneamente
- **Resultados Instantâneos**: Interface responsiva com resultados em tempo real

### 👥 Gestão Completa de Visitantes
- **Registro de Entrada**: Sistema completo de check-in de visitantes
- **Controle Demográfico**: Contadores separados para homens, mulheres e crianças
- **Controle de Objetos**: Registro de garrafas PET e outros itens permitidos
- **Histórico de Visitas**: Armazenamento completo do histórico com data/hora
- **Edição em Tempo Real**: Possibilidade de alterar quantidades após o registro
- **Remoção de Visitas**: Sistema para cancelar visitas do dia atual

### 📊 Dashboard Inteligente
- **Ocupação por Alojamento**: Visualização em tempo real da distribuição por pavilhões (1A, 1B, 2A, 2B, 3A, 3B, 4A, 4B)
- **Totalizadores Automáticos**: Cálculo automático de ocupação total da unidade
- **Resumo de Visitas Diárias**: Contadores em tempo real de visitantes do dia
- **Estatísticas de Objetos**: Controle total de garrafas PET registradas

### 💼 Controle de Trabalho
- **Gestão por Setor**: Organização de sentenciados aptos ao trabalho por área de atuação
- **Lista de Trabalhadores**: Visualização completa dos internos em atividade laboral
- **Integração com Visitas**: Identificação automática de trabalhadores durante o registro de visitas

### 📋 Sistema de Listas e Relatórios
- **Listas Dinâmicas**: Criação automática de listas de visitantes do dia
- **Ordenação Flexível**: Organização por nome, matrícula ou outros critérios
- **Exportação PDF**: Geração de relatórios profissionais para impressão
- **Atualização em Tempo Real**: Listas sempre atualizadas com as últimas informações

### 🔐 Sistema de Autenticação
- **Login Simplificado**: Sistema de autenticação por usuário
- **Criação Automática**: Registro automático de novos usuários
- **Sessões Seguras**: Controle de sessão com chaves secretas aleatórias

### 🎨 Interface Moderna e Responsiva
- **Design Bootstrap 5**: Interface moderna e profissional
- **Responsividade Total**: Funciona perfeitamente em qualquer dispositivo
- **Navegação Intuitiva**: Menu organizado por categorias funcionais
- **Feedback Visual**: Alertas e confirmações para todas as ações
- **Ícones Informativos**: Interface rica em elementos visuais para facilitar o uso

## Arquitetura Técnica

### 🏗️ Estrutura Geral
O SisUni segue uma arquitetura modular baseada em Flask com separação clara de responsabilidades:

```
SisUni/
├── src/
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── Data/                # Camada de dados
│   │   ├── conexao.py       # Configuração MongoDB
│   │   └── Dockerfile       # Container para banco
│   ├── Routes/              # Camada de apresentação
│   │   ├── rotas.py         # Rotas principais (pesquisa, visitas)
│   │   ├── jumbo.py         # Funcionalidades especiais
│   │   ├── trabalho.py      # Gestão de trabalho
│   │   ├── debug.py         # Ferramentas de debug
│   │   ├── templates/       # Templates HTML
│   │   └── static/          # Arquivos estáticos (CSS, JS, imagens)
│   ├── Funcoes/             # Camada de negócio
│   │   └── funcoes.py       # Funções auxiliares e formulários
│   └── Tests/               # Testes automatizados
└── requirements.txt         # Dependências do projeto
```

### 🔧 Stack Tecnológico

#### Backend
- **Flask 3.1.1**: Framework web principal
- **Flask-PyMongo 3.0.1**: Integração com MongoDB
- **Flask-WTF 1.2.2**: Formulários e validação
- **PyMongo 4.13.1**: Driver oficial MongoDB
- **ReportLab 4.3.1**: Geração de relatórios PDF
- **Pandas 2.3.0**: Manipulação de dados

#### Frontend
- **Bootstrap 5.3.0**: Framework CSS responsivo
- **Bootstrap Icons**: Ícones modernos
- **Font Awesome 6.0**: Ícones complementares
- **JavaScript Vanilla**: Interatividade sem dependências externas

#### Banco de Dados
- **MongoDB**: Banco NoSQL para flexibilidade de dados
- **Coleções Principais**:
  - `sentenciados`: Dados dos internos
  - `usuarios`: Sistema de autenticação
  - `trab`: Controle de trabalho

### 🔄 Fluxo de Dados

1. **Requisição HTTP** → Flask Router (Blueprint)
2. **Validação** → Flask-WTF Forms
3. **Processamento** → Funções de Negócio
4. **Persistência** → MongoDB via PyMongo
5. **Resposta** → Template Jinja2 + JSON API

### 🎯 Padrões Arquiteturais

#### Blueprint Pattern
Cada módulo funcional é organizado como um Blueprint Flask:
- `rotas_bp`: Funcionalidades principais
- `jumbo_bp`: Funcionalidades especiais
- `debug_bp`: Ferramentas de desenvolvimento
- `trabalho_bp`: Gestão de trabalho

#### Repository Pattern
A camada `Data/conexao.py` centraliza o acesso ao banco de dados, fornecendo uma interface consistente para todas as operações.

#### Template Pattern
Utilização do sistema de templates Jinja2 para separar lógica de apresentação:
- Templates base reutilizáveis
- Componentes modulares
- Context processors para dados globais

## Pré-requisitos

### Requisitos de Sistema
- **Python 3.8+**: Linguagem principal do projeto
- **MongoDB 4.4+**: Banco de dados NoSQL
- **pip**: Gerenciador de pacotes Python
- **Git**: Controle de versão
- **4GB RAM**: Mínimo recomendado
- **1GB Espaço em Disco**: Para aplicação e dados

### Requisitos de Rede
- **Porta 5000**: Para o servidor Flask
- **Porta 27017**: Para o MongoDB (padrão)
- **Conexão com Internet**: Para CDNs do Bootstrap e ícones

## Instalação Detalhada

### 1. Preparação do Ambiente

#### Clone o Repositório
```bash
git clone https://github.com/fernandopereira3/SisUni.git
cd SisUni
```

#### Crie um Ambiente Virtual (Recomendado)
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 2. Instalação de Dependências

```bash
# Instalar todas as dependências
pip install -r requirements.txt

# Verificar instalação
pip list
```

### 3. Configuração do MongoDB

#### Instalação do MongoDB
```bash
# Ubuntu/Debian
sudo apt-get install mongodb

# CentOS/RHEL
sudo yum install mongodb

# macOS (com Homebrew)
brew install mongodb-community

# Windows: Baixar do site oficial
```

#### Inicialização do Banco
```bash
# Linux/Mac
sudo systemctl start mongod
# ou
mongod --dbpath /caminho/para/dados

# Windows
net start MongoDB
# ou executar mongod.exe
```

#### Verificação da Conexão
```bash
# Testar conexão
mongo
# Deve conectar sem erros
```

### 4. Configuração Inicial do Banco

O sistema criará automaticamente as coleções necessárias:
- `sentenciados`: Dados dos internos
- `usuarios`: Sistema de login
- `trab`: Controle de trabalho

### 5. Configuração Opcional

#### Variáveis de Ambiente (Opcional)
```bash
# Criar arquivo .env (opcional)
echo "MONGO_URI=mongodb://localhost:27017/cpppac" > .env
echo "FLASK_ENV=development" >> .env
echo "SECRET_KEY=sua_chave_secreta_aqui" >> .env
```

## Execução do Sistema

### 🚀 Modo Desenvolvimento

#### Execução Básica
```bash
# Navegar para o diretório src
cd src

# Executar o sistema
python main.py
```

#### Execução com Debug
```bash
# Com debug ativo (recomendado para desenvolvimento)
FLASK_ENV=development python main.py

# Com debug e auto-reload
FLASK_DEBUG=1 python main.py
```

#### Acesso ao Sistema
- **URL Local**: http://localhost
- **URL de Rede**: http://[IP-DO-SERVIDOR]
- **Login**: Qualquer nome de usuário (sistema cria automaticamente)

### 🏭 Modo Produção

#### Linux/Mac - Usando systemd (Recomendado)

1. **Criar arquivo de serviço**:
```bash
sudo nano /etc/systemd/system/sisuni.service
```

2. **Conteúdo do arquivo**:
```ini
[Unit]
Description=SisUni - Sistema Penitenciário
After=network.target mongodb.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/caminho/para/SisUni/src
Environment=PATH=/caminho/para/venv/bin
ExecStart=/caminho/para/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. **Ativar o serviço**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable sisuni
sudo systemctl start sisuni
sudo systemctl status sisuni
```

#### Execução via Docker Compose (Recomendado)

O projeto foi atualizado para utilizar **Docker Compose**, facilitando a orquestração dos serviços (Aplicação Web + Banco de Dados) e garantindo a persistência dos dados.

**Pré-requisitos:**
- Docker Desktop instalado e rodando.

**Como Executar:**

1. **Inicie o ambiente:**
   ```bash
   docker-compose up -d --build
   ```
   Isso irá:
   - Construir a imagem da aplicação Python (otimizada com variáveis de ambiente para evitar arquivos `.pyc` e buffering).
   - Iniciar o container do MongoDB.
   - Configurar a rede interna entre os serviços.

2. **Acesse a aplicação:**
   - Abra o navegador em: `http://localhost:80` (ou apenas `http://localhost`).

**Detalhes Técnicos da Configuração Docker:**

- **Persistência de Dados (Bind Mount):**
  O banco de dados MongoDB utiliza um **volume do tipo Bind**, o que significa que os dados são salvos diretamente em uma pasta do seu computador host, garantindo segurança e facilidade de backup.
  - *Configuração no `docker-compose.yml`:*
    ```yaml
    volumes:
      mongo_data:
        driver: local
        driver_opts:
          type: none
          o: bind
          device: /caminho/no/seu/computador/mongo_data
    ```
  - *Nota:* Certifique-se de ajustar o caminho `device` no `docker-compose.yml` para uma pasta válida no seu sistema.

- **Variáveis de Ambiente Dinâmicas:**
  A conexão com o banco de dados não é mais "chumbada" no código. O arquivo `src/Data/conexao.py` foi atualizado para ler a variável `MONGO_URI` do ambiente, permitindo flexibilidade total.
  - *No `docker-compose.yml`:*
    ```yaml
    environment:
      - MONGO_URI=mongodb://mongo:27017/cpppac
    ```

- **Otimizações Python:**
  O `Dockerfile` inclui variáveis para melhorar a performance em containers:
  - `PYTHONDONTWRITEBYTECODE=1`: Evita criação de arquivos `.pyc` desnecessários.
  - `PYTHONUNBUFFERED=1`: Garante que os logs sejam exibidos em tempo real no console do Docker.

3. **Parar o ambiente:**
   ```bash
   docker-compose down
   ```

#### Linux/Mac - Usando PM2 (Node.js)

```bash
# Instalar PM2
npm install -g pm2

# Criar arquivo ecosystem.config.js
echo 'module.exports = {
  apps: [{
    name: "sisuni",
    script: "python",
    args: "main.py",
    cwd: "./src",
    interpreter: "none",
    env: {
      FLASK_ENV: "production"
    }
  }]
}' > ecosystem.config.js

# Iniciar aplicação
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

#### Windows - Como Serviço

1. **Usando NSSM (Recomendado)**:
```powershell
# Baixar NSSM de https://nssm.cc/
# Instalar como serviço
nssm.exe install SisUni
# Configurar:
# - Path: C:\caminho\para\python.exe
# - Startup directory: C:\caminho\para\SisUni\src
# - Arguments: main.py

# Iniciar serviço
nssm.exe start SisUni
```

2. **Usando Task Scheduler**:
```powershell
# Criar tarefa agendada para inicialização
schtasks /create /tn "SisUni" /tr "python C:\caminho\para\SisUni\src\main.py" /sc onstart /ru SYSTEM
```

### 🔧 Configurações de Produção

#### Nginx (Proxy Reverso)
```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /caminho/para/SisUni/src/Routes/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### Apache (Proxy Reverso)
```apache
<VirtualHost *:80>
    ServerName seu-dominio.com
    
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
    
    Alias /static /caminho/para/SisUni/src/Routes/static
    <Directory "/caminho/para/SisUni/src/Routes/static">
        Require all granted
    </Directory>
</VirtualHost>
```

### 📊 Monitoramento

#### Verificação de Status
```bash
# Verificar se o serviço está rodando
curl -f http://localhost:5000 || echo "Serviço offline"

# Verificar logs
tail -f /var/log/sisuni/app.log

# Verificar uso de recursos
top -p $(pgrep -f "python main.py")
```

#### Logs de Sistema
```bash
# Logs do systemd
sudo journalctl -u sisuni -f

# Logs personalizados
tail -f logs/sisuni.log
```

## Manual de Uso Completo

### 🏠 Dashboard Principal

Ao acessar o sistema, você verá:

#### Painel de Alojamentos
- **Visualização em Tempo Real**: Ocupação atual de cada pavilhão (1A, 1B, 2A, 2B, 3A, 3B, 4A, 4B)
- **Total Geral**: Soma automática de todos os internos na unidade
- **Atualização Automática**: Dados sempre atualizados

#### Painel de Trabalho
- **Lista de Trabalhadores**: Sentenciados aptos ao trabalho organizados por setor
- **Scroll Automático**: Interface otimizada para listas grandes
- **Integração com Visitas**: Identificação automática durante registro de visitas

#### Painel de Visitantes
- **Resumo Diário**: Contadores em tempo real de visitantes do dia
- **Separação Demográfica**: Homens, mulheres e crianças
- **Controle de Objetos**: Contagem de garrafas PET

### 🔍 Sistema de Pesquisa

#### Pesquisa Básica
1. **Acesse**: Menu "SENTENCIADOS" → "Pesquisar"
2. **Digite**: Matrícula ou nome (parcial ou completo)
3. **Pesquise**: Clique em "PESQUISAR" ou pressione Enter
4. **Visualize**: Resultados aparecem instantaneamente

#### Dicas de Pesquisa
- **Por Matrícula**: Digite apenas números (ex: "12345")
- **Por Nome**: Digite qualquer parte do nome (ex: "João", "Silva")
- **Busca Inteligente**: Sistema ignora maiúsculas/minúsculas
- **Resultados Múltiplos**: Todos os registros correspondentes são exibidos

### 👥 Gestão de Visitas

#### Registrar Nova Visita

1. **Acesse**: Menu "VISITAS" → "Entrada/Saída"
2. **Pesquise**: Localize o sentenciado (matrícula ou nome)
3. **Preencha os Dados**:
   - **Homens**: Quantidade de visitantes masculinos
   - **Mulheres**: Quantidade de visitantes femininas
   - **Crianças**: Quantidade de menores de idade
   - **Garrafas PET**: Quantidade de garrafas trazidas
4. **Confirme**: Clique no botão de adicionar
5. **Verificação**: Sistema confirma o registro com mensagem de sucesso

#### Funcionalidades Especiais
- **Detecção de Trabalho**: Sistema identifica automaticamente se o sentenciado trabalha
- **Histórico Automático**: Cada visita é registrada com data/hora
- **Validação**: Sistema previne registros duplicados no mesmo dia

### 📋 Gerenciamento de Listas

#### Visualizar Lista do Dia

1. **Acesse**: Menu "VISITAS" → "Lista de Selecionados" (ou botão na tela principal)
2. **Visualize**: Todos os visitantes registrados no dia atual
3. **Informações Disponíveis**:
   - Nome e matrícula do sentenciado
   - Alojamento/pavilhão
   - Quantidades de visitantes por categoria
   - Horário da última visita
   - Setor de trabalho (se aplicável)

#### Editar Registros

1. **Localize**: Encontre o registro na lista
2. **Clique**: No ícone de edição (lápis)
3. **Modifique**: Altere as quantidades conforme necessário
4. **Salve**: Confirme as alterações
5. **Verificação**: Sistema atualiza automaticamente os totais

#### Remover Visitas

1. **Localize**: Encontre o registro na lista
2. **Clique**: No ícone de remoção (lixeira)
3. **Confirme**: Sistema solicita confirmação
4. **Resultado**: Visita é removida e totais atualizados

### 📊 Relatórios e Exportação

#### Gerar Relatório PDF

1. **Acesse**: Lista de visitantes do dia
2. **Clique**: No botão "Exportar PDF"
3. **Aguarde**: Sistema gera o relatório
4. **Download**: Arquivo é baixado automaticamente

#### Conteúdo do Relatório
- **Cabeçalho**: Data, unidade, totais gerais
- **Lista Completa**: Todos os visitantes organizados
- **Totalizadores**: Resumo por categoria
- **Rodapé**: Informações de controle

### 💼 Gestão de Trabalho

#### Visualizar Trabalhadores

1. **Acesse**: Menu "SENTENCIADOS" → "Trabalho"
2. **Visualize**: Lista completa de sentenciados aptos ao trabalho
3. **Informações**: Matrícula, nome e setor de atuação

#### Integração com Visitas
- **Identificação Automática**: Durante registro de visitas, sistema identifica trabalhadores
- **Destaque Visual**: Trabalhadores são destacados na interface
- **Informação Adicional**: Setor de trabalho é exibido

### 🔧 Funcionalidades Avançadas

#### Sistema Jumbo

1. **Acesse**: Menu "VISITAS" → "Jumbo"
2. **Funcionalidade**: Sistema especial para controles específicos
3. **Uso**: Conforme necessidades operacionais da unidade

#### Modo Debug

1. **Acesse**: Menu "Debug" (se disponível)
2. **Funcionalidades**: Ferramentas para administradores
3. **Cuidado**: Uso restrito a pessoal técnico

### 📱 Uso em Dispositivos Móveis

#### Interface Responsiva
- **Adaptação Automática**: Interface se ajusta ao tamanho da tela
- **Touch Friendly**: Botões otimizados para toque
- **Navegação Simplificada**: Menu colapsável em telas pequenas

#### Dicas para Mobile
- **Orientação**: Use preferencialmente em modo paisagem para tablets
- **Zoom**: Interface permite zoom sem perder funcionalidade
- **Conectividade**: Funciona offline para consultas (dados em cache)

### ⚠️ Boas Práticas

#### Segurança
- **Logout**: Sempre faça logout ao terminar o uso
- **Dados Sensíveis**: Não compartilhe informações do sistema
- **Acesso**: Use apenas em computadores/dispositivos confiáveis

#### Operacional
- **Backup Regular**: Dados são salvos automaticamente no MongoDB
- **Verificação Diária**: Confira totais ao final do expediente
- **Relatórios**: Gere relatórios diários para controle

#### Performance
- **Navegador Atualizado**: Use versões recentes do Chrome, Firefox ou Safari
- **Cache**: Limpe cache do navegador se houver problemas
- **Conexão**: Mantenha conexão estável com a internet

## Estrutura Detalhada do Projeto

### 📁 Organização de Arquivos

```
SisUni/
├── 📄 README.md                    # Documentação principal
├── 📄 requirements.txt              # Dependências Python
├── 📄 gerador_db.py                # Script para popular banco de dados
├── 📄 update.py                    # Script de atualização
├── 📄 test_trab.py                 # Testes de trabalho
├── 📄 start.ps1                    # Script de inicialização Windows
├── 📄 .gitignore                   # Arquivos ignorados pelo Git
│
└── 📂 src/                         # Código fonte principal
    ├── 📄 main.py                  # Ponto de entrada da aplicação
    │
    ├── 📂 Data/                    # Camada de dados
    │   ├── 📄 conexao.py           # Configuração MongoDB
    │   ├── 📄 Dockerfile           # Container para banco
    │   └── 📄 import.sh            # Script de importação
    │
    ├── 📂 Funcoes/                 # Camada de negócio
    │   └── 📄 funcoes.py           # Funções auxiliares e formulários
    │
    ├── 📂 Routes/                  # Camada de apresentação
    │   ├── 📄 rotas.py             # Rotas principais (pesquisa, visitas)
    │   ├── 📄 rotas_saida.py       # Rotas de saída
    │   ├── 📄 jumbo.py             # Funcionalidades especiais
    │   ├── 📄 trabalho.py          # Gestão de trabalho
    │   ├── 📄 debug.py             # Ferramentas de debug
    │   ├── 📄 tests.py             # Testes das rotas
    │   │
    │   ├── 📂 templates/           # Templates HTML
    │   │   ├── 📄 index.html       # Dashboard principal
    │   │   ├── 📄 login.html       # Tela de login
    │   │   ├── 📄 pesquisa.html    # Pesquisa de sentenciados
    │   │   ├── 📄 entrada_saida.html # Controle de visitas
    │   │   ├── 📄 lista.html       # Lista de visitantes
    │   │   ├── 📄 trabalho.html    # Gestão de trabalho
    │   │   ├── 📄 jumbo.html       # Funcionalidades especiais
    │   │   ├── 📄 saida.html       # Controle de saída
    │   │   └── 📄 debug.html       # Interface de debug
    │   │
    │   └── 📂 static/              # Arquivos estáticos
    │       ├── 📂 css/             # Estilos CSS
    │       ├── 📂 js/              # Scripts JavaScript
    │       └── 📂 img/             # Imagens e ícones
    │
    └── 📂 Tests/                   # Testes automatizados
        └── 📄 test_trab.py         # Testes específicos
```

### 🔧 Descrição dos Componentes

#### 📄 Arquivos Principais

- **`main.py`**: Ponto de entrada da aplicação Flask
  - Configuração do servidor
  - Registro de Blueprints
  - Configuração de segurança

- **`requirements.txt`**: Lista todas as dependências Python necessárias
  - Flask e extensões
  - MongoDB drivers
  - Bibliotecas de relatórios
  - Ferramentas de desenvolvimento

#### 📂 Camada de Dados (`Data/`)

- **`conexao.py`**: Gerenciamento de conexão com MongoDB
  - Configuração de URI
  - Pool de conexões
  - Tratamento de erros

- **`Dockerfile`**: Containerização do banco de dados
  - Configuração MongoDB
  - Volumes persistentes
  - Rede interna

#### 📂 Camada de Negócio (`Funcoes/`)

- **`funcoes.py`**: Lógica de negócio centralizada
  - Formulários WTF
  - Funções de pesquisa
  - Geração de relatórios
  - Cálculos estatísticos

#### 📂 Camada de Apresentação (`Routes/`)

- **`rotas.py`**: Rotas principais do sistema
  - Autenticação
  - Pesquisa de sentenciados
  - Controle de visitas
  - Geração de listas

- **`trabalho.py`**: Gestão de trabalho
  - Lista de trabalhadores
  - Setores de atuação
  - Integração com visitas

- **`jumbo.py`**: Funcionalidades especiais
  - Controles específicos
  - Operações em lote

- **`debug.py`**: Ferramentas de desenvolvimento
  - Logs do sistema
  - Estatísticas de performance
  - Diagnósticos

#### 📂 Templates HTML (`templates/`)

Cada template segue o padrão:
- **Base responsiva**: Bootstrap 5
- **Componentes reutilizáveis**: Navegação, formulários
- **JavaScript integrado**: Interatividade sem dependências externas
- **Acessibilidade**: Suporte a leitores de tela

#### 📂 Arquivos Estáticos (`static/`)

- **CSS**: Estilos customizados complementando Bootstrap
- **JavaScript**: Funcionalidades interativas
- **Imagens**: Logos, ícones e recursos visuais

### 🗄️ Estrutura do Banco de Dados

#### Coleção `sentenciados`
```javascript
{
  "_id": ObjectId,
  "matricula": "12345",
  "nome": "Nome do Sentenciado",
  "pavilhao": "1A",
  "alojamento": "1A",
  "visitas": [Date, Date, ...],
  "marcadores": [garrafas, homens, mulheres, criancas]
}
```

#### Coleção `usuarios`
```javascript
{
  "_id": ObjectId,
  "username": "usuario",
  "created_at": Date
}
```

#### Coleção `trab`
```javascript
{
  "_id": ObjectId,
  "matricula": "12345",
  "nome": "Nome do Trabalhador",
  "setor": "Cozinha"
}
```

### 🔄 Fluxo de Dados

1. **Requisição HTTP** → Flask Router
2. **Autenticação** → Session Management
3. **Validação** → WTF Forms
4. **Processamento** → Business Logic
5. **Persistência** → MongoDB
6. **Resposta** → Jinja2 Templates
7. **Cliente** → HTML + CSS + JS

## Como o Sistema Funciona

### 🔄 Fluxo Operacional Completo

#### 1. Inicialização do Sistema
```python
# main.py - Ponto de entrada
app = Flask(__name__)
# Registro de Blueprints modulares
app.register_blueprint(BPjumbo)    # Funcionalidades especiais
app.register_blueprint(BProtas)    # Rotas principais
app.register_blueprint(BPdebug)    # Ferramentas debug
app.register_blueprint(BPtrabalho) # Gestão trabalho
```

#### 2. Conexão com Banco de Dados
```python
# Data/conexao.py
def conexao():
    mongo = PyMongo(app)
    db = mongo.db  # Conecta ao MongoDB 'cpppac'
    return db
```

#### 3. Autenticação Simplificada
```python
# Sistema de login automático
@rotas_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username'].lower().replace(' ', '')
    user = db.usuarios.find_one({'username': username})
    if not user:
        # Cria usuário automaticamente se não existir
        db.usuarios.insert_one({'username': username})
    session['user'] = username
```

#### 4. Pesquisa Inteligente
```python
# Busca por matrícula ou nome com regex
if matricula:
    query['matricula'] = {
        '$regex': f'^\\s*{re.escape(matricula)}\\s*',
        '$options': 'i'  # Case insensitive
    }
if nome:
    query['nome'] = {'$regex': nome, '$options': 'i'}
```

#### 5. Registro de Visitas
```python
# Atualização atômica no MongoDB
resultado = db.sentenciados.update_one(
    {'matricula': matricula},
    {
        '$push': {'visitas': datetime.datetime.now()},
        '$set': {'marcadores': [garrafas, homens, mulheres, criancas]}
    }
)
```

#### 6. Dashboard em Tempo Real
```python
# Agregação MongoDB para estatísticas
pipeline = [
    {'$match': {
        'visitas': {
            '$elemMatch': {'$gte': hoje_inicio, '$lte': hoje_fim}
        }
    }},
    {'$project': {'matricula': 1, 'marcadores': 1}}
]
documentos_hoje = list(db.sentenciados.aggregate(pipeline))
```

### 🎯 Funcionalidades Técnicas Avançadas

#### Context Processors
```python
# Injeção automática de dados em templates
@rotas_bp.context_processor
def inject_tabela_trabalho():
    documentos = list(db.trab.find({}))
    tabela_html = construir_tabela_trabalho(documentos)
    return {'tab_trabalho': tabela_html}
```

#### Geração Dinâmica de HTML
```python
# Construção de tabelas responsivas
def construir_tabela(query=None, incluir_acoes=True):
    documentos = list(db.sentenciados.find(query).sort('nome', 1))
    # Gera HTML Bootstrap dinamicamente
    html = f'<table class="table table-striped">...</table>'
    return html
```

#### API RESTful
```python
# Endpoints JSON para AJAX
@rotas_bp.route('/api/lista_dados', methods=['GET'])
def api_lista_dados():
    # Retorna dados em JSON para atualização dinâmica
    return jsonify({'status': 'success', 'documentos': documentos})
```

### 🔐 Segurança e Performance

#### Validação de Dados
```python
# Flask-WTF para validação segura
class PesquisaForm(FlaskForm):
    matricula = StringField('Matrícula')
    nome = StringField('Nome')
    pesquisar = SubmitField('PESQUISAR')
```

#### Sessões Seguras
```python
# Chave secreta aleatória
secret_key = os.urandom(24)
app.config['SECRET_KEY'] = secret_key
```

#### Otimização de Consultas
```python
# Índices MongoDB para performance
# Busca otimizada com projeção
documentos = db.sentenciados.find(query, {'_id': 0}).sort('nome', 1)
```

### 📊 Sistema de Relatórios

#### Geração PDF com ReportLab
```python
# Criação de relatórios profissionais
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter

# Estrutura de dados → PDF formatado
doc = SimpleDocTemplate(buffer, pagesize=letter)
table = Table(data)
table.setStyle(TableStyle([...]))
```

### 🔄 Integração Frontend-Backend

#### Templates Jinja2
```html
<!-- Dados dinâmicos do backend -->
<h3>{{ totals.aloj_1a|default(0) }}</h3>
{{ tab_trabalho|safe }}
{{ resumo.total_visitantes }}
```

#### JavaScript Interativo
```javascript
// AJAX para atualizações sem reload
fetch('/api/lista_dados')
    .then(response => response.json())
    .then(data => {
        // Atualiza interface dinamicamente
        updateTable(data.documentos);
    });
```

### 🏗️ Padrões de Design Implementados

#### Blueprint Pattern
- **Modularização**: Cada funcionalidade em blueprint separado
- **Reutilização**: Templates e funções compartilhadas
- **Manutenibilidade**: Código organizado por responsabilidade

#### Repository Pattern
- **Abstração**: Camada de dados isolada
- **Testabilidade**: Fácil mock para testes
- **Flexibilidade**: Troca de banco sem impacto

#### MVC Architecture
- **Model**: MongoDB + PyMongo
- **View**: Jinja2 Templates + Bootstrap
- **Controller**: Flask Routes + Business Logic

## 🤝 Contribuição

### Como Contribuir

1. **Fork do Repositório**
   ```bash
   git clone https://github.com/seu-usuario/SisUni.git
   cd SisUni
   ```

2. **Criar Branch de Feature**
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```

3. **Desenvolvimento**
   - Siga os padrões de código existentes
   - Adicione testes para novas funcionalidades
   - Documente mudanças significativas

4. **Commit e Push**
   ```bash
   git commit -m "feat: adiciona nova funcionalidade X"
   git push origin feature/nova-funcionalidade
   ```

5. **Pull Request**
   - Descreva as mudanças detalhadamente
   - Inclua screenshots se aplicável
   - Referencie issues relacionadas

### 📋 Diretrizes de Desenvolvimento

#### Padrões de Código
- **Python**: PEP 8
- **HTML**: Semântico e acessível
- **CSS**: BEM methodology
- **JavaScript**: ES6+ features

#### Estrutura de Commits
```
feat: nova funcionalidade
fix: correção de bug
docs: atualização de documentação
style: formatação de código
refactor: refatoração
test: adição de testes
chore: tarefas de manutenção
```

#### Testes
```bash
# Executar testes
python -m pytest src/Tests/

# Cobertura de código
pip install coverage
coverage run -m pytest
coverage report
```

### 🐛 Reportar Bugs

1. **Verificar Issues Existentes**: Evite duplicatas
2. **Informações Necessárias**:
   - Versão do Python
   - Sistema operacional
   - Passos para reproduzir
   - Logs de erro
   - Screenshots (se aplicável)

### 💡 Sugerir Melhorias

- **Funcionalidades**: Descreva o caso de uso
- **Performance**: Inclua benchmarks
- **UX/UI**: Mockups ou wireframes
- **Segurança**: Análise de riscos

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

### Resumo da Licença MIT

✅ **Permitido**:
- Uso comercial
- Modificação
- Distribuição
- Uso privado

❌ **Limitações**:
- Responsabilidade
- Garantia

📋 **Condições**:
- Incluir aviso de copyright
- Incluir texto da licença

---

**Desenvolvido com ❤️ para gestão penitenciária eficiente**

*Para suporte técnico ou dúvidas, abra uma issue no repositório.*