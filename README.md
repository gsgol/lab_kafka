# Лабораторная работа номер 1
## Использованные данные
Использовались случайные 300000 строк датасета [Flight status prediction](https://www.kaggle.com/datasets/robikscube/flight-delay-dataset-20182022?select=Combined_Flights_2019.csv)
## ML задача
Решается задача предсказания на сколько в минутах будет задержан рейс самолета.

## Дашборды
![image](https://github.com/user-attachments/assets/7a845442-133c-4e81-b502-e58956f52fd4)

![image](https://github.com/user-attachments/assets/32bec081-06d3-4e3f-b32f-d987a886305e)

![image](https://github.com/user-attachments/assets/9fec2e2d-e46f-47b9-aad0-c30bf9156a31)

## Требования
Установить зависимости требуемые приложением
```
pip install -r requirements.txt
```
Далее скачать docker образ kafka
```
docker pull bitnami/kafka
```

## Запуск приложения
```
 docker-compose up -d
```
   
Далее последовательно в отдельных терминалах

 ```
 python3 produce.py
```
```
python3 train.py
```
```
streamlit run visualize.py
```

## Завершение работы
Последовательно остановить процессы в отдельных терминалах ``CTRL`` + ``C``

Далее выполнить 
```
docker-compose down
```




