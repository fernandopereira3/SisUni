import datetime
import subprocess
import sys


# Configuração de estilo visual
class Style:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def run(cmd, description):
    """Executa comandos de subprocesso com tratamento de erro."""
    print(f"{Style.CYAN}>> {description}...{Style.RESET}")
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"{Style.RED}Erro em: {description}{Style.RESET}")
        if e.stderr:
            print(e.stderr.decode())
        sys.exit(1)


def get_commit_prefix():
    """Menu para escolha do padrão Conventional Commits."""
    prefixes = {
        "1": "--feat",
        "2": "--fix",
        "3": "--docs",
        "4": "--refactor",
        "5": "--style",
        "6": "--test",
        "7": "--chore",
    }

    print(f"\n{Style.BOLD}Selecione o tipo de alteração:{Style.RESET}")
    for key, value in prefixes.items():
        print(f"  {key}. {value}")

    escolha = input("\nEscolha um número (ou Enter para pular): ").strip()
    return prefixes.get(escolha, "")


def main():
    try:
        # 1. Validação de ambiente Git
        git_check = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"], capture_output=True
        )
        if git_check.returncode != 0:
            print(f"{Style.RED}Erro: Você não está em um repositório Git!{Style.RESET}")
            return

        # 2. Qualidade de Código (Linting com Ruff)
        try:
            run(["ruff", "format", "."], "Formatando código")
            run(["ruff", "check", "--fix", "."], "Checando erros (Ruff)")
        except FileNotFoundError:
            print(
                f"{Style.CYAN}Nota: Ruff não encontrado, pulando linting.{Style.RESET}"
            )

        # 3. Coleta de informações do Commit
        subprocess.run(["clear"])
        current_branch = (
            subprocess.check_output(["git", "branch", "--show-current"])
            .strip()
            .decode()
        )
        date_str = datetime.datetime.now().strftime("%d-%m-%y %H:%M")

        print(
            f"{Style.BOLD}Branch atual:{Style.RESET} {Style.CYAN}{current_branch}{Style.RESET}"
        )

        detalhes_lista = []
        while True:
            more_details = (
                input(
                    f"{Style.GREEN}Deseja adicionar detalhes ao commit? (s/n): {Style.RESET}"
                )
                .strip()
                .lower()
            )

            if more_details not in ("s", "n"):
                print(f"{Style.RED}Responda 's' ou 'n'.{Style.RESET}")
                continue

            if more_details == "n":
                break

            # more_details == "s"
            prefixo = get_commit_prefix()
            detalhes = input(f"{Style.GREEN}Detalhes do commit: {Style.RESET}").strip()

            if not detalhes:
                print(
                    f"{Style.RED}Cancelado: A mensagem de commit não pode ser vazia.{Style.RESET}"
                )
                return

            # Acumular detalhe na lista
            if prefixo:
                detalhes_lista.append(f"{prefixo}: {detalhes}")
            else:
                detalhes_lista.append(detalhes)

        # Montagem da mensagem final
        if detalhes_lista:
            mensagem_final = " ; ".join(detalhes_lista) + f" / {date_str}"
        else:
            mensagem_final = date_str

        # 4. Git Flow (Add, Commit, Push)
        run(["git", "add", "."], "Adicionando arquivos")
        run(["git", "commit", "-m", mensagem_final], "Realizando commit")

        print(f"\n{Style.BOLD}Mensagem registrada:{Style.RESET} {mensagem_final}")

        push_confirm = input(
            f"\nDeseja dar push para {Style.BOLD}{Style.RED}{current_branch}{Style.RESET}? (s/n): "
        )

        if push_confirm.lower() == "s":
            run(["git", "push", "origin", current_branch], "Enviando para o servidor")
            print(f"{Style.GREEN}✔ Processo finalizado com sucesso!{Style.RESET}")
        else:
            print(f"{Style.CYAN}Commit feito localmente. Push ignorado.{Style.RESET}")

    except KeyboardInterrupt:
        print(f"\n{Style.RED}Operação cancelada pelo usuário.{Style.RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
