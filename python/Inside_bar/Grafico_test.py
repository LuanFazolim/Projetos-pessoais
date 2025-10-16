import random
import statistics
import matplotlib.pyplot as plt

# ------------------------
# CONFIGURAÇÃO
# ------------------------
DAY_MIN = 1
DAY_MAX = 8

MIN_APPS_PER_PERSON = 5   # cada pessoa tem entre 5 e 10 aplicações (total)
MAX_APPS_PER_PERSON = 10

DAYS_PER_PERSON_MIN = 3   # cada pessoa opera em 3-5 dias (escolhidos em 1..8)
DAYS_PER_PERSON_MAX = 5

LUCRO_MIN = -50
LUCRO_MAX = 100

# opcional: para reproduzir sempre os mesmos números
SEED = None
if SEED is not None:
    random.seed(SEED)

# ------------------------
# GERAÇÃO DE DADOS (PRIMEIRO PASSO)
# ------------------------
def gerar_pessoa():
    """Gera um dicionário {dia: [(hora, lucro), ...]}.
       Cada dia tem pelo menos 1 aplicação.
    """
    n_days = random.randint(DAYS_PER_PERSON_MIN, DAYS_PER_PERSON_MAX)
    dias = sorted(random.sample(range(DAY_MIN, DAY_MAX + 1), n_days))
    total_apps = random.randint(MIN_APPS_PER_PERSON, MAX_APPS_PER_PERSON)

    dados = {d: [] for d in dias}

    # Garante 1 aplicação por dia
    for d in dias:
        hora = random.randint(8, 22)
        lucro = round(random.uniform(LUCRO_MIN, LUCRO_MAX), 2)
        dados[d].append((hora, lucro))

    # Distribui o restante das aplicações
    restantes = total_apps - len(dias)
    for _ in range(restantes):
        d = random.choice(dias)
        hora = random.randint(8, 22)
        lucro = round(random.uniform(LUCRO_MIN, LUCRO_MAX), 2)
        dados[d].append((hora, lucro))

    return dados

# gera as 3 pessoas
pessoas = {
    "Pessoa 1": gerar_pessoa(),
    "Pessoa 2": gerar_pessoa(),
    "Pessoa 3": gerar_pessoa(),
}

# ------------------------
# CALCULA GLOBAL MIN/MAX E X RANGE (APÓS GERAR OS DADOS)
# ------------------------
todos_lucros = []
todos_dias = []

for dados in pessoas.values():
    for dia, lista in dados.items():
        if not lista:
            continue
        todos_dias.append(dia)
        for _, lucro in lista:
            todos_lucros.append(lucro)

global_max = max(todos_lucros)
global_min = min(todos_lucros)

y_top = global_max + 5
y_bottom = global_min - 5

x_min = min(todos_dias)
x_max = max(todos_dias)

# ------------------------
# FUNÇÃO DE PLOT (usa médias diárias)
# ------------------------
def mostrar_grafico(nome, dados):
    dias = sorted(dados.keys())
    medias = [statistics.mean([lucro for _, lucro in dados[d]]) for d in dias]

    plt.figure(figsize=(10, 6))
    plt.plot(dias, medias, color='black', linewidth=3, marker='o', label='Média diária')

    # anotações: média e número de aplicações
    for d, m in zip(dias, medias):
        n = len(dados[d])
        va = 'bottom' if m >= 0 else 'top'
        plt.text(d, m, f"{m:.1f}\n(n={n})", ha='center', va=va, fontsize=9)

    plt.axhline(0, color='black', linewidth=1)
    plt.title(f"Lucro médio por dia — {nome}")
    plt.xlabel("Dia")
    plt.ylabel("Lucro (R$)")
    plt.xticks(range(x_min, x_max + 1))
    plt.ylim(y_bottom, y_top)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.show()

# ------------------------
# RESUMO IMPRESSO (para depuração)
# ------------------------
print("=== RESUMO DOS DADOS GERADOS ===")
for nome, dados in pessoas.items():
    total_apps = sum(len(v) for v in dados.values())
    dias = sorted(dados.keys())
    print(f"\n{nome}: {total_apps} aplicações em {len(dias)} dias -> dias {dias}")
    for d in dias:
        lucs = [l for _, l in dados[d]]
        if not lucs:
            print(f"  Dia {d}: sem aplicações (erro de geração)")  # debug extra
            continue
        print(f"  Dia {d}: n={len(lucs)} -> min={min(lucs):.2f}, mean={statistics.mean(lucs):.2f}, max={max(lucs):.2f}")

print(f"\nMáximo global (entre todas as aplicações): {global_max:.2f}")
print(f"Mínimo global (entre todas as aplicações): {global_min:.2f}")
print(f"Eixo Y definido entre {y_bottom:.2f} e {y_top:.2f}")
print(f"Eixo X definido entre dia {x_min} e dia {x_max}")

# ------------------------
# LOBBY INTERATIVO
# ------------------------
while True:
    print("\n=== LOBBY ===")
    print("1 - Pessoa 1")
    print("2 - Pessoa 2")
    print("3 - Pessoa 3")
    print("4 - Sair")
    escolha = input("Escolha uma opção: ").strip()

    if escolha == "1":
        mostrar_grafico("Pessoa 1", pessoas["Pessoa 1"])
    elif escolha == "2":
        mostrar_grafico("Pessoa 2", pessoas["Pessoa 2"])
    elif escolha == "3":
        mostrar_grafico("Pessoa 3", pessoas["Pessoa 3"])
    elif escolha == "4":
        print("Saindo...")
        break
    else:
        print("Opção inválida. Escolha 1/2/3/4.")
