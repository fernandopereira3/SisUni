#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de lista com X numero de registros fictícios
Baseado no formato do arquivo lista.json fornecido
"""

import json
import random
from datetime import datetime, timedelta
import time

# Arrays de nomes e sobrenomes brasileiros
nomes = [
    "JOSÉ",
    "JOÃO",
    "ANTÔNIO",
    "FRANCISCO",
    "CARLOS",
    "PAULO",
    "PEDRO",
    "LUCAS",
    "LUIZ",
    "MARCOS",
    "GABRIEL",
    "RAFAEL",
    "MATEUS",
    "FELIPE",
    "BRUNO",
    "GUSTAVO",
    "DANIEL",
    "RODRIGO",
    "LEANDRO",
    "FERNANDO",
    "RICARDO",
    "SAMUEL",
    "ANDRÉ",
    "THIAGO",
    "ALEXANDRE",
    "EDUARDO",
    "DIEGO",
    "LEONARDO",
    "JORGE",
    "ROBERTO",
    "SÉRGIO",
    "AUGUSTO",
    "VINÍCIUS",
    "CAIO",
    "MURILO",
    "FÁBIO",
    "IGOR",
    "GUILHERME",
    "RENATO",
    "WALLACE",
    "JEFFERSON",
    "WELLINGTON",
    "CRISTIANO",
    "ALAN",
    "EMERSON",
    "RAUL",
    "WESLEY",
    "VICTOR",
    "EVERTON",
    "CÍCERO",
    "MARIA",
    "ANA",
    "FRANCISCA",
    "ANTÔNIA",
    "ADRIANA",
    "JULIANA",
    "MARCIA",
    "FERNANDA",
    "PATRÍCIA",
    "ALINE",
    "SANDRA",
    "CAMILA",
    "AMANDA",
    "BRUNA",
    "JÉSSICA",
    "LETÍCIA",
    "FABIANA",
    "DANIELA",
    "GABRIELA",
    "ALESSANDRA",
    "SIMONE",
    "ELAINE",
    "CARLA",
    "LUCIANA",
    "TATIANE",
    "RAQUEL",
    "DÉBORA",
    "BIANCA",
    "VANESSA",
    "LARISSA",
    "MICHELE",
    "CLÁUDIA",
    "RENATA",
    "SHEILA",
    "SÔNIA",
    "RITA",
    "ROSA",
    "CÍNTIA",
    "VIVIANE",
    "REGINA",
    "CRISTIANE",
    "MÔNICA",
    "ELISÂNGELA",
    "KELLY",
    "TÂNIA",
    "NATÁLIA",
    "PAULA",
    "SOLANGE",
    "VERÔNICA",
    "ISABEL",
]

sobrenomes = [
    "SILVA",
    "SANTOS",
    "OLIVEIRA",
    "SOUZA",
    "RODRIGUES",
    "FERREIRA",
    "ALVES",
    "PEREIRA",
    "LIMA",
    "GOMES",
    "RIBEIRO",
    "CARVALHO",
    "ALMEIDA",
    "LOPES",
    "SOARES",
    "FERNANDES",
    "VIEIRA",
    "BARBOSA",
    "ROCHA",
    "DIAS",
    "MONTEIRO",
    "MENDES",
    "CAMPOS",
    "COSTA",
    "MARTINS",
    "ARAUJO",
    "NASCIMENTO",
    "CORREIA",
    "TEIXEIRA",
    "REIS",
    "MACHADO",
    "CARDOSO",
    "NUNES",
    "CASTRO",
    "FREITAS",
    "MOREIRA",
    "MIRANDA",
    "PINTO",
    "CAVALCANTI",
    "AZEVEDO",
    "MORAIS",
    "CUNHA",
    "RAMOS",
    "MOURA",
    "FONSECA",
    "XAVIER",
    "COELHO",
    "MEDEIROS",
    "TORRES",
    "ANDRADE",
    "MELO",
    "BARROS",
    "PAIVA",
    "NOGUEIRA",
    "MAGALHAES",
    "TAVARES",
    "BEZERRA",
    "FARIAS",
    "BAPTISTA",
    "MARQUES",
]

procedencias = [
    "CPP VALPARAISO",
    "CPP SOROCABA",
    "CPP PRESIDENTE VENCESLAU",
    "CPP AMERICANA",
    "CPP ARARAQUARA",
    "CPP BAURU",
    "CPP CAMPINAS",
    "CPP FRANCA",
    "CPP GUARULHOS",
    "CPP JUNDIAI",
    "CPP LIMEIRA",
    "CPP MARILIA",
    "CPP MOGI DAS CRUZES",
    "CPP OSASCO",
    "CPP PIRACICABA",
    "CPP RIBEIRAO PRETO",
    "CPP SANTO ANDRE",
    "CPP SAO BERNARDO",
    "CPP SAO CAETANO",
    "CPP SAO JOSE DOS CAMPOS",
    "CPP SAO VICENTE",
    "CPP TAUBATE",
    "CPP DIADEMA",
    "CPP SUZANO",
    "CPP CARAPICUIBA",
]

pavilhoes = [
    "1A",
    "1B",
    "1C",
    "2A",
    "2B",
    "2C",
    "3A",
    "3B",
    "3C",
    "4A",
    "4B",
    "4C",
    "5A",
    "5B",
    "5C",
]


def random_date(start_date, end_date):
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime("%d/%m/%Y")


def generate_rg():
    digits = [random.randint(0, 9) for _ in range(8)]
    rg_base = "".join(map(str, digits))
    check_digit = random.randint(0, 9)
    if random.random() < 0.1:  # 10% de chance de ter X como dígito verificador
        check_digit = "X"
    return f"{rg_base[:2]}.{rg_base[2:5]}.{rg_base[5:8]}-{check_digit}"


def generate_matricula():
    return str(random.randint(10000, 1500000))


def generate_nome():
    """Gera um nome completo brasileiro"""
    primeiro_nome = random.choice(nomes)
    segundo_nome = random.choice(sobrenomes)
    terceiro_nome = random.choice(sobrenomes)

    # 70% de chance de ter um nome do meio
    if random.random() > 0.3:
        nome_do_meio = (
            random.choice(nomes) if random.random() > 0.5 else random.choice(sobrenomes)
        )
        return f"{primeiro_nome} {nome_do_meio} {segundo_nome} {terceiro_nome}"

    return f"{primeiro_nome} {segundo_nome} {terceiro_nome}"


def generate_registro():
    nascimento_inicio = datetime(1940, 1, 1)
    nascimento_fim = datetime(2006, 12, 31)

    inclusao_inicio = datetime(2001, 1, 1)
    inclusao_fim = datetime(2025, 12, 31)

    return {
        "matricula": generate_matricula(),
        "nome": generate_nome(),
        "rg": generate_rg(),
        "nascimento": random_date(nascimento_inicio, nascimento_fim),
        "inclusao": random_date(inclusao_inicio, inclusao_fim),
        "procedencia": random.choice(procedencias),
        "pavilhao": random.choice(pavilhoes),
    }


def main():
    """Função principal"""
    lista = []
    start_time = time.time()
    quantidade = int(input("Digite a quantidade de registros a ser gerada: "))

    for i in range(quantidade):
        registro = generate_registro()
        lista.append(registro)

        # Mostrar progresso a cada 10.000 registros
        if (i + 1) % (quantidade // 10) == 0:
            elapsed = time.time() - start_time
            print(f"Gerados {i + 1:,} registros... ({elapsed:.1f}s)")

    end_time = time.time()
    print(f"\nGeração concluída em {end_time - start_time:.2f} segundos")

    # Salvar em arquivo JSON
    print("Salvando arquivo JSON...")
    with open("db_modelo.json", "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)

    print("Arquivo 'db_modelo.json' criado com sucesso!")
    print(f"Total de registros: {len(lista):,}")

    # Mostrar exemplos dos primeiros 3 registros
    print("\nExemplo dos primeiros 3 registros:")
    print(json.dumps(lista[:3], ensure_ascii=False, indent=2))

    # Estatísticas básicas
    print("\nEstatísticas:")
    print("- Arquivo salvo: db_modelo.json")
    print(f"- Registros gerados: {len(lista):,}")
    print(f"- Tempo de execução: {end_time - start_time:.2f} segundos")
    print(f"- Procedências diferentes: {len(set(r['procedencia'] for r in lista))}")
    print(f"- Pavilhões diferentes: {len(set(r['pavilhao'] for r in lista))}")


if __name__ == "__main__":
    main()
