# Управление задачами (Task Management) на Django


## Описание проекта<a name="description"></a>
Task manager - приложение для управления задачами, включая создание, просмотр, редактирование и удаление задач, а также учет времени выполнения и трудозатрат. Иерархия задач представлена в виде дерева.


### Используемый стек<a name="stack"></a>

[![Python][Python-badge]][Python-url]
[![Django][Django-badge]][Django-url]
[![Postgres][Postgres-badge]][Postgres-url]

### Системные требования
- Python 3.11+;
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)


### Установка проекта локально <a name="local-install"></a>

1. **Склонировать репозиторий:**

   ```bash
   git clone https://github.com/VitaliyDrozdov/task-management.git
   cd task_manager

2. **Установить poetry**
### Установка<a name="install"></a>

1. Установите poetry следуя [инструкции с официального сайта](https://python-poetry.org/docs/#installation).
2. После установки перезапустите оболочку и введите команду
```SHELL
poetry --version

3. Копируем файл **.env.example** с новым названием **.env** и заполняем его необходимыми данными:

```shell
cp .env.example .env
```
```shell
nano .env
```

4. Подготавливаем бэкенд к работе:

```shell
python manage.py migrate
```

5. Наполняем БД данными заданий:

```shell
python manage.py loaddata initial_tasks.json
```

## Запуск проекта локально (без docker)<a name="local-run"></a>

Если нужен доступ в админскую часть для управления данными, создаем администратора:

```shell
python manage.py createsuperuser
```

Для запуска используем команду:

```shell
python manage.py runserver
```

http://localhost:8000/


<!-- MARKDOWN LINKS & BADGES -->

[Python-url]: https://www.python.org/

[Python-badge]: https://img.shields.io/badge/Python-376f9f?style=for-the-badge&logo=python&logoColor=white

[Django-url]: https://github.com/django/django

[Django-badge]: https://img.shields.io/badge/Django-0c4b33?style=for-the-badge&logo=django&logoColor=white


[Postgres-url]: https://www.postgresql.org/

[Postgres-badge]: https://img.shields.io/badge/postgres-306189?style=for-the-badge&logo=postgresql&logoColor=white
