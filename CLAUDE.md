# SisUni — Sistema de Gestão Penitenciária (CPPPAC)

Sistema web Flask para gestão interna de uma unidade penitenciária. Gerencia sentenciados, visitas, trabalho, frequência, funcionários e folgas.

---

# ⚠️ REGRAS ABSOLUTAS — LER ANTES DE QUALQUER COISA

## 🚫 NUNCA FAÇA COMMITS OU PUSH — SÓ O USUÁRIO FAZ

**NÃO** execute `git commit`, `git push`, `git push --force` ou qualquer variante.
O usuário faz todos os commits e pushes manualmente. Sempre.
Se o usuário não pedir explicitamente, não commite. Se pedir, avise antes de executar.

## 🚫 NUNCA adicione Co-Authored-By nos commits

Não incluir `Co-Authored-By: Claude ...` em nenhuma mensagem de commit.

---

## Stack

- **Backend**: Python 3.13 + Flask
- **Banco principal**: MongoDB (database `cpppac`) via PyMongo
- **Banco secundário**: MySQL (`siscar`) via SQLAlchemy — fonte de dados para sync
- **Frontend**: Jinja2 + Bootstrap 5 + JS vanilla (sem frameworks JS)
- **Deploy**: Docker Compose (`fernandopereira3/sisuni:latest`)
- **Scheduler**: APScheduler — sync automático MySQL→MongoDB às 06h, 12h e 18h

## Estrutura do projeto

```
src/
├── main.py                      # Entry point — blueprints + scheduler
├── Data/
│   └── conexao.py               # Singleton MongoClient + SQLAlchemy engine
├── Funcoes/
│   ├── funcoes.py               # PesquisaForm, construir_tabela, resumo_visitas
│   └── exportar_banco.py        # Sync MySQL → MongoDB
├── Routes/
│   ├── rotas.py                 # Core: login, index, entrada_saida, lista, download PDF
│   ├── debug.py                 # Admin: stats, coleções, sync manual, export/import ZIP
│   ├── administrativo/
│   │   └── rh.py                # CRUD de funcionários (setor: cpd/administrativo/rh)
│   ├── seguranca/
│   │   └── folgas.py            # Agendamento e aprovação de folgas
│   ├── sentenciados/
│   │   ├── pesquisas.py         # Pesquisa sentenciados + histórico visitas por data
│   │   └── visitas.py           # Jumbo — rol de visitas diário + PDF
│   ├── producao/
│   │   ├── trabalho.py          # Gestão de trabalho dos sentenciados
│   │   └── frequencia.py        # Frequência/entrada-saída de trabalho
│   └── simic/
│       └── simic.py             # Cadastro SIMIC (setor: cpd/simic)
└── Tests/
    └── test.py
```

## Conexão com banco

`src/Data/conexao.py` usa **singleton** — um único `MongoClient` compartilhado:

```python
from Data.conexao import cpppac        # função → retorna _db
from Data.conexao import conexao_mongo # alias de cpppac
from Data.conexao import conexao_sql   # cria SQLAlchemy engine para MySQL
from Data.conexao import MONGO_URI, MONGO_DB, MYSQL_URI  # constantes

db = cpppac()  # todos os módulos recebem o mesmo objeto _db
```

**Nunca** instanciar `MongoClient()` fora de `conexao.py`. Cada módulo chama `cpppac()` no nível do módulo:

```python
from Data.conexao import cpppac
cpppac = cpppac()  # reatribui a variável para o objeto db
```

## Coleções MongoDB

| Coleção | Conteúdo |
|---|---|
| `sentenciados` | Ficha completa — sincronizada do MySQL `siscar`. **Somente leitura no fluxo de visitas.** |
| `excluidos` | Sentenciados transferidos ou liberados |
| `usuarios` | Funcionários: login, setor, lvl, folgas[] |
| `trab` | Alocação de trabalho dos sentenciados |
| `visitas_dia` | Registro de visitas do dia (ver abaixo) |
| `visitas` | Histórico permanente de visitas do Jumbo |
| `aux` | Dados auxiliares |

## Coleção `visitas_dia` — IMPORTANTE

**Toda a lógica de visitas diárias usa `visitas_dia`, não `sentenciados`.**

A coleção `sentenciados` não é modificada pelo fluxo de entrada/saída de visitas — ela só recebe dados do sync MySQL.

**Um documento por matrícula por dia.** `data_visita` é um **array** de timestamps — cada vez que a mesma matrícula é adicionada no dia, um novo timestamp é `$push`ado ao array.

Estrutura do documento em `visitas_dia`:
```json
{
  "matricula": "12345",
  "nome": "FULANO DE TAL",
  "pavilhao": "1A",
  "garrafas": 0,
  "homens": 1,
  "mulheres": 0,
  "criancas": 0,
  "data_visita": [ISODate("10:30"), ISODate("14:00")]
}
```

Query para buscar visitas de um período usa `$elemMatch`:
```python
{"data_visita": {"$elemMatch": {"$gte": inicio, "$lte": fim}}}
```

Lógica de `adicionar_lista`: se já existe doc para essa matrícula hoje → `$push` no array + `$set` marcadores. Se não existe → `insert_one` com array `[datetime.now()]`.

Mapeamento das rotas para `visitas_dia`:

