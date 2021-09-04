## Ford vs Ferrari: Car Classifier
[![SkillFactory DataScience](https://img.shields.io/badge/SF-Data%20Science-brightgreen)](https://skillfactory.ru/data-science)
[![Kaggle](https://img.shields.io/badge/-Kaggle-%2334b6ef)](https://www.kaggle.com/c/sf-dl-car-classification)

В этом [соревновательном проекте](https://www.kaggle.com/c/sf-dl-car-classification) стояла задача построения модели классификации автомобилей по фотографиям.

В результате работы над проектом:
- Был построен классификатор изображений;
- Применены различные методы предобработки изображений;
- Задействованы методы обучения *transfer learning* и *finetuning*;
- Найдены и использованы предобученные *SOTA-модели*.

## Описание и ход работы

Был предоставлен готовый [датасет](https://www.kaggle.com/c/sf-dl-car-classification/data) и **baseline** в формате Kaggle Kernel Notebook.
Необходимо было изучить данные и повысить точность baseline-модели.
Базовое решение основывалось на идее взять предобученую на ImageNet сеть Xception и дообучить под задачу.

**Метрика качества:**
- **accuracy** — доля верно предсказанных ответов.
