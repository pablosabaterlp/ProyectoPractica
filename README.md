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
4. Crear mapa de calor del espacio

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
6. Power BI para el mapa de calor
7. Camera
8. Fotos de Entrenamiento
   - Caras
   - Espacio

<p align="right">(<a href="#readme-top">Subir</a>)</p>

## Diseño
Proceso:
1. Si se detecta una persona, la cámara toma una foto (JPEG, PNG, o BMP) y la sube un Azure Stack Hub Blob Storage
2. El blob storage provoca una function de Azure
3. La funcion llama a un contenedor con el API de Custom Vision y Face para obtener información sobre la persona y decir el numero de puestos disponibles y donde se ubican
4. Los datos se envian a un Cosmos DB
5. Los puestos se represetan visualmente usando Power BI como disponibles u ocupados

Flowchart:
![](https://github.com/pablosabaterlp/ProyectoPractica/blob/505b96f94100560c1c3a6264817779b764c5df8c/FaceRecognitionAzure/Extra/dise%C3%B1o2.png)

<p align="right">(<a href="#readme-top">Subir</a>)</p>

## Resumen Avance

|    Tema       | Tiempo |
| ------------- | ------------- |
| Reconocer Caras en Foto | 13/5/24 -> 15/5/24 |
| Reconocer Caras en Video | 15/5/24 -> 16/5/24 |
| Entrenar modelo para detectar puestos de trabajo | 17/5/24 -> 20/5/24 |
| Crear codigo para detectar puestos ocupados usando modelo | 17/5/24 -> 22/5/24 |
| EXTRA: Añadir aspecto reconocimiento facial | 22/5/24 -> 27/5/24 |
| Implementar utilización del blob storage | 2/6/24 -> 5/6/24 |
| Implementar Cosmos DB, function, etc. | 5/6/24 -> 12/6/24 |
| Testing y Optimización | 13/6/24 -> 19/6/24 |

<p align="right">(<a href="#readme-top">Subir</a>)</p>

## Demo
![](https://github.com/pablosabaterlp/ProyectoPractica/blob/ffaff35eb07d07bdf7010be77ad22962302fb16a/FaceRecognitionAzure/Extra/demo.gif)

<p align="right">(<a href="#readme-top">Subir</a>)</p>
## Referencias
* [Guias de Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/)

<p align="right">(<a href="#readme-top">Subir</a>)</p>




