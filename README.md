#### Evironment
- Python3
- Mac OS Catalina / Ubuntu 18.04

#### Project/App Setup
- Setup directory
```
mkdir __folder_name__ && cd $_

python3 -m venv venv
source vene/bin/activate

pip3 install -r requirements.txt
```

#### Run basic coverage
```
coverage run --source='.' manage.py test
coverage report
```

#### React Frontend
- Install Node
```
(Mac) brew install node
```
(Ubuntu) [steps](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-18-04)

- under the directory [frontend]
```
npm init -y
npm i webpack webpack-cli --save-dev
npm i @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev
npm i react react-dom --save-dev
npm run dev
```

#### Run
- At the root of the project
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
- Add data under the endpoint ```localhost:port/api/lead/```

#### Cypress Test
- At the root of the project
```
npm i cypress --save-dev
node_modules/.bin/cypress/ open
```

#### Celery with Redis as Broker
- Install Redis
```
pip3 install celery
(Mac) brew install redis
```
(Ubuntu) follow [directions](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04)


- On one terminal, start the redis server
```
(Mac) brew services start redis
(Ubuntu) sudo systemctl enable redis
```
- Check the connection is established with ```redis-cli```

- On another terminal, run the following
```
celery -A django_react worker --loglevel=DEBUG
celery -A django_react worker --beat -l info -S django
```
- Clear out redis connection after all the runs
```
(Mac) brew services stop redis
(Ubuntu) sudo systemctl stop redis
```
