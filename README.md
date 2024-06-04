**Название приложения**: ToDoMany

**Описание проекта**:

ToDoMany - это веб-приложение, разработанное для управления задачами и комментариями в различных рабочих окружениях. Оно предоставляет возможность создания задач, их назначения, отслеживания статуса выполнения и обсуждения в комментариях. Пользователи могут работать в различных окружениях, где могут просматривать задачи, назначенные на них или других участников, а также добавлять комментарии.

**Функциональность**:

1. **Аутентификация и авторизация**:
   - Пользователи могут регистрироваться и аутентифицироваться в системе.
   - Для безопасного доступа к данным используется JWT-аутентификация.

2. **Управление пользователями**:
   - Пользователи могут создавать новые учетные записи.
   - Пользователи могут просматривать информацию о своем профиле.

3. **Управление задачами**:
   - Пользователи могут создавать новые задачи, указывая их описание и другие атрибуты.
   - Задачи могут быть назначены на конкретных пользователей.
   - Пользователи могут отмечать задачи как завершенные.

4. **Управление комментариями**:
   - Пользователи могут добавлять комментарии к задачам.
   - Комментарии могут быть иерархическими, т.е. могут иметь дочерние комментарии.
   - Пользователи могут удалять свои комментарии.

5. **Управление окружениями**:
   - Пользователи могут создавать различные рабочие окружения (например, проекты или команды).
   - Задачи и комментарии могут быть организованы в рамках определенных окружений.

6. **Управление администраторами окружений**:
   - Пользователи могут быть добавлены в качестве администраторов для определенных окружений.
   - Администраторы могут управлять задачами и комментариями в своих окружениях.

7. **Документирование API**:
   - API проекта документируется с использованием Swagger.

**Технологии**:

- **Backend**:
  - Язык программирования: Python
  - Фреймворк: Django
  - Библиотеки: Django REST Framework, drf-yasg, rest_framework_simplejwt
  - База данных: PostgreSQL

- **Frontend**:
  - Фреймворк: React.js
  - Управление состоянием: Redux
  - Библиотеки: React Router, Axios

- **Аутентификация и авторизация**:
  - JSON Web Tokens (JWT)

**Интерфейс**:
Интерфейс приложения представлен в виде веб-страниц с использованием современных средств стилизации и визуализации, обеспечивающих удобство использования и приятный пользовательский опыт. В приложении реализованы различные страницы для управления задачами, комментариями, профилем пользователя и другими функциями.


## Установка и запуск

Чтобы запустить проект локально, выполните следующие шаги:

1. Склонируйте репозиторий на локальную машину.
2. Установите зависимости, используя `pip install -r requirements.txt`.
3. Примените миграции базы данных: `python manage.py migrate`.
4. Создайте суперпользователя: `python manage.py createsuperuser`.
5. Запустите сервер: `python manage.py runserver`.
6. Перейдите по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/) в вашем браузере.

Ибо можете перейти по ссылке https://todomany-17c00a7d561d.herokuapp.com/
