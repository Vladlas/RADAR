import streamlit as st
import json
from utils import RadarAnalyzer  # твой класс из предыдущего кода

st.set_page_config(page_title="RADAR News Analyzer", layout="wide")
st.title("📰 RADAR - Выявление горячих финансовых новостей")

# -------------------------------
# Форма ввода события
# -------------------------------
with st.form("event_form"):
    headline = st.text_input(
        "📝 Заголовок события (headline)",
        "",
        help="Краткий заголовок события"
    )

    hotness = st.slider(
        "🔥 Оценка горячести (hotness ∈ [0,1])",
        0.0, 1.0, 0.5,
        help="Оценка, насколько событие горячее, влияет на рынки и активы"
    )

    why_now = st.text_area(
        "📌 Почему важно сейчас (why_now)",
        "",
        help="1–2 фразы о новизне, подтверждениях и масштабе затронутых активов"
    )

    entities = st.text_input(
        "🏷 Сущности (entities)",
        "",
        help="Компании, тикеры, страны или сектора, связанные с событием"
    )

    sources = st.text_area(
        "🔗 Источники (sources)",
        "",
        help="3–5 проверяемых ссылок: оригинал, подтверждение, апдейт"
    )

    timeline = st.text_area(
        "⏱ Таймлайн события (timeline)",
        "",
        help="Ключевые метки времени: первое сообщение → подтверждение → уточнение"
    )

    dedup_group = st.text_input(
        "🆔 ID кластера дубликатов (dedup_group)",
        "",
        help="Идентификатор кластера дубликатов/перепечаток"
    )

    submit = st.form_submit_button("✅ Сгенерировать черновик")

if submit:
    # Формируем словарь события
    sample_event = {
        "headline": headline,
        "hotness": hotness,
        "why_now": why_now,
        "entities": [e.strip() for e in entities.split(",")],
        "sources": [s.strip() for s in sources.splitlines() if s.strip()],
        "timeline": [t.strip() for t in timeline.splitlines() if t.strip()],
        "dedup_group": dedup_group
    }

    # Создаём экземпляр анализатора
    analyzer = RadarAnalyzer()

    # Получаем факты от Perplexity
    with st.spinner("Получаем факты и источники..."):
        try:
            facts = analyzer.fetch_event_sources(headline)
            st.subheader("🔗 Факты и источники")
            st.text(facts)
        except Exception as e:
            st.error(f"Ошибка при получении фактов: {e}")

    # Генерируем черновик поста
    with st.spinner("Генерируем черновик поста..."):
        try:
            draft = analyzer.generate_draft(sample_event)
            st.subheader("📝 Черновик поста")
            st.json(draft)
        except Exception as e:
            st.error(f"Ошибка при генерации черновика: {e}")

    # Показать исходное событие
    st.subheader("📌 Исходное событие")
    st.json(sample_event)
