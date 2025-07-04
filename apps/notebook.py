import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""### Selected views of the dataset generated in the tsca_categories repository""")
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import altair as alt
    import openpyxl
    from pathlib import Path

    return Path, alt, mo, np, pd


@app.cell
def _():
    from rdkit import Chem
    from rdkit.Chem.Draw import IPythonConsole
    from rdkit.Chem import Draw
    from rdkit.Chem import Draw
    from rdkit.Chem import rdFMCS
    Draw.SetComicMode(IPythonConsole.drawOptions)

    return


@app.cell
def _(Path):

    TOP = Path.cwd().as_posix().replace('notebooks','')
    raw_dir = Path(TOP) / 'data' /'raw'
    processed_dir =  Path(TOP) / 'data' /'processed'
    interim_dir = Path(TOP) / 'data' /'interim'
    external_dir = Path(TOP) / 'data' /'external'
    figures_dir = Path(TOP) / 'reports' /'figures'
    return interim_dir, raw_dir


@app.cell
def _(pd, raw_dir):
    df = (pd.read_excel(raw_dir/'tsca_categorisation_071124_wmappingdict.xlsx', index_col=[0]))
    return (df,)


@app.cell
def _(df, mo):
    _df = mo.sql(
        f"""
        select * from df where physical_form = 'liquid' ;
        """
    )
    return


@app.cell
def _(alt, df, mo):
    alt.theme.enable('googlecharts')
    physical_form = mo.ui.altair_chart(alt.Chart(df.physical_form.value_counts().reset_index()).mark_bar().encode(x = 'physical_form:N', y = 'count:Q'))
    physical_form
    return


@app.cell
def _():
    #alt.Chart(df.groupby('group').size().reset_index().rename(columns = {0: 'Frequency_Count'}).sort_values(by = #['Frequency_Count'], ascending=False)).mark_bar().encode(alt.Y('group:N',sort='-x'), alt.X('Frequency_Count'))
    return


@app.cell
def _(alt, df, mo):
    cats_counts = mo.ui.altair_chart(alt.Chart(df.groupby('group').size().reset_index().rename(columns = {0: 'Frequency_Count'}).sort_values(by = ['Frequency_Count'], ascending=False)).mark_bar().encode(alt.X('Frequency_Count:Q').title('Frequency Count'), alt.Y('group:N', sort='-x').title('Group')))
    cats_counts
    return


@app.cell
def _(interim_dir, pd):
    opera_df = pd.read_csv(interim_dir/'opera_df_tox.csv', index_col=[0])

    return (opera_df,)


@app.cell
def _(opera_df):
    catmos = {}
    for i, group in opera_df.groupby('group_str'):
        catmos[i] = group['CATMoS_LD50_pred'].values
    return (catmos,)


@app.cell
def _(np):
    def ecdf(data):
        n = len(data)
        x = np.sort(data)
        y = np.arange(1, n+1)/n
        return x, y
    return (ecdf,)


@app.cell
def _(ecdf, np):
    def catmos_summary(d, label=None):
        summary = {}
        summary['median'] = np.median(d)
        summary['ecdfx'], summary['ecdfy'] = ecdf(d)
        summary['label'] = label
        return summary
    return (catmos_summary,)


@app.cell
def _(catmos, catmos_summary):
    summaries = []
    for k, v in catmos.items():
        summaries.append(catmos_summary(v, label = k))

    return (summaries,)


@app.cell
def _():
    selected_labels = [
        "('Benzenoids', 5.0)",
        "('Fatty Acyls', 3.0)",
        "('Alkaloids and derivatives', nan)",
        "('Organosulfur compounds', 2.0)",
        "('Allenes', nan)"
    ]
    return (selected_labels,)


@app.cell
def _(np, pd, selected_labels, summaries):
    plot_data = []
    for summary in summaries:
        label = summary['label']
        if label in selected_labels:
            x = np.log10(summary['ecdfx'])  # log10 transform
            y = summary['ecdfy']
            for xi, yi in zip(x, y):
                plot_data.append({'label': label, 'log10x': xi, 'ecdfy': yi})

    df_plot = pd.DataFrame(plot_data)
    return (df_plot,)


@app.cell
def _(df_plot):
    df_plot.head()
    return


@app.cell
def _(mo):
    mo.md(r"""Selected ECDFs for categories to show the variation in LD50 potencies""")
    return


@app.cell
def _(alt, df_plot, mo):
    ecdf_selected = mo.ui.altair_chart(alt.Chart(df_plot).mark_point().encode(x = alt.X('log10x:Q', title='CATMoS_log10pred(LD50)'), y = alt.Y('ecdfy:Q', title='ECDF'), color=alt.Color('label:N', title='Category-Subcategory'), tooltip=['label:N', 'log10x:Q', 'ecdfy:Q']).configure_legend(orient='right'))
    ecdf_selected
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
