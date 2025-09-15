# Базовый образ
FROM nginx:stable-alpine

# Копируем конфиг nginx
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Копируем файлы фронтенда (без ./frontend)
COPY . /usr/share/nginx/html

# Открываем порт
EXPOSE 80

# Автозапуск nginx (по умолчанию уже в base image)
CMD ["nginx", "-g", "daemon off;"]
