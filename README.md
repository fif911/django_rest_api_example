# tutorial_rest_udemy
docker-compose run app sh -c "python manage.py test"
docker-compose run app sh -c "python manage.py test && flake8"

Так как мой интерпретатор пайтона 3.8 а в проекте 3.7 - команда python manage.py test && flake8 локально не запуститься. Только в докере так как там 3.7.

To optimize import using isort press ctrl + alt + o

docker-compose run --rm app sh -c "python manage.py test"
--rm to remove container after running command just to save local space 
