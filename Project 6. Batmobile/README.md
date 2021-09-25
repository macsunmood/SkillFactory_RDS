# Batmobile: Car Price Prediction
[![SkillFactory Data Science](https://img.shields.io/badge/SF-Data%20Science-brightgreen)](https://skillfactory.ru/data-science)
[![Kaggle](https://img.shields.io/badge/-Kaggle-34b6ef?logo=Kaggle&logoColor=white)](https://www.kaggle.com/c/sf-dst-car-price-prediction-part2)\
![TF](https://img.shields.io/badge/-TensorFlow-FF6F00?logo=TensorFlow&logoColor=white)
![NLP](https://img.shields.io/badge/Deep_Learning-NLP-1f8280)

Этот [финальный проект](https://www.kaggle.com/c/sf-dst-car-price-prediction-part2) курса _Real Data Science_ подводил итоги обучения по курсам _Machine Learning_ и _Deep Learning_ и являлся продолжением соревнования ([Project 3. Car Price Prediction](https://github.com/macsunmood/SkillFactory_RDS/tree/master/Project%203.%20Car%20Price%20Prediction)), но уже с дополнительными данными (текст и изображения).

Задача заключалась в доведении работы по созданию модели, предсказывающей стоимость автомобиля, до логического завершения: обогатить датасет текстовыми данными из объявлений о продаже и свести все модели в единое решение — **Multiple Inputs сеть**.

> Эффективно работающая, такая модель позволит быстро выявлять выгодные предложения, что **значительно ускорит работу менеджеров и повысит прибыль компании**.

## Описание и ход работы

**Целевая метрика:**
- **[MAPE](http://en.wikipedia.org/wiki/Mean_absolute_percentage_error)** (mean absolute percentage error) — **средняя абсолютная ошибка в процентах**:

![MAPE](https://render.githubusercontent.com/render/math?math=MAPE%20=%20\frac{1}{n}%20\sum1^n%20\frac{|Yt%20-%20\hat{Y}_t|}{Yt})

```
Где:
Yt – фактический значение за анализируемый период;
Ŷt — значение прогнозной модели за анализируемый период;
n — количество периодов.
```

Предоставлялся готовый датасет и baseline в формате Kaggle Kernel Notebook. 
Было разрешено использовать любые ML и DL алгоритмы и библиотеки.


В РЕЗУЛЬТАТЕ ВЫПОЛНЕНИЯ ПРОЕКТА:
- Обработаны данные и оптимизированы NLP-модели.
- Пройден весь цикл разработки комплексной Multi-Inputs модели (от обработки данных до внедрения в продакшн).
- Использовано blend-решение, повлиявшее на целевую метрику.
