<a name="readme-top"></a>

## Sobre el Proyecto

Este proyecto tiene como objectivo principal usar los recursos de Azure Computer Vision y Custom Vision para entrenar un modelo que sea capaz de detectar puestos libres u ocupados en una oficina. Como extension se queria implementar el uso de Face API para crear un sistema de reconocimiento facial en el mismo contexto.

## Entregables

Los entregables principales son los siguentes:
1. Detectar puestos libres/crear un mapa
2. Identificar personas
   - Nombre
   - Edad
   - Etc.

## Arquitectura

Como componentes se utilizaran los siguentes:
1. Visual Studio Code/Python
2. Recursos Azure Gen AI:
   - Computer Vision
   - Custom Vision
   - Face API
4. Recursos Azure para el Dataflow:
   - Blob Storage
   - Function
6. Poqer BI para visualizar
7. Camera
8. Fotos de Entrenamiento
   - Caras
   - Espacio

<p align="right">(<a href="#readme-top">Subir</a>)</p>

## Diseño
Proceso:
1. Cada 5 minutos, la cámara toma una foto (JPEG, PNG) y la sube un Azure Blob Storage directamente
2. El blob storage provoca una function de Azure
3. La funcion llama a un contenedor con el API de Custom Vision y Face para obtener información sobre la persona y los puestos ocupados y desocupados
4. Los datos se envian a un Cosmos DB y el estado de los puestos se actualiza en un excel
5. Los puestos se represetan visualmente usando Power BI y el excel subido a un Sharepoint

Flowchart:
![](https://github.com/pablosabaterlp/ProyectoPractica/blob/9a43a92e3e215551bd4426be3499da2850820327/FaceRecognitionAzure/Extra/DataFlowFinal.png)

<p align="right">(<a href="#readme-top">Subir</a>)</p>

## Resumen Avance

|    Tema       | Tiempo |
| ------------- | ------------- |
| Aprender sobre Azure y sacar ideas para proyecto | ~~8/5/24 -> 13/5/24~~ |
| Crear reconocimiento de caras en foto y video | ~~13/5/24 -> 15/5/24~~ |
| Entrenar modelo Custom Vision para detectar puestos de trabajo | ~~16/5/24 -> 20/5/24~~ |
| Crear código para detectar puestos ocupados usando modelo | ~~17/5/24 -> 22/5/24~~ |
| Implementar utilización del blob storage y function | ~~22/5/24 -> 27/5/24~~ |
| Visualizar en Power BI | ~~27/5/24 -> 7/5/24~~ |
| Implementar "clustering" para puestos | **4/6/24 -> 10/6/24** |
| EXTRA: Añadir aspecto reconocimiento facial | **10/6/24 -> 17/6/24** |
| Testing y Entrenamiento | **17/6/24 -> 19/6/24** |
| Presentación | **17/6/24 -> 19/6/24** |

<p align="right">(<a href="#readme-top">Subir</a>)</p>

## Demo

### Reconocimiento en Fotos (15/5/24)

![](https://github.com/pablosabaterlp/ProyectoPractica/blob/866d609e9bd3f5f5792336910f7601ea52951a56/FaceRecognitionAzure/Extra/demo.gif)

### Mapa de Oficina (27/5/24)
![](https://github.com/pablosabaterlp/ProyectoPractica/blob/c7ccb23e826f95186ccb5b2da5cfe84e92964530/FaceRecognitionAzure/Extra/Mapa%20de%20Oficina.png)

### Power BI Dashboard (31/5/24)
https://app.powerbi.com/view?r=eyJrIjoiMzNmYTRhMzUtODM5Yi00N2M0LThkNmEtYjc1NDJiNjI1YTk4IiwidCI6ImE4ZWVjMjgxLWFhYTMtNGRhZS1hYzliLTlhMzk4YjkyMTVlNyIsImMiOjN9

## Como Utilizar
### Instalación
El programa utiliza las siguentes librerias:
* azure-functions
* msrest.authentication
* numpy
* requests
* opencv-python
* azure.storage.blob
* azure.cognitiveservices
* scikit-learn

Estas se encuentran en el documento `requirements.txt`, y para installar se puedo copiar lo siguente al terminal:
 ```sh
   pip install -r requirements.txt
   ```
Aparte de las librerias, los documentos de `captureAndUpload.py`, y `read_line.py`, son importantes para la instalación. Sirve tambien copiar los contenidos al documento principal `function_app.py`, pero estan por separados para simplificar el entendimiento.

El Azure Function del cual este programa depende se creo utilizando Azure Core Tools, el cual se puede installar en el dispositivo sea necesario siguiendo este [link](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python). Por último, para usar las funciones de Azure se requiere una llave y endpoint para cada uno. El codigo de 'read_line.py' facilita la implementacion de estas llaves de forma que esten guardadas localmente en un documento .txt.

### Implementación Power BI
Para representar los resultados del programa Custom Vision, se eligio usar un mapa de Power BI y Synoptic Design. Este mapa se diseña manualmente y usando Synoptic Design es posible representar data de un archivo Excel. Como se puede ver en el demo de Power BI arriba, el programa sube los resultados del API Custom Vision a un Excel como occupados o libres en base de 0 o 1 (0 es libre). El mapa entonces representa un puesto en verde o rojo dependiendo de la información en el Excel.  

<p align="right">(<a href="#readme-top">Subir</a>)</p>

## Referencias
* [Guias de Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/)
* [Guia de Azure Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python)
* [Floor Plan para Power BI](https://www.youtube.com/watch?v=18UJYvl_c8s)

<p align="right">(<a href="#readme-top">Subir</a>)</p>




