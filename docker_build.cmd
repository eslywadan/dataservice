docker build -t dataservice:basev001 . -f buildbase\Dockerfile
docker build -t dataservice:workerv001 . -f buildcw\Dockerfile
docker build -t dataservice:flowerv001 . -f buildfl\Dockerfile
docker build -t dataservice:apiportv001 . -f buildgw\Dockerfile