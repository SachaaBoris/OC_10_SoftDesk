# OC_10 SoftDesk Support 

<p align="center"><img src="https://github.com/SachaaBoris/OC_10_SoftDesk/blob/main/softdesk_logo.png" width="300"/></p>
  
# ● Description du projet  
SoftDesk Support est un outil de suivi de projet / gestion des problèmes techniques collaboratif. Développé en architecture API django Rest, elle s'adresse aux entreprises en Business to Business.  
  
# ● Comment installer et démarrer l'application  
1. Prérequis :  
    Avoir Python 3 installé  
    Avoir téléchargé et dézipé l'archive du projet sur votre disque dur,  
    Ou clonez le repo avec cette commande :  
  ```  
  git clone https://github.com/SachaaBoris/OC_10_SoftDesk.git "local\folder"
  ```  
  
2. Générer et utiliser une clé secrète Django :  
	Rendez-vous sur https://djecrety.ir/ et générez une clé que vous pourrez coller dans le fichier .env.sample situé à la racine du projet.  
	Rennomez .env.sample en .env  
  
3. Installer l'environnement virtuel :  
    Depuis votre console favorite, naviguez jusqu'au répertoire du projet  
    Pour créer l'environnement virtuel rentrez la ligne de commande : `py -m venv ./venv`  
    Activez ensuite l'environnement virtuel en rentrant la commande : `venv\Scripts\activate`  
    Installer les requirements du projet avec la commande : `py -m pip install -r requirements.txt`  
  
4. Démarrer le serveur :  
    Toujours dans la console et à la racine du projet, tapez la commande : `py softdesk/manage.py runserver`  
	Rendez-vous dans votre navigateur et allez à l'adresse :  
	http://127.0.0.1:8000 ou http://localhost:8000/  
  
:black_circle:  

# ● Etapes supplémentaires facultatives  
5. Démarrer une nouvelle BDD :  
	Quittez le serveur (CTRL+C dans la console) si vous l'avez lancé et supprimez le fichier db.sqlite3  
	Et rentrer les commandes suivantes pour créer une nouvelle BDD
  ``` 
  py softdesk/manage.py makemigrations
  py softdesk/manage.py migrate
  ``` 
  
6. Créer un SuperUser :  
	Rentrez la commande suivante et suivez les instructions  
  ``` 
	py softdesk/manage.py createsuperuser
  ```  
  
7. Noubliez pas de switcher ces valeurs avant mise en production :  
	dans les settings du projet, DEBUG = False & ajustez SIMPLE_JWT token lifetime  
	vous pouvez également éditer pagination.py : page_size  
	
  
:black_circle:  

# ● Documentation de l'API :scroll:  

## Obtain Admin token

```
POST {{base_url}}/softdesk_api/login/
```

This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.

A successful POST request typically returns a `200 OK` or `201 Created` response code.

### Request

> 
> **Body**
> 
> ```
> {
>   "username": "user",
>   "password": "@123456789"
> }
> ```
> 

## Obtain User token

```
POST {{base_url}}/softdesk_api/login/
```

This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.

A successful POST request typically returns a `200 OK` or `201 Created` response code.

### Request

> 
> **Body**
> 
> ```
> {
>   "username": "user",
>   "password": "@123456789"
> }
> ```
> 

## Refresh Token

```
POST {{base_url}}/softdesk_api/login/refresh/
```

This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.

A successful POST request typically returns a `200 OK` or `201 Created` response code.

### Request

> 
> **Body**
> 
> ```
> {
>   "username": "user",
>   "password": "@123456789"
> }
> ```
> 

## User list

```
GET {{base_url}}/softdesk_api/users/
```



## User

```
POST {{base_url}}/softdesk_api/users/
```

This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.

A successful POST request typically returns a `200 OK` or `201 Created` response code.

### Request

> 
> **Body**
> 
> ```
> {
>   "email": "user@example.com",
>   "username": "users_name",
>   "password": "@123456789",
>   "password_confirm": "@123456789",
>   "dob": "1999-10-22",
>   "can_be_contacted": true,
>   "can_data_be_shared": false
> }
> ```
> 

## User

```
GET {{base_url}}/softdesk_api/users/#/
```



## User

```
PUT {{base_url}}/softdesk_api/users/#/
```



### Request

> 
> **Body**
> 
> ```
> {

>   "email": "user@example.com",

>   "username": "users_name",

>   "password": "@123456789",

>   "dob": "1984-11-22"

> }
> ```
> 

## User

```
DELETE {{base_url}}/softdesk_api/users/#/
```



## Project list

```
GET {{base_url}}/softdesk_api/projects/
```



## Project

```
POST {{base_url}}/softdesk_api/projects/
```



### Request

> 
> **Body**
> 
> ```
> {

>   "title": "Project title",

>   "description": "Project description.",

>   "type": "Front-End",

>   "contributors": ["username1","username2"]

> }
> ```
> 

## Project

```
GET {{base_url}}/softdesk_api/projects/#/
```



## Project

```
PUT {{base_url}}/softdesk_api/projects/#/
```



### Request

> 

## Project

```
DELETE {{base_url}}/softdesk_api/projects/#/
```



## Contributors list

```
GET {{base_url}}/softdesk_api/projects/#/contributors/
```



## Contributors

```
POST {{base_url}}/softdesk_api/projects/#/contributors/
```



### Request

> 
> **Body**
> 
> ```
> {

>   "contributors": ["username1", "username2"]

> }
> ```
> 

## Contributor info (user info)

```
GET {{base_url}}/softdesk_api/projects/#/contributors/#/
```



## Contributors

```
DELETE {{base_url}}/softdesk_api/projects/#/contributors/#/
```



## Issue list

```
GET {{base_url}}/softdesk_api/projects/#/issues/
```



## Issue

```
POST {{base_url}}/softdesk_api/projects/#/issues/
```



### Request

> 
> **Body**
> 
> ```
> {

>   "title": "Issue title",

>   "description": "Issue description",

>   "tag": "BUG",

>   "priority": "ÉLEVÉE",

>   "status": "EN COURS",

>   "assigned_user": #

> }
> ```
> 

## Issue

```
GET {{base_url}}/softdesk_api/projects/#/issues/#/
```



## Issue

```
PUT {{base_url}}/softdesk_api/projects/#/issues/#/
```



### Request

> 

## Issue

```
DELETE {{base_url}}/softdesk_api/projects/#/issues/#/
```



## Comment list

```
GET {{base_url}}/softdesk_api/projects/#/issues/#/comments/
```



## Comment

```
POST {{base_url}}/softdesk_api/projects/#/issues/#/comments/
```



### Request

> 
> **Body**
> 
> ```
> {

>   "description": "Users comment."

> }
> ```
> 

## Comment

```
GET {{base_url}}/softdesk_api/projects/#/issues/#/comments/#/
```



## Comment

```
PUT {{base_url}}/softdesk_api/projects/#/issues/#/comments/#/
```



### Request

> 

## Comment

```
DELETE {{base_url}}/softdesk_api/projects/#/issues/#/comments/#/
```


---  
  
[![CC BY 4.0][cc-by-shield]][cc-by]  
  
This work is licensed under a [Creative Commons Attribution 4.0 International License][cc-by].  
  
[cc-by]: http://creativecommons.org/licenses/by/4.0/  
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg  
