# RADAR
Перед запуском добавте 
VSE_GPT_API_KEY=sk-or-vv-1a8dfaf4540f762b6c3297bda76e35360f21132ede51920cebc10796f1d6ccab

1) Windows (PowerShell)
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
macOS / Linux
python3.11 -m venv .venv
source .venv/bin/activate
2) Поставь библиотеки
pip install --upgrade pip
pip install -r requirements.txt
3) Ключ (если используешь .env-вариант)
Создай файл .env в корне:
VSE_GPT_API_KEY=sk-ВАШ_ТОКЕН
(если оставляешь хардкод в utils.py — шаг можно пропустить)
4) Запуск Streamlit
Вариант А (у тебя в проекте — pages.py)
streamlit run pages.py

Вариант Б (если файл реально называется rages.py — вдруг опечатка)
streamlit run rages.py

Открой в браузере адрес из консоли (обычно):
http://localhost:8501


