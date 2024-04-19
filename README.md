# Healing

---

<p align="center">
Um sistema para médicos realizarem seu cadastro, liberar horarios, iniciar consultas, enviar documentos para seus pacientes e pacientes poderem procurar médicos, ver suas consutas, horários e documentos. Fora a parte de autenticação e autorização.
</p> 

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

Este projeto é um sistema de consultas online desenvolvido utilizando o framework Django, juntamente com tecnologias como Crispy Forms para formulários mais elegantes e i18n para suporte a internacionalização. Além disso, o ambiente de desenvolvimento é gerenciado por Docker Compose, garantindo a consistência e facilidade de configuração em diferentes ambientes. O banco de dados utilizado é o PostgreSQL (psql), proporcionando robustez e escalabilidade ao sistema.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- docker compose
```
sudo apt-install docker-compose
```

- git
```
sudo apt-get install git-all
```

### Installing

A step by step series of examples that tell you how to get a development env running.

- Open terminal

- Clone the repository
```
git clone https://github.com/EvandroNetoo/healing.git
```

- Enter on directory
```
cd healing
```

- Run the docker compose
```
sudo docker-compose.yaml up --build
```

- On other terminal execute the migations
```
sudo docker-compose django python manage.py migrate
```

- Create a super user
```
sudo docker-compose django python manage.py createsuperuser
```

- enter the username, email and password

- the aplication will be running on port [127.0.0.1:8000/accounts/login](http://127.0.0.1:8000/accounts/login/)

## ⛏️ Built Using <a name = "built_using"></a>

- [Django](https://www.mongodb.com/) - Server Framework
- [Django crispy forms](https://expressjs.com/) - Have full control without writing custom form templates
- [Docker](https://www.docker.com/) - Accelerated Container Application Development
- [Docker compose](https://docs.docker.com/compose/) - A tool for defining and running multi-container applications
- [git](https://git-scm.com/) - Versionamento do código
- [bootstrap](https://getbootstrap.com/) - Build fast, responsive sites
