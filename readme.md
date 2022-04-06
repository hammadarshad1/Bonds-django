![Python version](https://img.shields.io/badge/Python-version>=3.6-green) ![Django version](https://img.shields.io/badge/django-v3.2.5,<3.3.0-blue)
# Django-Bonds


## Getting started

To clone repository on your local machine, please follow these steps:

```
git clone https://github.com/hammadarshad1/Bonds-django
cd Bonds-django
```

# Installation setup

In order to run the project you need to have `Docker` installed on your system.

### Windows Guide
To install `Docker` in windows Follow the official [documentation](https://docs.docker.com/desktop/windows/install/)

### Linux Guide (Debian)
open your terminal and let's install `Docker` for your system, but before installing you need to make sure that you have updated OS
```
$ sudo apt-get update
```
now, its done let's start by installing dependencies for `Docker`
```
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```
Add Docker’s official __GPG__ key:
```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

Use the following command to set up the __stable__ repository. To add the nightly or test repository, add the word nightly or test (or both) after the word stable in the commands below.
```
$ echo \ "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \ $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Install a `Docker` engine:
```
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### MacOS Guide
To install `Docker` in __MacOS__ Follow the official [documentation](https://docs.docker.com/desktop/mac/install/).

# Setting up the project
Before setting up the project we need to install `docker-compose` in a system. Follow the official [documentation](https://docs.docker.com/compose/install/) to install.

Create a `.env` file while copying the contents from the `.env.example` file.
```
cp .env.example .env
```

To make a docker build:
```
$ docker-compose build
```

## Usage

```
$ docker-compose up
```

## Testing
```
$ docker-compose run --rm app sh -c "python manage.py test && flake8"
```

## APIs Docs:
For Swagger API documentation visit: `http://localhost:8000/api-docs`
