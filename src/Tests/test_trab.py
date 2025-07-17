from Data.conexao import conexao
from Funcoes.funcoes import construir_tabela_trabalho

db = conexao()

print("Testando conexão com a coleção 'trab'...")

# Verificar se a coleção existe
collections = db.list_collection_names()
print(f"Coleções disponíveis: {collections}")

if 'trab' in collections:
    print("\nColeção 'trab' encontrada!")
    
    # Contar documentos
    count = db.trab.count_documents({})
    print(f"Número de documentos na coleção 'trab': {count}")
    
    if count > 0:
        # Buscar alguns documentos de exemplo
        documentos = list(db.trab.find({}).limit(3))
        print(f"\nPrimeiros 3 documentos:")
        for i, doc in enumerate(documentos, 1):
            print(f"Documento {i}: {doc}")
        
        # Testar a função construir_tabela_trabalho
        print("\nTestando construir_tabela_trabalho...")
        tabela_html = construir_tabela_trabalho(documentos)
        print(f"HTML gerado (primeiros 200 chars): {tabela_html[:200]}")
    else:
        print("A coleção 'trab' está vazia.")
else:
    print("Coleção 'trab' não encontrada!")