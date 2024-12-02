import requests
from typing import List, Optional, Dict
from youtube_transcript_api import YouTubeTranscriptApi
import json
import openai
import streamlit as st
import pandas as pd
from io import BytesIO

def GPT35(prompt, systeme, secret_key, temperature=0.7, model="gpt-4o-mini", max_tokens=1200):
    url = "https://api.openai.com/v1/chat/completions"
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": systeme},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {secret_key}"
    }

    response = requests.post(url, headers=headers, json=payload)
    response_json = response.json()
    return response_json['choices'][0]['message']['content'].strip()

def generate_optimized_title(api_key: str, video_title: str) -> str:
    prompt = (f"Analyse le titre suivant d'une vidéo YouTube et génère une version optimisée pour le référencement, en tenant compte des mots-clés, de l'engagement et des bonnes pratiques SEO : {video_title}")
    system_message = (f"Vous êtes un assistant de rédaction compétent et expérimenté, spécialisé dans l'optimisation SEO des contenus, "
    "et particulièrement dans la création de titres optimisés pour YouTube. "
    "Votre mission est de rédiger des titres engageants, informatifs et performants en termes de SEO, adaptés aux attentes de l'audience et aux bonnes pratiques de référencement. "
    "Voici le système à suivre pour rédiger une title YouTube optimisée pour le SEO : "
    "Identifier le sujet principal : Définir le thème ou le sujet de la vidéo et l’objectif principal (informer, expliquer, divertir, vendre). "
    "Prioriser les mots-clés avec un fort volume de recherche et une concurrence modérée/faible. Considérer les variantes spécifiques liées à la niche ou au public cible. "
    "Structure optimale de la title : Placer le mot-clé principal au début pour maximiser sa visibilité. "
    "Ajouter un mot-clé secondaire ou un complément descriptif. Insérer des éléments engageants (chiffres, questions, superlatifs) pour inciter au clic. Utiliser les ? et ! pour impacter. "
    "Utilisation des bonnes pratiques SEO : Respecter une longueur idéale de 50 à 60 caractères pour éviter la coupure dans les résultats de recherche. "
    "Utiliser un langage clair, simple et engageant. Éviter les titres vagues ou génériques."
    "Utiliser 1 ou 2 émojis pertinents pour capter l’attention. Utiliser les majuscules avec parcimonie pour mettre en valeur des mots-clés ou des éléments importants. "
    "Incorporer des éléments attractifs : Ajouter un aspect unique ou une promesse claire (ex. : 'En 5 minutes', 'Sans expérience'). "
    "Mettre en avant une solution ou un avantage spécifique. Poser une question pour capter l’attention ou susciter la curiosité. "
    "Adapter au format vidéo et à l'audience : Pour des tutoriels, utiliser des formats comme 'Comment...', 'Guide pour...', 'Tuto'. "
    "Pour des classements ou listes, utiliser 'Top X', 'Les X meilleurs...'. Pour des actualités ou analyses, inclure des termes comme '2024', 'Tendances', 'Analyse'."
    "Réponds UNIQUEMENT avec la Réponse."
)

    optimized_title = GPT35(prompt, system_message, api_key)
    return optimized_title

def generate_optimized_description(api_key: str, video_description: str) -> str:
    prompt = (f"Analyse la description suivante d'une vidéo YouTube et génère une version optimisée pour le référencement, en tenant compte des mots-clés, de l'engagement et des bonnes pratiques SEO : {video_description}")
    system_message = (f"Vous êtes un assistant de rédaction compétent et expérimenté, spécialisé dans l'optimisation SEO des contenus, "
    "et particulièrement dans la création de descriptions optimisées pour YouTube. "
    "Votre mission est de rédiger des descriptions de vidéos engageantes, informatives et performantes en termes de SEO, adaptées aux attentes de l'audience et aux bonnes pratiques de référencement. "
    "Voici le système à suivre pour rédiger une description YouTube optimisée pour le SEO : "
    "Identifier le sujet principal : Définir le thème ou le sujet de la vidéo et l’objectif principal (informer, expliquer, divertir, vendre). "
    "Inclure des mots-clés pertinents liés au contenu de la vidéo. "
    "Ajouter des variantes spécifiques pour maximiser la visibilité et couvrir des requêtes similaires. "
    "Structure optimale de la description : La premiere phrase doit etre une question incitant TRES impactante pour le viewer en lien avec le mot clé principal. Utilise l'emoji 👇 juste apres la question. "
    "Inclure des hashtags pertinents : Ajouter 8 à 10 hashtags stratégiques à la fin de la description pour améliorer la recherche. "
    "Développer un résumé clair et attrayant du contenu de la vidéo dans les premières lignes. "
    "Inclure des phrases contenant des mots-clés secondaires et des compléments pertinents. "
    "Utilisation des bonnes pratiques SEO : Respecter une longueur idéale entre 400 et 500 caractères pour maximiser la visibilité dans les résultats de recherche. "
    "Utiliser un langage clair, simple et engageant. Éviter les descriptions vagues, génériques ou trop répétitives. "
    "Ajouter des éléments attractifs : Mettre en avant un aspect unique de la vidéo, une promesse claire ou un avantage spécifique (ex. : 'Apprenez en 5 minutes', 'Sans expérience'). "
    "Poser une question pour inciter à l’engagement dans les commentaires ou à cliquer sur la vidéo. "
    "Adapter au format vidéo et à l'audience : Pour des tutoriels, commencer par 'Comment...', 'Découvrez...', 'Guide pour...'. "
    "Pour des classements ou listes, utiliser 'Top X', 'Les X meilleurs...'. Pour des analyses ou actualités, inclure des termes comme '2024', 'Tendances', 'Analyse'. "
    "Ajouter des appels à l’action : Inclure des CTA (Call To Action) pour inviter les spectateurs à liker, s’abonner ou visiter un lien spécifique. "
    "Votre priorité est de produire des descriptions engageantes et performantes en termes de SEO, tout en captant l’intérêt des spectateurs."
    "Réponds UNIQUEMENT avec la Réponse."

)

    optimized_description = GPT35(prompt, system_message, api_key)
    return optimized_description

