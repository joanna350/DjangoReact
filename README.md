#### Evironment
- Python3
- Mac OS

#### Project/App Setup
- Setup directory
```
mkdir __folder_name__ && cd $_

python3 -m venv venv
source vene/bin/activate

pip3 install django djangorestframework
```

#### Run coverage with
```
coverage run --source='.' manage.py test
coverage report
```

#### React Frontend
- Install Node
```
brew install node
```

- Ready to use Node Package Manager
```
./frontend
npm init -y
npm i webpack webpack-cli --save-dev
npm i @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev
npm i react react-dom --save-dev
npm run dev
```

#### Run
```
python3 manage.py runserver
```
- Add data under the endpoint 'localhost:port/api/lead/'
