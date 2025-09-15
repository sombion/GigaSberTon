# GigaSberTon

## Для работы необходим файл .env
### Файл .env
```
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=...
DB_NAME=sber_ton

GIGACHAT_TOKEN=...
GIGACHAT_MODEL=GigaChat

TG_TOKEN=...

```
IP: 178.72.128.235:8080 - Frontend
Адрес tg-бота: @minzhkh36_bot

API Documentation
1. API Applications
POST /api/applications/create

Теги: API applications
Summary: Create Application
Описание: Создание новой заявки
Тело запроса: объект SCreateApplications

PATCH /api/applications/departure

Теги: API applications
Summary: Update Departure Date
Описание: Изменение даты выезда по заявке
Тело запроса: объект SApplicationsDeparture

DELETE /api/applications/delete/{id}

Теги: API applications
Summary: Delete Application
Описание: Удаление заявки по ID

GET /api/applications/all

Теги: API applications
Summary: Get All Applications
Описание: Получение списка всех заявок

GET /api/applications/detail/{id}

Теги: API applications
Summary: Get Application by ID
Описание: Просмотр заявки по ID

GET /api/applications/search/{text}

Теги: API applications
Summary: Search Applications
Описание: Поиск заявок по тексту

GET /api/applications/filter

Теги: API applications
Summary: Filter Applications
Описание: Фильтрация заявок
Параметры запроса: street, date_from, date_to, is_departure

GET /api/applications/street

Теги: API applications
Summary: Get Street List
Описание: Получение списка улиц по поисковому запросу

GET /api/applications/download/{id}

Теги: API applications
Summary: Download Application
Описание: Загрузка файла заявки

GET /api/applications/view/{id}

Теги: API applications
Summary: View Application
Описание: Просмотр заявки (PDF/документ)

2. API Conclusion
POST /api/conclusion/create

Теги: API conclusion
Summary: Create Conclusion
Описание: Создание заключения
Тело запроса: объект SCreateConclusion

PATCH /api/conclusion/update

Теги: API conclusion
Summary: Update Conclusion
Описание: Обновление заключения

GET /api/conclusion/all

Теги: API conclusion
Summary: Get All Conclusions
Описание: Получение списка всех заключений

GET /api/conclusion/detail/{id}

Теги: API conclusion
Summary: Get Conclusion by ID
Описание: Просмотр заключения по ID

GET /api/conclusion/search/{text}

Теги: API conclusion
Summary: Search Conclusions
Описание: Поиск заключений по тексту

GET /api/conclusion/filter

Теги: API conclusion
Summary: Filter Conclusions
Описание: Фильтрация заключений
Параметры запроса: street, date_from, date_to, signed

GET /api/conclusion/download/{id}

Теги: API conclusion
Summary: Download Conclusion
Описание: Загрузка заключения

GET /api/conclusion/view/{id}

Теги: API conclusion
Summary: View Conclusion
Описание: Просмотр заключения (PDF/документ)

3. API Notification
POST /api/notification/make

Теги: API Notification
Summary: Make Notification (Telegram)
Описание: Отправка уведомления пользователю по tg_id

POST /api/notification/add

Теги: API Notification
Summary: Add Notification
Описание: Добавление уведомления пользователю по user_id

GET /api/notification/all

Теги: API Notification
Summary: Get All Notifications
Описание: Получение всех уведомлений текущего пользователя

POST /api/notification/read

Теги: API Notification
Summary: Read Notification
Описание: Отметка уведомления как прочитанного
Тело запроса: объект SNotificationId

GET /api/notification/read-all

Теги: API Notification
Summary: Read All Notifications
Описание: Отметка всех уведомлений пользователя как прочитанных

DELETE /api/notification/delete

Теги: API Notification
Summary: Delete Notification
Описание: Удаление уведомления
Тело запроса: объект SNotificationId

4. API Signature
GET /api/signature/all

Теги: API Signature
Summary: Get All Signatures
Описание: Получение всех подписей

POST /api/signature/subscribe

Теги: API Signature
Summary: Subscribe Signature
Описание: Добавление подписи пользователя
Тело запроса: объект SAddSignature

GET /api/signature/search/{text}

Теги: API Signature
Summary: Search Signatures
Описание: Поиск подписей по тексту

GET /api/signature/filter

Теги: API Signature
Summary: Filter Signatures
Описание: Фильтрация подписей
Параметры запроса: street, date_from, date_to

