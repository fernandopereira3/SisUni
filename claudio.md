# SisUni — Sistema de Gestão Penitenciária (CPPPAC)

Sistema web Flask para gestão interna de uma unidade penitenciária. Gerencia sentenciados, visitas, trabalho, frequência, funcionários e folgas.

## Stack

- **Backend**: Python 3.13 + Flask
- **Banco principal**: MongoDB (coleção `cpppac`) via PyMongo
- **Banco secundário**: MySQL (`siscar`) via SQLAlchemy — fonte de dados para sync
- **Frontend**: Jinja2 + Bootstrap 5 + JS vanilla
- **Deploy**: Docker Compose (`fernandopereira3/sisuni:latest`)
- **Scheduler**: APScheduler — sync automático MySQL→MongoDB às 06h, 12h e 18h

## Estrutura do projeto

```
src/
├── main.py                  # Entry point, registra blueprints e scheduler
├── Data/
│   └── conexao.py           # Singleton MongoClient + SQLAlchemy engine
├── Funcoes/
│   ├── funcoes.py           # Helpers: PesquisaForm, construir_tabela, resumo_visitas
│   └── exportar_banco.py    # Lógica de sync MySQL → MongoDB
├── Routes/
│   ├── rotas.py             # Core: login, index, entrada_saida, lista, download PDF
│   ├── debug.py             # Admin: stats, visualização de coleções, sync manual
│   ├── administrativo/
│   │   └── rh.py            # Gestão de funcionários (CRUD usuários)
│   ├── seguranca/
│   │   └── folgas.py        # Agendamento e aprovação de folgas
│   ├── sentenciados/
│   │   ├── pesquisas.py     # Pesquisa por nome/matrícula, histórico de visitas por data
│   │   └── visitas.py       # Jumbo (rol de visitas diário + PDF)
│   ├── producao/
│   │   ├── trabalho.py      # Gestão de trabalho dos sentenciados
│   │   └── frequencia.py    # Frequência/entrada-saída de trabalho
│   └── simic/
│       └── simic.py         # Cadastro SIMIC (ficha completa do sentenciado)
└── Tests/
    └── test.py
```

## Conexão com banco

`src/Data/conexao.py` exporta um **singleton** — um único `MongoClient` compartilhado por todos os módulos:

```python
from Data.conexao import cpppac          # função que retorna o db
from Data.conexao import conexao_mongo   # alias (mesma coisa)
from Data.conexao import conexao_sql     # SQLAlchemy engine para MySQL

db = cpppac()   # retorna sempre o mesmo objeto _db
```

Nunca criar `MongoClient` direto nos módulos — usar sempre `cpppac()` ou `conexao_mongo()`.

## Coleções MongoDB

| Coleção | Conteúdo |
|---|---|
| `sentenciados` | Ficha completa (sincronizada do MySQL siscar) |
| `excluidos` | Sentenciados transferidos/liberados |
| `usuarios` | Funcionários da unidade (login, setor, lvl, folgas) |
| `trab` | Alocação de trabalho dos sentenciados |
| `visitas` | Histórico permanente de visitas (jumbo) |
| `aux` | Dados auxiliares |

## Sistema de usuários

Cada usuário tem `setor` e `lvl` (nível de acesso):

| setor | Acesso |
|---|---|
| `cpd` | Admin geral — acesso a tudo |
| `simic` | Cadastro SIMIC |
| `administrativo` / `rh` | Gestão de funcionários |
| qualquer | Folgas, pesquisas, visitas |

Senhas de usuários `lvl=10` ou `lvl=0` são hasheadas com **bcrypt**.

## Controle de acesso por rota

Cada blueprint tem uma função `verificar_acesso_<setor>()`. Padrão:

```python
def verificar_acesso_simic():
    if "user" not in session:
        abort(403)
    usuario = cpppac.usuarios.find_one({"username": session["user"]})
    setor = str(usuario.get("setor", "")).strip().lower()
    if setor not in ("cpd", "simic"):
        abort(403)
```

## Sync MySQL → MongoDB

`Funcoes/exportar_banco.py` — função `sincronizar()`:
- Lê tabelas do MySQL `siscar` (sentenciados, trabalho, etc.)
- Upsert no MongoDB preservando dados de visitas e anotações locais
- Chamada automaticamente pelo scheduler e manualmente via `/debug/sincronizar`

## Deploy

```bash
docker compose up -d
```

Variáveis de ambiente (no compose):
- `MONGO_URI` — ex: `mongodb://mongo:27017/`
- `MYSQL_URI` — ex: `mysql+mysqlconnector://user:pass@host:port/siscar`

## Regras importantes

- Nunca criar `MongoClient` fora de `conexao.py`
- `global df_visitas` deve ficar no topo da função, não dentro de blocos `if`
- CSS e templates ficam em `src/Routes/static/` e `src/Routes/templates/`
- Não adicionar Co-Authored-By nos commits
- Commits e pushes só quando o usuário pedir explicitamente
