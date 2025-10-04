import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("VSE_GPT_API_KEY")

class RadarAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("VSE_GPT_API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY не найден! Установите VSE_GPT_API_KEY в окружении.")
        self.url = "https://api.vsegpt.ru/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer sk-or-vv-1a8dfaf4540f762b6c3297bda76e35360f21132ede51920cebc10796f1d6ccab",
            "Content-Type": "application/json"
        }
        self.event = None
        self.sources_and_facts = None
        self.draft = None

    # -------------------------------
    # Получение источников и фактов
    # -------------------------------
    def fetch_event_sources(self, headline: str) -> str:
        json_data = {
            "model": "perplexity/latest-large-online",
            "messages": [
                {"role": "system", "content": "Ты аналитическая система RADAR. Найди официальные источники и факты по событию."},
                {"role": "user", "content": f"Найди ссылки, точное название датасета и статистику пользователей для события: {headline}"}
            ]
        }
        response = requests.post(self.url, headers=self.headers, json=json_data)
        response.raise_for_status()
        self.sources_and_facts = response.json()["choices"][0]["message"]["content"]
        return self.sources_and_facts

    # -------------------------------
    # Генерация черновика поста
    # -------------------------------
    def generate_draft(self, event_json: dict) -> dict:
        # Объединяем событие и факты
        combined_event = {
            **event_json,
            "facts": self.sources_and_facts  # добавляем факты в JSON
        }
        self.event = combined_event

        event_str = json.dumps(combined_event, ensure_ascii=False)
        json_data = {
            "model": "openai/gpt-4.1",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Ты редактор деловых новостей. Используй ТОЛЬКО предоставленные факты "
                        "и события. Формат ответа — JSON с ключами headline, lead, bullets, citation."
                    )
                },
                {
                    "role": "user",
                    "content": f"Сделай черновик поста для события и фактов:\n{event_str}"
                }
            ]
        }

        response = requests.post(self.url, headers=self.headers, json=json_data)
        response.raise_for_status()
        draft_str = response.json()["choices"][0]["message"]["content"]

        try:
            self.draft = json.loads(draft_str)
        except json.JSONDecodeError:
            self.draft = {"error": "Не удалось распарсить JSON", "raw": draft_str}
        return self.draft


# -------------------------------
# Пример использования
# -------------------------------
if __name__ == "__main__":
    headline = "Центробанк впервые оценил потенциальный вклад НДС в инфляцию"

    analyzer = RadarAnalyzer()

    # 1️⃣ Получаем факты
    analyzer.fetch_event_sources(headline)

    # 2️⃣ Формируем событие
    sample_event = {
        "headline": headline,
        "hotness": 0.88,
        "why_now": "Центробанк впервые оценил потенциальный вклад НДС в инфляцию",
        "entities": ["Центробанк"],
        "sources": ["https://www.rbc.ru"],
        "timeline": [
            "30 октября 2025 — пресс-релиз о публикации",
            "30 октября 2025 — анонс на официальном сайте"
        ],
        "dedup_group": "cb_tax_inflation_20251030"
    }

    # 3️⃣ Генерируем черновик
    analyzer.generate_draft(sample_event)

    # 4️⃣ Выводим всё красиво
    analyzer.display()