| Rota | Operação |
|---|---|
| `POST /adicionar/<matricula>` | find → update (`$push`) ou insert |
| `DELETE /remover_visita_hoje/<matricula>` | `delete_one` com `$elemMatch` |
| `PUT /editar_marcadores/<matricula>` | `update_one` com `$elemMatch` |
| `GET /lista` | `find` com `$elemMatch` |
| `GET /api/lista_dados` | `find` com `$elemMatch` |
| `GET /download` (PDF) | `find` com `$elemMatch` |
| `GET /pesquisas/dia-de-visita` | `find` com `$elemMatch` por data |
| `resumo_visitas()` | `find` com `$elemMatch` |

Helpers em `rotas.py`:
```python
def _hoje():                        # retorna (inicio, fim) do dia atual
def _lista_visitas_dia(inicio, fim): # find + formata data_visita como última string
```

## `construir_tabela()` — parâmetro `modo`

A função `construir_tabela` em `funcoes.py` tem o parâmetro `modo`:

- `modo="detalhes"` (padrão) → botão **Detalhes** (abre modal com dados do sync)
- `modo="adicionar"` → `<td>` vazio — o JS de `entrada_saida.js` adiciona o botão **Adicionar**

Usar sempre `modo="adicionar"` quando chamar de `entrada_saida`:
```python
resultados = construir_tabela(query=query, incluir_acoes=True, modo="adicionar")
```

## Sistema de usuários (`cpppac.usuarios`)

Cada usuário tem `setor` (string) e `lvl` (string):

| setor | Acesso liberado |
|---|---|
| `cpd` | Tudo — admin geral |
| `simic` | Cadastro SIMIC (`/simic`) |
| `administrativo` / `rh` | Gestão de funcionários |
| `seguranca` | Folgas (qualquer logado pode ver as próprias) |
| qualquer | Pesquisas, visitas, entrada/saída |

Senhas de `lvl=10` ou `lvl=0` são hasheadas com **bcrypt** e salvas em `lvl10_password`.

## Padrão de controle de acesso

Cada blueprint tem `verificar_acesso_<setor>()`. Usa `session["user"]` para buscar o usuário e checar `setor`:

```python
def verificar_acesso_simic():
    if "user" not in session:
        abort(403)
    usuario = cpppac.usuarios.find_one({"username": session["user"]})
    if not usuario:
        abort(403)
    setor = str(usuario.get("setor", "")).strip().lower()
    if setor not in ("cpd", "simic"):
        abort(403)
```

## Sync MySQL → MongoDB

`Funcoes/exportar_banco.py` — função `sincronizar()`:
- Conecta no MySQL `siscar` via `conexao_sql()`
- Lê sentenciados, trabalho, excluídos etc.
- Faz upsert no MongoDB **somente nas coleções de cadastro** (sentenciados, trab, excluidos)
- Roda automaticamente pelo scheduler (06h, 12h, 18h)
- Pode ser chamada manualmente via `/debug/sincronizar`
- O modal de detalhes em `pesquisa.html` mostra os campos sincronizados (artigo, pena, regime, tatuagens, família etc.)

## Export/Import de banco (debug)

`GET /debug/banco/export` → baixa `sisuni_backup_DD-MM-YYYY_HH-MM.zip` com todas as coleções como JSON.

`GET /POST /debug/banco/import` → restaura a partir do ZIP (apaga e reimporta cada coleção).

## Modal de detalhes (pesquisa.html)

O modal tem 4 abas com campos vindos do sync MySQL:

| Aba | Campos principais |
|---|---|
| Pessoal | matricula, nome, vulgo, rg, cpf, nascimento, naturalidade, pavilhao, cela |
| Judicial | regime, reincidente, hediondo, artigo, deecrim, pena (anos/meses/dias), prisao |
| Físico | cutis, cabelos, olhos, estatura, peso, tatuagens, cicatrizes |
| Família | pai, mae, esposa, estado_civil, filhos, endereco_familiar, contato |

## Formulário SIMIC (novo cadastro)

`simic.html` — "Novo Cadastro" usa os **mesmos nomes de campo** do modal para consistência com o banco. Envia JSON via `fetch` para `POST /simic/cadastrar`. Os nomes exatos: `anos_de_prisao`, `meses_de_prisao`, `dias_de_prisao`, `numero_de_filhos`, `endereco_familiar`, `bairro_familiar`, `cidade_familiar`, `uf_familiar`, `cep_familiar`.

## Deploy

```bash
docker compose up -d
```

Variáveis de ambiente:
- `MONGO_URI=mongodb://mongo:27017/`
- `MYSQL_URI=mysql+mysqlconnector://user:pass@host:port/siscar`

Imagem Docker: `fernandopereira3/sisuni:latest`
Imagem MongoDB: `fernandopereira3/sisuni_db:latest`

## Armadilhas conhecidas

- `global df_visitas` deve estar no **topo** da função em `visitas.py`, nunca dentro de `if`/`elif`
- CSS e templates ficam em `src/Routes/static/` e `src/Routes/templates/`
- O blueprint `debug` é isento de CSRF (`csrf.exempt(BPdebug)`)
- `jumbo.py` foi movido para `sentenciados/visitas.py` (blueprint `visitas`) — URLs não mudaram
- `funcionarios.py` foi dividido: RH → `administrativo/rh.py`, folgas → `seguranca/folgas.py`
- `pesquisas.py` foi movido para `sentenciados/pesquisas.py`
- A branch `dev` foi deletada — só existe `main`
- **Não tocar em `sentenciados.visitas` nem `sentenciados.marcadores`** — esses campos existem como legado mas não são usados pelo sistema atual. Todo o fluxo de visitas usa `visitas_dia`.
