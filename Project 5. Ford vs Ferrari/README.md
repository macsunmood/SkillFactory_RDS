# Ford vs Ferrari: Car Classifier
[![SkillFactory Data Science](https://img.shields.io/badge/SF-Data%20Science-brightgreen)](https://skillfactory.ru/data-science)
[![Kaggle](https://img.shields.io/badge/-Kaggle-34b6ef?logo=Kaggle&logoColor=white)](https://www.kaggle.com/c/sf-dl-car-classification)\
![TF](https://img.shields.io/badge/-TensorFlow-FF6F00?logo=TensorFlow&logoColor=white)


В этом [соревновательном проекте](https://www.kaggle.com/c/sf-dl-car-classification) стояла задача построения модели классификации автомобилей по фотографиям.

В результате работы над проектом:
- Был построен классификатор изображений;
- Применены различные методы предобработки изображений;
- Задействованы методы обучения *transfer learning* и *finetuning*;
- Найдены и использованы предобученные *SOTA-модели*.

## Описание и ход работы

Был предоставлен готовый [датасет](https://www.kaggle.com/c/sf-dl-car-classification/data) (также доступен **[`▶ здесь ◀`](https://drive.google.com/drive/folders/16Uwt4yKmC7ZTGD6Igj9mDwYoo882_I_0)**) и **baseline** в формате Kaggle Kernel Notebook.
Необходимо было изучить данные и повысить точность baseline-модели.
Базовое решение основывалось на идее взять предобученую на ImageNet сеть Xception и дообучить под задачу.

**Метрика качества:**
- **Accuracy** — доля верно предсказанных ответов.

**Основные этапы:**
1. После подгрузки датасета проведен EDA (Разведывательный анализ данных);
2. Поскольку работа шла с относительно небольшим датасетом, добавлена аугментация данных для улучшения генерализации при обучении (данные были завернуты в генератор `ImageDataGenerator`);
3. Была загружена предобученная сеть для **Transfer Learning** и на неё поставлена новая "голова" (head). Испробованы Xception и EfficientNet;
4. Далее шли эксперименты с самой легковесной моделью EfficientNetB0 и подбор гиперпараметров;
5. После подбора оптимальных настроек подгружена более совершенная модель **EfficientNetB3** и вместе с **Transfer Learning** применена техника **Fine-tuning** с постепенным размораживанием слоев;
6. На последнем шаге модель дообучена с увеличенным размером изображения (**512x512**) и уменьшенным **BATCH_SIZE**;
7. Добавлена **Test Time Augmentation (TTA)**, что еще улучшило результат;

---

## Результаты

Занято **3-е место** ([macsunmood](https://www.kaggle.com/c/sf-dl-car-classification/leaderboard)) на момент проведения соревнования.\
Достигнутая **_accuracy_** на kaggle: **`0.97827`**  (**`+4.7%`** к baseline: `0.93408`)
 
**Итоги и особенности решения:**
- Применена **аугментация** данных;
- Написан новый callback: `TimingCallback`;
- Использован **LearningRateScheduler** со **scheduler** `lr * tf.math.exp(decay_rate)` для плавного уменьшения Learning rate;
- Заметный прирост точности показало добавление в архитектуру "головы" **BatchNormalization**;
- Из протестированных оптимизаторов (Adam, Nadam, Adamax..) лучший результат показал **Adam** с параметром **amsgrad=True**;
- Добавлена **l2-регуляризация**;
- Для улучшения предсказаний на kaggle submit использована техника **Test Time Augmentations**;

**Возможные способы улучшения результата:**
- Ансамблирование предобученных нейросетей;
- Динамическое увеличение размера картинки при Fine-tuning;
- Другие стратегии разморозки слоев;
- Cyclic Learning Rate;
- Использование внешних датасетов для дообучения модели.
