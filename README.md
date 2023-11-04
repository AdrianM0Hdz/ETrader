An e comerce online platform that i implemented using ddd

Comming up

- [ ] Error system

Docker Development

run image:
``` {shell}
docker build --tag dev_image -f ./dockerfiles/development/api.Dockerfile .
```

run image: 

``` {shell}
docker run -it -p 5000:5000 -v ./app.py:/usr/ETrader/app.py -v ./requirements.txt:/usr/ETrader/requirements.txt -v ./app:/usr/ETrader/app dev_image
```
