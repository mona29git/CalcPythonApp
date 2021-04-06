## Objective: 
This program is a demo of running a web application using the python flask.
In this web app a basic calculator is created which can be accessed by different user/sessions. The calculator shows the top 10 history of the calculation.

## Run Methods:
#### **1. Local Run:** In this method we can run the python program after launching the docker run of the redis. Once the docker is started in the local the command "docker run --name my-redis -d -p 6379:6379 redis" is the simplest method to launch the redis instance. Once the redis is up, you can run main.py file and navigating to http://0.0.0.0:5000/ can show the web app.

#### **2. Local Docker Run:** In this method both the web program and Redis are bundled into a single docker image. And once the images is composed up we can navigate to http://0.0.0.0:5000/ to see the web app. To compose it, go to the basicCalcApp directory and run docker-compose up.

#### **3. Cloud host:** In this particular example I have used the heroku for the simplicty in hosting the docker image. This same program is running under the address: https://calculatorappmonalisa.herokuapp.com/
Please follow the heroku guidelines for deploying the docker.

## Out Of Scope:
We have used the Heroku host this web application. The scalabilty of the app and the redis is managed by Heroku.
But followings are out of scope in this project but can be easily managed in Heroku.
1. The Heroku free account is used with the nano redistogo, so the number of the connection is limited (10). Separate effort can be done to increase it.
2. The redis console should be managed to handle the number of keys and monitoring the web app health. The RedisMonitor provided by Heroku can be used.
3. The top 10 history is kept even if the calculation is invalid, this functionality can be changed easily. We have coded it this way to log what ever the calculation is done by user.
