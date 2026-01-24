import datetime
import subprocess

date = datetime.datetime.now().strftime("%d-%m-%y as %H:%M")

print("Processo iniciado...")
subprocess.run(["clear"])
print("Realizando checagem de erros...")
subprocess.run(["ruff", "format", "."])
subprocess.run(["ruff", "check", "."])
subprocess.run(["clear"])
commit = input("Detalhes do commit: ")
print("Realizando commit...")
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", f"{commit} / {date}"])
subprocess.run(["clear"])
branch = input("Qual o branch devo usar?: ")
subprocess.run(["git", "push", "origin", branch])
subprocess.run(["clear"])
print("Processo finalizado com sucesso!")
