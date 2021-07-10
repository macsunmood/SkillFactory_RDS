## **English Accent Recognizer ( EAR )**
![project type](https://img.shields.io/badge/%F0%9F%A6%9C-pet%20project-green)

_Дипломный проект курса SkillFactory Data Science_

---

### Цели и задачи проекта:
- **Цель** - предсказание акцента английского языка спикера по аудиозаписи;
- **Задача-минимум** - сделать классификатор с хорошей (~70-90%) точностью на 3-х акцентах;
- **Сверхзадача:** достичь высокой точности распознавания живой речи с микрофона хотя бы на 5 акцентах.

### Основная метрика:
- **Accuracy score**

### Этапы работы над проектом:
1. Поиск и отбор подходящего датасета;
2. Проведено исследование по работе с аудио, голосовому распознаванию, рассмотрены некоторые существующие варианты решений;
3. Скачан архив с датасетом [Common Voice Corpus 6.1](https://commonvoice.mozilla.org/en/datasets) (~60 Gb), проведен первичный осмотр метаинформации, очистка данных. В результате разархивированы только нужные файлы (~320 тыс., ~14 Gb);
4. Осуществлен Exploratory Data Analysis, подобраны полезные признаки и некоторые способы предобработки;
5. По результатам EDA сделан Data Preprocessing с написанием специальных функций для всех этапов предобработки;
6. Загрузка предобработанных данных на сервер (~65 Gb); моделирование и эксперименты, подбор удачных решений;
7. Скачивание, предобработка и подключение доролнительных внешних датасетов;
8. Конструирование прототипа на Streamlit.

### Составные части репозитория:
- **`Notebooks`** — ноутбуки по всем этапам реализации проекта:
  - [`English Accent Detector [data cleaning + pre-eda].ipynb`](https://github.com/macsunmood/SkillFactory_RDS/blob/master/Diploma.%20Accent%20Recognizer/Notebooks/English%20Accent%20Detector%20%5Bdata%20cleaning%20%2B%20pre-eda%5D.ipynb) - очистка данных и предварительный осмотр
  - [`English Accent Detector [EDA].ipynb`](https://github.com/macsunmood/SkillFactory_RDS/blob/master/Diploma.%20Accent%20Recognizer/Notebooks/English%20Accent%20Detector%20%5BEDA%5D.ipynb) - Exploratory Data Analysis
  - [`English Accent Detector [data preprocessing].ipynb`](https://github.com/macsunmood/SkillFactory_RDS/blob/master/Diploma.%20Accent%20Recognizer/Notebooks/English%20Accent%20Detector%20%5Bdata%20preprocessing%5D.ipynb) - предобработка данных
  - [`English Accent_Detector [models].ipynb`](https://github.com/macsunmood/SkillFactory_RDS/blob/master/Diploma.%20Accent%20Recognizer/Notebooks/English%20Accent%20Detector%20%5Bmodels%5D.ipynb) - моделирование и эксперименты
  - [`English Accent_Detector [models - Table].ipynb`](https://github.com/macsunmood/SkillFactory_RDS/blob/master/Diploma.%20Accent%20Recognizer/Notebooks/English%20Accent%20Detector%20%5Bmodels%20-%20Table%5D.ipynb) - моделирование и эксперименты (для табличных данных)

- **`Proto`** — прототип на Streamlit:
  - `app.py`- основной скрипт с front-end
  - `core.py` - back-end ядро приложения
  - `utils.py` - подключаемые утилиты и вспомогательные функции
  - `examples.py` - экземпляры примеров для пресетов

**Запуск прототипа:**
1. В папку **`models`** поместить файлы моделей (предобученные модели можно скачать **[`▶ здесь ◀`](https://drive.google.com/drive/folders/1tB5hyQPfNooqlF8suWj9Ek3cb4XX5HBE?usp=sharing)**)
2. `pip install streamlit`
3. `streamlit run app.py`

Подробное описание датасета представлено в исследовательском ноутбуке [`English Accent Detector [EDA].ipynb`](https://github.com/macsunmood/SkillFactory_RDS/blob/master/Diploma.%20Accent%20Recognizer/Notebooks/English%20Accent%20Detector%20%5BEDA%5D.ipynb)
