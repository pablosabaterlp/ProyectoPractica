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
3. ~~Crear mapa de calor del espacio~~

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
   - Cosmos DB
6. Azure Maps para visualizar
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
![](https://github.com/pablosabaterlp/ProyectoPractica/blob/be25ad011c5d4850bce849d54d9449f228f9ae7b/FaceRecognitionAzure/Extra/diagramapractica.drawio.png)

<p align="right">(<a href="#readme-top">Subir</a>)</p>

## Resumen Avance

|    Tema       | Tiempo |
| ------------- | ------------- |
| Reconocer Caras en Foto | ~~13/5/24 -> 15/5/24~~ |
| Reconocer Caras en Video | ~~15/5/24 -> 16/5/24~~ |
| Entrenar modelo para detectar puestos de trabajo | ~~17/5/24 -> 20/5/24~~ |
| Crear codigo para detectar puestos ocupados usando modelo | ~~17/5/24 -> 22/5/24~~ |
| Implementar utilización del blob storage y function | ~~22/5/24 -> 27/5/24~~ |
| Visualizar en Power BI| **27/6/24 -> 7/6/24** |
| EXTRA: Añadir aspecto reconocimiento facial | **Indeterminado** |
| Testing y Entrenamiento | **13/6/24 -> 17/6/24** |
| Presentación | **17/6/24 -> 19/6/24** |

<p align="right">(<a href="#readme-top">Subir</a>)</p>

## Demo

Reconocimiento en Fotos (15/5/24)

![](https://github.com/pablosabaterlp/ProyectoPractica/blob/866d609e9bd3f5f5792336910f7601ea52951a56/FaceRecognitionAzure/Extra/demo.gif)

Reconocimiento en Video (16/5/24)


## Iteraciones de Entrenamiento
### Iteracion 1 - Foto de oficina casi vacia y resultados de entrenamiento (20/5/24)
![](https://github.com/pablosabaterlp/ProyectoPractica/blob/ab9f93f33710ec95cf37bd0d9d0811cbed83c61b/FaceRecognitionAzure/Extra/EntrenamientoIter1.png)
![](https://github.com/pablosabaterlp/ProyectoPractica/blob/bde28e7c1f6d53ce78eca150dbe9d973b60bdd22/FaceRecognitionAzure/Extra/EntrenamientoTest4%20-%20Oficina.png)



### Iteracion 3 - Misma foto y resultados de entrenamiento (20/5/24)
![](https://github.com/pablosabaterlp/ProyectoPractica/blob/3cee4988938afeac8cac580c38dabbfb0551dfd7/FaceRecognitionAzure/Extra/Captura%20de%20pantalla%202024-05-20%20131357.png)
![](https://github.com/pablosabaterlp/ProyectoPractica/blob/0b9151d6a4e7e64c19ae3b6dfc2250d94fb207fe/FaceRecognitionAzure/Extra/TestOficina2.png)



<p align="right">(<a href="#readme-top">Subir</a>)</p>
## Referencias
* [Guias de Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/)

<p align="right">(<a href="#readme-top">Subir</a>)</p>




