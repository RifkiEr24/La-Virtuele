# La Virtuele
Official Website of La Virtuele Streetwear Clothing Store

# Setting Up Development Server
Before you proceed in to the next step, you will need to have both Python and Node installed in your machine.

__First Time Setup__

Run the shell script.
```
setup.sh
```
You only need to do this once.<br>

__Running The Development Server__

This project has a completely separated client and server app.

__Run Django Server__

You need a python virtual environment (named 'env' if possible) inside the backend directory.<br>
If you named your virtual environment other than 'env', kindly change the djserver.sh script to your needs.<br>
The djserver.sh script may be slow since it's always installing the requirements and check for migrations.<br>

```
# Create the env folder
python -m pip install virtualenv
virtualenv backend/env
backend/djserver.sh
```

__Run Dockerize Django Server__

Other than the conventional way to run a django project as mentioned above.<br>
You can also use docker, but you need to have both docker and docker-compose available on your PATH.<br>

#### Development Container
```
docker-compose up --build
```
#### Deployment Container

```
docker-compose -f docker-compose-deploy.yml up --build
```

__Run Vue App__

The first thing you need to do is change your working directory to the frontend folder, then run npm install.<br>
If the installation is successfully completed, you can run npm run serve to start the app.
```
cd frontend
npm install
npm run serve
```


### Contributors
* **Muhammad Rifki Erlangga** - [Github](https://github.com/RifkiEr24)
* **Hariz Sufyan Munawar** - [Github](https://github.com/harizMunawar)
* **Candra Miftah Firdausy** - [Github](https://github.com/CandraMF)
