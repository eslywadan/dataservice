# Cloud Deployment

## Deployment config 
The external folder (\\pdhdfs\datastudio) is mounted and used for storing the required config files, system logs, sqllite and redis data etc. Two folders are specified that the
(.\prd) is used for prodution environment and (.\test) is used for testing environment.

The same structurs are created for both environments and described as below: 
- (\dataapiaccount)    is used for dataapiaccount   
- (\dataapigrpc)       is used for dataapigrpc
- (\dataservice)	     is used for dataservice
- (\logs)              is reserved for telemetric data service
Layout

service/ext folder/project folder|image name| image tag|image build|container mount path 
 -| -| -|-|-
dataapiaccount|dataapiaccount|v002|         2022.06.19|app/ext
dataapigrpc|dataapigrpc|v002|2022.06.19|    service/ext
dataservice|dataservice|v002|2022.06.19|app/ext
dataservice-cache|redis|alpine|2022.05.05|data


Deployment (test env @tinxcloud)

service|CPU|Memory|port
-|-|-|-  
dataapiaccount|50|200|8080/tcp
dataapigrpc|100|200|23335/tcp
dataservice|300|1000|8080/tcp
dataservice-cache|50|600|6379/tcp



Layout (prod env @inxcloud)

service/ext folder/project folder|image name| image tag|image build|container mount path 
-|-|-|-|- 
dataapiaccount|dataapiaccount|v01|2022.06.19|app/ext
dataapigrpc||dataapigrpc|v002|2022.06.19|service/ext
dataservice|dataservice|v002|2022.06.19|app/ext
dataservice-cache|redis|alpine|2022.05.03|data

Deployment (prod env @inxcloud)
limit CPU    1000m
limit Memory 1024m

service|CPU|Memory|port
-|-|-|- 
dataapiaccount|100|100|8080/tcp
dataapigrpc|200|100|23335/tcp
dataservice|600|500|8080/tcp
dataservice-cache|100|300|6379/tcp


###### tags: `Data Studio`
