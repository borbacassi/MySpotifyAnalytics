"""
Coleta dados pessoais do Spotify (top artistas, top músicas e características
de áudio) usando a Web API e salva em arquivos CSV para análise posterior.
"""

import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

SCOPE = "user-top-read"

RANGES = {
    "short_term": "ultimas_4_semanas",
    "medium_term": "ultimos_6_meses",
    "long_term": "todos_os_tempos",
}


def get_spotify_client():
    """Autentica com o Spotify usando OAuth e retorna o client."""
    auth_manager = SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope=SCOPE,
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def fetch_top_tracks(sp, time_range, limit=50):
    """Busca as top músicas do usuário para um período específico.

    Nota: o campo 'popularity' foi removido pela API do Spotify na
    migração de fevereiro/2026, então não é mais coletado.
    """
    results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    tracks = []
    for i, item in enumerate(results["items"], start=1):
        artistas = item.get("artists") or []
        album = item.get("album") or {}
        tracks.append({
            "posicao": i,
            "musica": item.get("name", "Desconhecido"),
            "artista": artistas[0]["name"] if artistas else "Desconhecido",
            "album": album.get("name", "Desconhecido"),
            "duracao_ms": item.get("duration_ms", 0),
            "id_musica": item.get("id", ""),
            "periodo": RANGES[time_range],
        })
    return pd.DataFrame(tracks)


def fetch_top_artists(sp, time_range, limit=50):
    """Busca os top artistas do usuário para um período específico.

    Nota: os campos 'popularity' e 'followers' foram removidos pela API
    do Spotify na migração de fevereiro/2026. O campo 'genres' às vezes
    também vem ausente de forma inconsistente, então usamos .get() com
    valor padrão pra não quebrar a coleta.
    """
    results = sp.current_user_top_artists(limit=limit, time_range=time_range)
    artists = []
    for i, item in enumerate(results["items"], start=1):
        generos = item.get("genres") or []
        artists.append({
            "posicao": i,
            "artista": item.get("name", "Desconhecido"),
            "generos": ", ".join(generos),
            "periodo": RANGES[time_range],
        })
    return pd.DataFrame(artists)

# Nota: a função de audio-features (dançabilidade, energia, humor, etc.)
# foi removida deste projeto porque o Spotify descontinuou esse endpoint
# em novembro/2024 para todos os apps criados após essa data — não há
# alternativa oficial. Mais detalhes no README.


def main():
    os.makedirs("data", exist_ok=True)
    sp = get_spotify_client()

    all_tracks = []
    all_artists = []

    for time_range in RANGES:
        print(f"Coletando dados de: {RANGES[time_range]}...")
        all_tracks.append(fetch_top_tracks(sp, time_range))
        all_artists.append(fetch_top_artists(sp, time_range))

    tracks_df = pd.concat(all_tracks, ignore_index=True)
    artists_df = pd.concat(all_artists, ignore_index=True)

    tracks_df.to_csv("data/top_tracks.csv", index=False)
    artists_df.to_csv("data/top_artists.csv", index=False)

    print("\nDados salvos em 'data/':")
    print(f"  - top_tracks.csv ({len(tracks_df)} linhas)")
    print(f"  - top_artists.csv ({len(artists_df)} linhas)")


if __name__ == "__main__":
    main()