def get_top_videos(api_key: str, query: str, language: str, max_results: int = 5) -> Optional[List[dict]]: 
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults={max_results}&relevanceLanguage={language}&key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        video_items = response.json().get('items', [])
        
        video_details = []
        for item in video_items:
            video_id = item['id']['videoId']
            video_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={video_id}&key={api_key}"
            try:
                video_response = requests.get(video_url)
                video_response.raise_for_status()
                video_data = video_response.json()
                video_details.append(video_data)
            except requests.RequestException:
                print("Error fetching transcript:")  # Log the error
                continue  # Skip to the next video

        return video_details
    except requests.RequestException as e:
        print(f"Error fetching videos: {e}")
        return None

def get_search_suggestions(api_key: str, query: str) -> Optional[List[str]]:
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        suggestions = response.json()[1]
        return suggestions
    except requests.RequestException as e:
        print(f"Error fetching search suggestions: {e}")
        return None

def analyze_video_content(video_id: str, language: str = 'fr') -> str:
    try:
        # Try to get the transcript in the specified language
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        text = ' '.join([entry['text'] for entry in transcript])
        
        return text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return ""

def process_keyword(api_key: str, openai_key: str, keyword: str, language: str, max_results: int) -> pd.DataFrame:
    data = []
    suggestions = get_search_suggestions(api_key, keyword)
    top_videos = get_top_videos(api_key, keyword, language, max_results)
    if top_videos:
        for i, video in enumerate(top_videos, 1):
            snippet = video.get('snippet', {})
            statistics = video.get('statistics', {})
            content_details = video.get('contentDetails', {})
            video_id = video.get('id', '')

            video_data = {
                "Original Title": snippet.get('title', 'N/A'),
                "Optimized Title": generate_optimized_title(openai_key, snippet.get('title', 'N/A')),
                "Original Description": snippet.get('description', 'N/A'),
                "Optimized Description": generate_optimized_description(openai_key, snippet.get('description', 'N/A')),
                "Views": statistics.get('viewCount', 'N/A'),
                "Length": content_details.get('duration', 'N/A'),
                "Published at": snippet.get('publishedAt', 'N/A'),
                "Comments": statistics.get('commentCount', 'N/A'),
                "URL": f"https://www.youtube.com/watch?v={video_id}",
                "Category": snippet.get('categoryId', 'N/A'),
                "Channel": snippet.get('channelTitle', 'N/A'),
                "Transcript": analyze_video_content(video_id, language) if i <= max_results else ""
            }
            data.append(video_data)
    return pd.DataFrame(data)

st.title("YouTube SEO Video Scraper")

api_key = st.text_input("Enter your YouTube API Key")
openai_key = st.text_input("Enter your OpenAI API Key")
keyword = st.text_input("Enter a keyword to fetch top videos")
language = st.selectbox("Select language", ["en", "fr"])
max_results = st.slider("Select number of videos to scrape", 1, 10, 5)

if st.button("Fetch Videos"):
    if api_key and openai_key and keyword:
        df = process_keyword(api_key, openai_key, keyword, language, max_results)
        st.dataframe(df)
        
        # Create a BytesIO buffer to store the Excel file
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        
        st.download_button(
            label="Download data as Excel",
            data=buffer,
            file_name='youtube_videos.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        st.error("Please provide all required inputs.")
