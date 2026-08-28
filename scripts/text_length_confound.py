"""
Checagem de confound: diferença de tamanho (texto_simplificado vs texto_original)
vs. similaridade de cosseno, e cruzamento com dependência de contexto prévio.

Le apenas os dados existentes (dataset_v0.jsonl, cosine_similarity_by_model_v1.csv,
context_dependency_v1.csv) e escreve novos artefatos:
  - results/phase1_embeddings/text_length_correlation.csv
  - results/phase1_embeddings/figures/length_vs_similarity.png
Nao modifica nenhum arquivo existente.
"""

import json
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

ROOT = "/home/larissa/Documentos/semantic-stress-lab"

dataset_path = f"{ROOT}/data/processed/dataset_v0.jsonl"
sim_path = f"{ROOT}/results/phase1_embeddings/cosine_similarity_by_model_v1.csv"
ctx_path = f"{ROOT}/results/phase1_embeddings/context_dependency_v1.csv"

out_csv = f"{ROOT}/results/phase1_embeddings/text_length_correlation.csv"
out_fig = f"{ROOT}/results/phase1_embeddings/figures/length_vs_similarity.png"

# --- carregar dados ---
records = []
with open(dataset_path, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))
df_text = pd.DataFrame(records)[["id", "texto_original", "texto_simplificado"]]

df_sim = pd.read_csv(sim_path)
df_ctx = pd.read_csv(ctx_path)

# --- calcular tamanho ---
df_text["len_original"] = df_text["texto_original"].str.len()
df_text["len_simplificado"] = df_text["texto_simplificado"].str.len()
df_text["diferenca_caracteres"] = df_text["len_simplificado"] - df_text["len_original"]
df_text["razao_tamanho"] = df_text["len_simplificado"] / df_text["len_original"]

# --- merge ---
df = df_text.merge(
    df_sim[["id", "fenomeno_linguistico", "similaridade_bge_m3", "similaridade_labse", "similaridade_embeddinggemma"]],
    on="id", how="inner",
)
df = df.merge(
    df_ctx[["id", "precisa_contexto_previo"]],
    on="id", how="inner",
)
df = df.rename(columns={"precisa_contexto_previo": "dependia_contexto"})

assert len(df) == 25, f"esperado 25 pares, obtido {len(df)}"

# --- salvar CSV de saida ---
cols_out = [
    "id", "fenomeno_linguistico", "diferenca_caracteres", "razao_tamanho",
    "dependia_contexto", "similaridade_bge_m3", "similaridade_labse", "similaridade_embeddinggemma",
]
df[cols_out].to_csv(out_csv, index=False)
print(f"Salvo: {out_csv}")

# --- correlacoes de Pearson ---
models = {
    "BGE-M3": "similaridade_bge_m3",
    "LaBSE": "similaridade_labse",
    "EmbeddingGemma": "similaridade_embeddinggemma",
}

print("\n=== Correlacao de Pearson: diferenca absoluta de caracteres vs similaridade ===")
corr_results = {}
for name, col in models.items():
    r, p = stats.pearsonr(df["diferenca_caracteres"], df[col])
    corr_results[("abs", name)] = (r, p)
    print(f"{name:15s} r={r:+.4f}  p={p:.4f}")

print("\n=== Correlacao de Pearson: razao de tamanho vs similaridade ===")
for name, col in models.items():
    r, p = stats.pearsonr(df["razao_tamanho"], df[col])
    corr_results[("razao", name)] = (r, p)
    print(f"{name:15s} r={r:+.4f}  p={p:.4f}")

# --- Mann-Whitney: diferenca de tamanho / razao vs dependencia de contexto ---
print("\n=== Mann-Whitney U: diferenca de tamanho / razao entre grupos de dependencia de contexto ===")
grp_dep = df[df["dependia_contexto"] == True]
grp_indep = df[df["dependia_contexto"] == False]
print(f"n dependente={len(grp_dep)}  n autocontido={len(grp_indep)}")

u_abs, p_abs = stats.mannwhitneyu(grp_dep["diferenca_caracteres"], grp_indep["diferenca_caracteres"], alternative="two-sided")
print(f"Diferenca absoluta:  U={u_abs:.2f}  p={p_abs:.4f}")
print(f"  mediana dependente={grp_dep['diferenca_caracteres'].median():.1f}  mediana autocontido={grp_indep['diferenca_caracteres'].median():.1f}")

u_razao, p_razao = stats.mannwhitneyu(grp_dep["razao_tamanho"], grp_indep["razao_tamanho"], alternative="two-sided")
print(f"Razao de tamanho:    U={u_razao:.2f}  p={p_razao:.4f}")
print(f"  mediana dependente={grp_dep['razao_tamanho'].median():.3f}  mediana autocontido={grp_indep['razao_tamanho'].median():.3f}")

# --- scatter plots ---
fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), sharey=True)

phenomena = sorted(df["fenomeno_linguistico"].unique())
cmap = plt.get_cmap("tab20")
color_map = {ph: cmap(i % 20) for i, ph in enumerate(phenomena)}

for ax, (name, col) in zip(axes, models.items()):
    for ph in phenomena:
        sub = df[df["fenomeno_linguistico"] == ph]
        ax.scatter(sub["diferenca_caracteres"], sub[col], color=color_map[ph], label=ph, s=60, edgecolor="black", linewidth=0.4)

    # linha de tendencia
    r, p = corr_results[("abs", name)]
    z = pd.Series(df["diferenca_caracteres"]).values
    coeffs = stats.linregress(df["diferenca_caracteres"], df[col])
    x_line = [df["diferenca_caracteres"].min(), df["diferenca_caracteres"].max()]
    y_line = [coeffs.intercept + coeffs.slope * x for x in x_line]
    ax.plot(x_line, y_line, color="black", linestyle="--", linewidth=1.2)

    ax.set_title(f"{name}\nr={r:+.3f}, p={p:.3f}")
    ax.set_xlabel("Diferenca de tamanho (caracteres)\n(simplificado - original)")

axes[0].set_ylabel("Similaridade de cosseno")

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, -0.18), ncol=4, fontsize=8, title="Fenomeno linguistico")
fig.suptitle("Diferenca de tamanho vs. similaridade de cosseno, por modelo (n=25 pares)")
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(out_fig, dpi=150, bbox_inches="tight")
print(f"\nSalvo: {out_fig}")
