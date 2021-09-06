## Car Price Prediction
[![SkillFactory Data Science](https://img.shields.io/badge/SF-Data%20Science-brightgreen)](https://skillfactory.ru/data-science)
[![Kaggle](https://img.shields.io/badge/-Kaggle-34b6ef?logo=Kaggle&logoColor=white)](https://www.kaggle.com/c/sf-dl-car-classification)


В рамках [проекта](https://www.kaggle.com/c/sf-dst-car-price) была поставлена задача создать ML-модель, предсказывающую стоимость автомобиля по его характеристикам.

Если такая модель будет работать хорошо, то, например, для компании, занимающейся продажей подержанных автомобилей, это **значительно ускорит выявление выгодных предложений и повысит её прибыль** (пример: [сервис](https://auto.ru/cars/evaluation/) на *auto.ru* и [статья](https://vc.ru/transport/29899-avto-ru-zapustil-besplatnyy-servis-dlya-ocenki-stoimosti-avtomobilya) про него).

## Описание и ход работы

Был предоставлен небольшой датасет с историей продаж компании за короткий период - он использовался для тестовых предсказаний, основную же обучающую часть предлагалось собирать самостоятельно с помощью парсинга. Допускалось применение любых методов и библиотек *ML* за исключением *Deep Learning*.

**Целевая метрика:**
- **[MAPE](http://en.wikipedia.org/wiki/Mean_absolute_percentage_error)** (mean absolute percentage error) — **средняя абсолютная ошибка в процентах**:

![MAPE](https://telegra.ph/file/78bbd99f5562ae6a69afa.png)

**Основные этапы работы состояли в следующем:**
- поиск и сбор нужных данных;
- обработка признаков, data cleaning and preprocessing;
- подготовка решения с применением ML.

## Результаты

Реализация проекта представляла собой коммандную работу с [соревнованием на Kaggle](https://www.kaggle.com/c/sf-dst-car-price).  
По итогам занято **1-е место** ([team SOVIET](https://www.kaggle.com/c/sf-dst-car-price/leaderboard)) на момент проведения соревнования.

Некоторые особенности решения:
- Написан мультипоточный [Web Scraper](https://github.com/macsunmood/SkillFactory_RDS/tree/master/Project%203.%20Car%20Price%20Prediction/Scraper), который может использоваться как самостоятельный скрипт для скрэппинга с портала _auto.ru_;
- Использовано ансамблирование моделей.

---

Датасет и результаты скрэпинга можно скачать **[`▶ здесь ◀`](https://drive.google.com/drive/folders/1D5wDknF2W-zh2ZcKj7KG3zzBX5Xthjm7)**

<details>
<summary>Список признаков, используемых для обучения и тестирования моделей:</summary>
  
- `bodyType` — тип кузова автомобиля
- `brand` — марка автомобиля
- `color` — цвет автомобиля
- `fuelType` — вид топлива
- `modelDate` — год выхода модели автомобиля
- `name` — contains information from several other columns (engineDisplacement, enginePower) plus some piece of a model reference, but not in every case
- `numberOfDoors` — количество дверей в авто
- `productionDate` — год выпуска конкретного автомобиля
- `vehicleConfiguration` — конфигурация автомобиля
- `vehicleTransmission` — тип трансмиссии
- `engineDisplacement` — объем двигателя
- `enginePower` — мощность двигателя
- `description` — описание к объявлению, оставленное владельцем
- `mileage` — общее расстояние, пройденное автомобилем
- `Комплектация` — перечень автомобильного оборудования
- `Привод` — тип трансмиссии
- `Руль` — сторона, на которой находится руль
- `Состояние` — состояние автомобиля
- `Владельцы` — количество владельцев, которые были у авто
- `ПТС` — тип документов на автомобиль (оригинал или дубликат)
- `Таможня` — был ли автомобиль растаможен
- `Владение` — длительность владения последним владельцем

</details>
