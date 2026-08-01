"""
Análise exploratória dos dados coletados do Spotify.
Gera gráficos com um visual inspirado na identidade do Spotify (preto + verde),
salvando arquivos PNG em alta resolução na pasta 'output/'.

Nota: os campos 'popularity', 'followers' e o endpoint de 'audio-features'
foram descontinuados pelo Spotify (fev/2026 e nov/2024, respectivamente).
O campo 'genres' também pode vir vazio dependendo da conta. Por isso, esta
análise foca em ranking, gêneros (quando disponíveis) e duração das músicas.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch

# ---------------------------------------------------------------------------
# Paleta de cores inspirada no Spotify
# ---------------------------------------------------------------------------
SPOTIFY_GREEN = "#1DB954"
SPOTIFY_GREEN_LIGHT = "#4FE377"
BG_COLOR = "#121212"
CARD_COLOR = "#181818"
TEXT_COLOR = "#FFFFFF"
SUBTEXT_COLOR = "#B3B3B3"
GRID_COLOR = "#2A2A2A"

# Gradiente de verdes usado nas barras (do mais escuro ao mais claro)
GREEN_GRADIENT = ["#0D4B25", "#116931", "#15873D", "#1AAF4E", "#1DB954", "#3DDB6F", "#63E88C"]


def setup_style():
    """Configura o tema visual escuro para todos os gráficos."""
    plt.rcParams.update({
        "figure.facecolor": BG_COLOR,
        "axes.facecolor": CARD_COLOR,
        "savefig.facecolor": BG_COLOR,
        "axes.edgecolor": GRID_COLOR,
        "axes.labelcolor": SUBTEXT_COLOR,
        "text.color": TEXT_COLOR,
        "xtick.color": SUBTEXT_COLOR,
        "ytick.color": SUBTEXT_COLOR,
        "grid.color": GRID_COLOR,
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Arial", "DejaVu Sans"],
        "axes.grid": True,
        "grid.linewidth": 0.6,
        "axes.axisbelow": True,
    })


def gradient_colors(n):
    """Retorna n cores interpoladas do gradiente verde."""
    import matplotlib.colors as mcolors
    cmap = mcolors.LinearSegmentedColormap.from_list("spotify_green", GREEN_GRADIENT)
    return [cmap(i / max(n - 1, 1)) for i in range(n)]


def style_axes(ax, title, subtitle=None):
    """Aplica título, remove bordas desnecessárias e adiciona acabamento."""
    ax.set_title(title, fontsize=17, fontweight="bold", color=TEXT_COLOR,
                 loc="left", pad=28 if subtitle else 14)
    if subtitle:
        ax.text(0, 1.06, subtitle, transform=ax.transAxes, fontsize=10.5,
                 color=SUBTEXT_COLOR, ha="left", va="bottom")
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(GRID_COLOR)
    ax.grid(axis="x", alpha=0.5)
    ax.set_axisbelow(True)


def load_data():
    tracks = pd.read_csv("data/top_tracks.csv")
    artists = pd.read_csv("data/top_artists.csv")
    return tracks, artists


def top_artists_chart(artists, periodo="todos_os_tempos", top_n=10):
    """Ranking dos artistas mais ouvidos, com barras em gradiente de verde."""
    df = artists[artists["periodo"] == periodo].sort_values("posicao").head(top_n)
    df = df.iloc[::-1]  # inverte pra o #1 aparecer no topo do gráfico

    fig, ax = plt.subplots(figsize=(10, 6.5))
    colors = gradient_colors(len(df))[::-1]
    bars = ax.barh(df["artista"], top_n + 1 - df["posicao"], color=colors,
                    height=0.68, zorder=3)

    # Rótulo de posição (#1, #2...) dentro/perto de cada barra
    for bar, pos, nome in zip(bars, df["posicao"], df["artista"]):
        ax.text(bar.get_width() + 0.15, bar.get_y() + bar.get_height() / 2,
                f"#{pos}", va="center", ha="left", fontsize=10,
                color=SPOTIFY_GREEN_LIGHT, fontweight="bold")

    ax.set_xticks([])
    ax.set_xlim(0, top_n + 2.5)
    style_axes(ax, "Artistas Mais Ouvidos", f"Ranking pessoal — {periodo.replace('_', ' ')}")
    ax.tick_params(axis="y", labelsize=11, colors=TEXT_COLOR)
    plt.tight_layout()
    plt.savefig(f"output/top_artistas_{periodo}.png", dpi=160)
    plt.close()


def top_genres_chart(artists, periodo="todos_os_tempos", top_n=10):
    df = artists[artists["periodo"] == periodo].copy()
    generos_validos = df["generos"].dropna().astype(str)
    generos_validos = generos_validos[generos_validos.str.strip() != ""]

    if generos_validos.empty:
        print(f"Aviso: nenhum dado de gênero disponível para '{periodo}' (a API do "
              "Spotify não retornou gêneros para estes artistas). Pulando gráfico.")
        return False

    generos = generos_validos.str.split(", ").explode()
    generos = generos[generos.str.strip() != ""]
    top_generos = generos.value_counts().head(top_n).sort_values()

    if top_generos.empty:
        print(f"Aviso: nenhum gênero válido encontrado para '{periodo}'. Pulando gráfico.")
        return False

    fig, ax = plt.subplots(figsize=(10, 6.5))
    colors = gradient_colors(len(top_generos))
    bars = ax.barh(top_generos.index, top_generos.values, color=colors,
                    height=0.65, zorder=3)

    for bar, valor in zip(bars, top_generos.values):
        ax.text(bar.get_width() + max(top_generos.values) * 0.02,
                bar.get_y() + bar.get_height() / 2, str(valor),
                va="center", ha="left", fontsize=10.5,
                color=SPOTIFY_GREEN_LIGHT, fontweight="bold")

    ax.set_xticks([])
    style_axes(ax, "Gêneros Musicais Favoritos", f"Quantidade de artistas por gênero — {periodo.replace('_', ' ')}")
    ax.tick_params(axis="y", labelsize=11, colors=TEXT_COLOR)
    plt.tight_layout()
    plt.savefig(f"output/top_generos_{periodo}.png", dpi=160)
    plt.close()
    return True


def duration_distribution(tracks, periodo="todos_os_tempos"):
    df = tracks[tracks["periodo"] == periodo].copy()
    df["duracao_min"] = df["duracao_ms"] / 60000

    fig, ax = plt.subplots(figsize=(10, 6))
    counts, bins, patches = ax.hist(df["duracao_min"], bins=18,
                                     color=SPOTIFY_GREEN, alpha=0.85,
                                     edgecolor=BG_COLOR, linewidth=1.2, zorder=3)

    # Realça a barra mais alta (duração mais comum) numa cor diferente
    if len(counts) > 0:
        idx_max = counts.argmax()
        patches[idx_max].set_facecolor(SPOTIFY_GREEN_LIGHT)

    media = df["duracao_min"].mean()
    ax.axvline(media, color="#FFFFFF", linestyle="--", linewidth=1.3, zorder=4, alpha=0.8)
    ax.text(media, ax.get_ylim()[1] * 0.95, f"  média: {media:.1f} min",
            color=TEXT_COLOR, fontsize=10, va="top", ha="left")

    style_axes(ax, "Duração das Músicas", f"Distribuição da duração das suas faixas — {periodo.replace('_', ' ')}")
    ax.set_xlabel("Duração (minutos)", fontsize=11)
    ax.set_ylabel("Quantidade de músicas", fontsize=11)
    plt.tight_layout()
    plt.savefig(f"output/duracao_musicas_{periodo}.png", dpi=160)
    plt.close()


def artist_overlap_across_periods(artists):
    """Mostra quais artistas do top 10 se repetem entre curto/médio/longo prazo."""
    periodos = ["ultimas_4_semanas", "ultimos_6_meses", "todos_os_tempos"]
    top10_por_periodo = {
        p: set(artists[artists["periodo"] == p].sort_values("posicao").head(10)["artista"])
        for p in periodos
    }
    fixos = (top10_por_periodo["ultimas_4_semanas"]
             & top10_por_periodo["ultimos_6_meses"]
             & top10_por_periodo["todos_os_tempos"])
    return fixos


def print_insights(tracks, artists):
    print("=" * 50)
    print("PRINCIPAIS INSIGHTS")
    print("=" * 50)

    top_artist = artists[artists["periodo"] == "todos_os_tempos"].sort_values("posicao").iloc[0]
    print(f"Seu artista mais ouvido (de todos os tempos): {top_artist['artista']}")

    top_track = tracks[tracks["periodo"] == "todos_os_tempos"].sort_values("posicao").iloc[0]
    print(f"Sua música mais ouvida (de todos os tempos): {top_track['musica']} - {top_track['artista']}")

    avg_duration = (tracks["duracao_ms"] / 60000).mean()
    print(f"Duração média das músicas: {avg_duration:.1f} minutos")

    fixos = artist_overlap_across_periods(artists)
    print(f"\nArtistas que aparecem no seu top 10 em TODOS os períodos "
          f"(4 semanas, 6 meses e sempre): {len(fixos)}")
    if fixos:
        print(f"  -> {', '.join(sorted(fixos))}")


PERIODOS = ["ultimas_4_semanas", "ultimos_6_meses", "todos_os_tempos"]


def main():
    os.makedirs("output", exist_ok=True)
    setup_style()
    tracks, artists = load_data()

    genres_ok_algum_periodo = False
    for periodo in PERIODOS:
        print(f"\nGerando gráficos para: {periodo.replace('_', ' ')}...")
        top_artists_chart(artists, periodo=periodo)
        genres_ok = top_genres_chart(artists, periodo=periodo)
        duration_distribution(tracks, periodo=periodo)
        genres_ok_algum_periodo = genres_ok_algum_periodo or genres_ok

    print()
    print_insights(tracks, artists)

    if not genres_ok_algum_periodo:
        print("\nNota: o(s) gráfico(s) de gêneros não foram gerados porque a API "
              "do Spotify não retornou essa informação para sua conta no momento.")
    print(f"\n{3 * len(PERIODOS)} gráficos (no máximo) salvos na pasta 'output/', "
          "um conjunto para cada período: últimas 4 semanas, últimos 6 meses e todos os tempos.")


if __name__ == "__main__":
    main()