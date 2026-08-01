# 🎧 Spotify Analytics — Análise dos Meus Dados de Escuta

Projeto de análise de dados pessoais do Spotify usando a **Web API** oficial.
Coleta meus top artistas, top músicas e gera visualizações com insights sobre meu gosto musical.

## 📊 Resultados
### Duração média de musicas ouvidas em todos os tempos
<img width="1600" height="960" alt="duracao_musicas_todos_os_tempos" src="https://github.com/user-attachments/assets/b05f80ed-99cc-4db7-a9de-7fb420476aee" />

### Duração média de musicas ouvidas nas últimas 4 semanas
<img width="1600" height="960" alt="duracao_musicas_ultimas_4_semanas" src="https://github.com/user-attachments/assets/930709dd-3416-46f2-bd6b-c59bedb8da54" />

### Duração média de musicas ouvidas nos últimos 6 meses
<img width="1600" height="960" alt="duracao_musicas_ultimos_6_meses" src="https://github.com/user-attachments/assets/712a63b8-5d43-4843-89c8-e8588e713b76" />

### Top Artistas de todos os tempos
<img width="1600" height="1040" alt="top_artistas_todos_os_tempos" src="https://github.com/user-attachments/assets/58bd0cc4-460e-474f-aeb3-70963ec66648" />

### Top Artistas ouvidos nas últimas 4 semanas
<img width="1600" height="1040" alt="top_artistas_ultimas_4_semanas" src="https://github.com/user-attachments/assets/b3d9cc94-0af6-4a2f-ad86-4771363f0551" />

### Top Artistas ouvidos nos últimos 6 meses
<img width="1600" height="1040" alt="top_artistas_ultimos_6_meses" src="https://github.com/user-attachments/assets/82cb9467-a590-491c-8fbe-d8e7a87a72a3" />


### Principais Insights
<!-- Preencha depois de rodar o projeto. Exemplos: -->
- Artista mais ouvido: **Joji**
- Duração média das músicas: **3.2 minutos**

## ⚠️ Sobre limitações da API do Spotify

O Spotify descontinuou alguns recursos da Web API que originalmente seriam
usados neste projeto:
- **Endpoint de `audio-features`** (dançabilidade, energia, humor, BPM):
  desativado desde novembro/2024 para qualquer app novo, sem alternativa
  oficial.
- **Campos `popularity` e `followers`**: removidos das respostas da API na
  migração de fevereiro/2026.

Por isso, a análise aqui foca em: ranking de artistas/músicas mais ouvidos e duração das faixas — dados que ainda estão disponíveis.

## 🛠️ Tecnologias

- Python
- [Spotipy](https://spotipy.readthedocs.io/) — wrapper da Web API do Spotify
- Pandas — manipulação e análise de dados
- Matplotlib / Seaborn — visualização de dados

## 🚀 Como rodar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/spotify-analytics.git
cd spotify-analytics
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure suas credenciais do Spotify
Crie um app gratuito em [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard):
- Redirect URI: `http://127.0.0.1:8888/callback`

Copie `.env.example` para `.env` e preencha com suas credenciais:
```bash
cp .env.example .env
```

### 4. Colete os dados
```bash
python fetch_data.py
```
Na primeira execução, uma janela do navegador vai abrir pra você autorizar o
app com sua conta Spotify.

### 5. Gere as análises
```bash
python analysis.py
```
Os gráficos serão salvos na pasta `output/`.

## 📁 Estrutura do projeto
```
spotify-analytics/
├── fetch_data.py      # Coleta dados via Spotify Web API
├── analysis.py        # Análise exploratória e geração de gráficos
├── data/               # CSVs com os dados coletados (não versionado)
├── output/             # Gráficos gerados (PNG)
├── requirements.txt
├── .env.example
└── README.md
```

## 💡 Possíveis melhorias futuras
- Dashboard interativo com Streamlit
- Análise de evolução do gosto musical ao longo do tempo
- Comparação de perfil sonoro entre playlists
