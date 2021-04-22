# tutorial_rest_udemy
```docker-compose run app sh -c "python manage.py test"
docker-compose run app sh -c "python manage.py test && flake8"

Так как мой интерпретатор пайтона 3.8 а в проекте 3.7 - команда python manage.py test && flake8 локально не запуститься. Только в докере так как там 3.7.

To optimize import using isort press ctrl + alt + o

docker-compose run --rm app sh -c "python manage.py test"
--rm to remove container after running command just to save local space 


docker build .

dcoker-compose up
docker-compose down

docker-compose 

ps                 List containers
images             List images
rm                 Remove stopped containers
kill               Kill containers
Commands:
  build              Build or rebuild services
  config             Validate and view the Compose file
  create             Create services
  down               Stop and remove resources
  events             Receive real time events from containers
  exec               Execute a command in a running container
  help               Get help on a command
  images             List images
  kill               Kill containers
  logs               View output from containers
  pause              Pause services
  port               Print the public port for a port binding
  ps                 List containers
  pull               Pull service images
  push               Push service images
  restart            Restart services
  rm                 Remove stopped containers
  run                Run a one-off command
  scale              Set number of containers for a service
  start              Start services
  stop               Stop services
  top                Display the running processes
  unpause            Unpause services
  up                 Create and start containers
  version            Show version information and quit

```