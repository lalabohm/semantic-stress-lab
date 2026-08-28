"""
Regressao linear multipla: similaridade ~ razao_tamanho + dependia_contexto,
por modelo, para testar se os dois preditores retem poder explicativo
quando controlados um pelo outro.

Le apenas results/phase1_embeddings/text_length_correlation.csv (ja
produzido anteriormente) e escreve novos artefatos:
  - results/phase1_embeddings/multiple_regression_results.csv
  - results/phase1_embeddings/figures/regression_diagnostics.png
Nao modifica nenhum arquivo existente.
"""

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

ROOT = "/home/larissa/Documentos/semantic-stress-lab"

in_csv = f"{ROOT}/results/phase1_embeddings/text_length_correlation.csv"
out_csv = f"{ROOT}/results/phase1_embeddings/multiple_regression_results.csv"
out_fig = f"{ROOT}/results/phase1_embeddings/figures/regression_diagnostics.png"

df = pd.read_csv(in_csv)

df["dependia_contexto_bin"] = df["dependia_contexto"].astype(bool).astype(int)

models = {
    "BGE-M3": "similaridade_bge_m3",
    "LaBSE": "similaridade_labse",
    "EmbeddingGemma": "similaridade_embeddinggemma",
}

X = df[["razao_tamanho", "dependia_contexto_bin"]].copy()
X = sm.add_constant(X)

rows = []
fitted_models = {}

for name, col in models.items():
    y = df[col]
    model = sm.OLS(y, X).fit()
    fitted_models[name] = model

    print(f"\n=== {name} ===")
    print(model.summary())

    for term in ["const", "razao_tamanho", "dependia_contexto_bin"]:
        rows.append({
            "modelo_embedding": name,
            "termo": term,
            "coeficiente": model.params[term],
            "erro_padrao": model.bse[term],
            "t": model.tvalues[term],
            "p_valor": model.pvalues[term],
            "r_quadrado_modelo": model.rsquared,
            "gl_residuais": int(model.df_resid),
            "n_obs": int(model.nobs),
        })

out_df = pd.DataFrame(rows)
out_df.to_csv(out_csv, index=False)
print(f"\nSalvo: {out_csv}")

# --- diagnostico visual: previsto vs observado, para os tres modelos ---
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)

for ax, (name, col) in zip(axes, models.items()):
    model = fitted_models[name]
    y = df[col]
    y_pred = model.predict(X)

    ax.scatter(y_pred, y, s=60, edgecolor="black", linewidth=0.4, color="#4C72B0")
    lims = [min(y.min(), y_pred.min()) - 0.02, max(y.max(), y_pred.max()) + 0.02]
    ax.plot(lims, lims, color="black", linestyle="--", linewidth=1.0, label="y = x (ajuste perfeito)")
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.set_xlabel("Similaridade prevista pelo modelo OLS")
    ax.set_title(f"{name}\nR²={model.rsquared:.3f}")

axes[0].set_ylabel("Similaridade observada")
axes[0].legend(fontsize=8, loc="upper left")
fig.suptitle("Diagnostico de regressao: previsto vs. observado\n(similaridade ~ razao_tamanho + dependia_contexto)")
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(out_fig, dpi=150, bbox_inches="tight")
print(f"Salvo: {out_fig}")
