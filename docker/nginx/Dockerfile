FROM node:14 as builder

WORKDIR /app/frontend
COPY ./frontend/package*.json ./
RUN npm install
RUN npm install --upgrade -g @angular/cli@11.2.0
COPY ./frontend ./
RUN ng build

FROM nginx:alpine

ARG project_env
# nginx conf
ADD ./docker/nginx/$project_env/django.conf /etc/nginx/sites-enabled/default
ADD ./docker/nginx/nginx.conf /etc/nginx/nginx.conf

COPY --from=builder /app/frontend/dist ./app/frontend
COPY ./backend /app/backend

EXPOSE 80 443