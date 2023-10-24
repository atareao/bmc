user    := "atareao"
name    := `basename ${PWD}`
version := `git tag -l  | tail -n1`

default:
    @just --list

rebuild:
    echo {{version}}
    echo {{name}}
    docker build --no-cache \
                 -t {{user}}/{{name}}:{{version}} \
                 -t {{user}}/{{name}}:latest \
                 .
build:
    echo {{version}}
    echo {{name}}
    docker build -t {{user}}/{{name}}:{{version}} \
                 -t {{user}}/{{name}}:latest \
                 .

push:
    docker push {{user}}/{{name}}:{{version}}
    docker push {{user}}/{{name}}:latest

build-test:
    echo {{version}}
    echo {{name}}
    docker build -t {{user}}/{{name}}:test \
                 .
start:
    docker run --rm \
               --init \
               --name {{name}} \
               --detach \
               -p 5000:5000 \
               --volume $PWD/database:/app/database \
               --volume $PWD/templates:/app/templates \
               --env-file bmc_prod.env \
               {{user}}/{{name}}:latest
stop:
    docker stop {{name}}

run:
    gunicorn main:app -k uvicorn.workers.UvicornWorker \
             -w 1 \
             --chdir src \
             --threads 1 \
             --access-logfile - \
             -b 0.0.0.0:8000
