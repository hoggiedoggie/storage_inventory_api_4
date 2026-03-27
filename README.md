# 📦 Storage Inventory API (Lab #4)
### Финальная итерация системы инвентаризации накопителей. Основной упор сделан на автоматизированное документирование по стандарту OpenAPI 3.1, продвинутую конфигурацию сред и интеграцию механизмов безопасности непосредственно в Swagger UI.

# 🛠 Технологический стек
### Backend: Python 3.13 + FastAPI.

### Docs: OpenAPI 3.1 + Swagger UI.

### Security: JWT, Bcrypt, HttpOnly Cookies.

### Database: PostgreSQL + SQLAlchemy.

### DevOps: Docker + Docker Compose.

# ⚙️ Конфигурация среды (.env)
###
 | Переменная          | Описание                     | Значение для теста         |
 |---------------------|------------------------------|----------------------------|
 | APP_ENV             | Режим работы приложения      | development / production   |
 | PROJECT_NAME        | Название в заголовке Swagger | Storage Inventory API      |
 | JWT_ACCESS_SECRET   | Секретный ключ для подписи   | your_secret_key            |
###
# 🚀 Запуск и проверка
## 1. Сборка и старт:
```
 docker-compose up -d --build
```
## 2. Автоматическое создание таблиц:
### В данной версии таблицы (users, storage_devices) создаются автоматически при старте приложения благодаря Base.metadata.create_all в main.py.

## 3. Доступ к документации:

### Swagger UI: http://localhost:8000/api/docs

### OpenAPI JSON: http://localhost:8000/api/openapi.json

# 🔐 Тестирование авторизации в Swagger
### Для проверки защищенных эндпоинтов (управление дисками) выполните шаги:

### Перейдите в секцию Authentication -> POST /login.

### После успешного выполнения браузер получит HttpOnly Cookie.

### Используйте кнопку Authorize (иконка замка) в верхней части страницы.

### Теперь все запросы к Storage Management будут проходить успешно, так как Swagger будет автоматически прикреплять вашу куку к запросам.

# 📊 Примеры данных (Storage Management)
### Пример регистрации типичного устройства из вашей коллекции:
```
JSON
{
  "model": "Western Digital Blue 4TB",
  "serial_number": "WD-WCC7K123456",
  "capacity_gb": 4000,
  "status": "active"
}
```
# 🛡 Безопасность и архитектура
### Tags Grouping: Эндпоинты разделены на логические группы: Authentication и Storage Management.

### Automatic Ownership: При создании устройства owner_id извлекается из JWT-токена в куках. Пользователь физически не может создать запись для другого человека.

### Status Codes: Документированы все коды ответов: 201 (Created), 401 (Unauthorized), 404 (Not Found), 422 (Validation Error).

# 📋 Полезные команды
### Логи приложения: ``` docker-compose logs -f app ```
### Остановка системы: ``` docker-compose down ```
### Проверка таблиц в БД: ``` docker-compose exec db psql -U postgres -d inventory_db -c "\dt" ```
