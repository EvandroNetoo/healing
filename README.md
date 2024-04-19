# Healing

---

<p align="center">
A system for doctors to register, schedule appointments, start consultations, send documents to their patients, and for patients to search for doctors, view their consultations, schedules, and documents. Besides, there's the authentication and authorization part.
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

This project is an online consultation system developed using the Django framework, along with technologies like Crispy Forms for more elegant forms and i18n for internationalization support. Additionally, the development environment is managed by Docker Compose, ensuring consistency and ease of configuration across different environments. The database used is PostgreSQL (psql), providing robustness and scalability to the system.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker compose
```
sudo apt-install docker-compose
```

- Git
```
sudo apt-get install git-all
```

### Installing

A step-by-step series of examples that tell you how to get a development environment running.

- Open terminal

- Clone the repository
```
git clone https://github.com/EvandroNetoo/healing.git
```

- Navigate to the directory
```
cd healing
```

- Create a dev.env file inside the dotenv_files folder based on dotenv_files/example.env


- Run the docker compose
```
sudo docker-compose.yaml up --build
```

- In another terminal, execute the migrations
```
sudo docker-compose django python manage.py migrate
```

- Create a superuser
```
sudo docker-compose django python manage.py createsuperuser
```

- Enter the username, email, and password

- The application will be running on port [127.0.0.1:8000/accounts/login](http://127.0.0.1:8000/accounts/login/)

## ⛏️ Built Using <a name = "built_using"></a>

- [Django](https://www.mongodb.com/) - Server Framework
- [Django crispy forms](https://expressjs.com/) - Have full control without writing custom form templates
- [Docker](https://www.docker.com/) - Accelerated Container Application Development
- [Docker compose](https://docs.docker.com/compose/) - A tool for defining and running multi-container applications
- [git](https://git-scm.com/) - Version control
- [bootstrap](https://getbootstrap.com/) - Build fast, responsive sites
