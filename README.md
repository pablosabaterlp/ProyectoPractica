<a name="readme-top"></a>

<img src="https://github.com/pablosabaterlp/ProyectoPractica/blob/ed0d9f0270ed7b5f40ddbe08d3e6fd75f3939a36/Archivos%20Extra/Banco_Santander_Logotipo.svg.png" width="400" height="75"/>

## About the Project

The main goal of this project is to use Azure Computer Vision and Custom Vision resources to train a model capable of detecting free or occupied workstations in an office. Additionally, the project aims to implement Face API to create a facial recognition system in the same context.

## Deliverables

The main deliverables are as follows:
1. Detect free workstations/create a map
2. Identify people
   - Name
   - Age
   - Etc.

## Architecture

The components used in this project include:
1. Visual Studio Code/Python
2. Azure Gen AI resources:
   - Computer Vision
   - Custom Vision
   - Face API
3. Azure resources for data flow:
   - Blob Storage
   - Functions
4. Visualization tools:
   - Power BI
   - HTML
   - Excel
   - JavaScript
5. Camera
6. Training Photos
   - Faces
   - Workspace

<p align="right">(<a href="#readme-top">Back to Top</a>)</p>

## Design
Process:
1. Every 5 minutes, the camera captures a photo (JPEG, PNG) and directly uploads it to Azure Blob Storage.
2. The blob storage triggers an Azure Function.
3. The function calls a container with the Custom Vision and Face APIs to gather information about the person and the occupied or unoccupied workstations.
4. The data is sent to a Cosmos DB, and the workstation statuses are updated in an Excel file.
5. The workstations are visually represented using Power BI and the Excel file uploaded to SharePoint.

Flowchart:
![](https://github.com/pablosabaterlp/ProyectoPractica/blob/9a43a92e3e215551bd4426be3499da2850820327/FaceRecognitionAzure/Extra/DataFlowFinal.png)

<p align="right">(<a href="#readme-top">Back to Top</a>)</p>

## Progress Summary

|    Task       | Timeline |
| ------------- | -------- |
| Learning Azure and brainstorming project ideas | ~~8/5/24 -> 13/5/24~~ |
| Creating facial recognition for photos and videos | ~~13/5/24 -> 15/5/24~~ |
| Training a Custom Vision model to detect workstations | ~~16/5/24 -> 20/5/24~~ |
| Coding to detect occupied workstations using the model | ~~17/5/24 -> 22/5/24~~ |
| Implementing Blob Storage and Azure Functions | ~~22/5/24 -> 27/5/24~~ |
| Visualizing in Power BI | ~~27/5/24 -> 7/5/24~~ |
| ~~Implementing "clustering" for workstations~~ | ~~4/6/24 -> 10/6/24~~ |
| Building HTML as a Power BI alternative | ~~03/06/24 -> 10/06/24~~|
| ~~EXTRA: Adding facial recognition features~~ | ~~10/6/24 -> 17/6/24~~ |
| Testing and training | ~~17/6/24 -> 19/6/24~~ |
| Presentation | ~~17/6/24~~ |

<p align="right">(<a href="#readme-top">Back to Top</a>)</p>

## Demo

### Photo Recognition (15/5/24)

![](https://github.com/pablosabaterlp/ProyectoPractica/blob/866d609e9bd3f5f5792336910f7601ea52951a56/FaceRecognitionAzure/Extra/demo.gif)

### Office Map (27/5/24)
![](https://github.com/pablosabaterlp/ProyectoPractica/blob/c7ccb23e826f95186ccb5b2da5cfe84e92964530/FaceRecognitionAzure/Extra/Mapa%20de%20Oficina.png)

### Power BI Dashboard (31/5/24)
https://app.powerbi.com/view?r=eyJrIjoiMTUwMWI4ZWQtMDM3Ni00NGFhLThlODYtNDI4YTA2ZGZiMmRmIiwidCI6ImE4ZWVjMjgxLWFhYTMtNGRhZS1hYzliLTlhMzk4YjkyMTVlNyIsImMiOjN9

## How to Use
### Installation
The program uses the following libraries:
* azure-functions
* msrest.authentication
* numpy
* requests
* opencv-python
* azure.storage.blob
* azure.cognitiveservices
* scikit-learn

These are listed in the `requirements.txt` file, and you can install them by running the following in your terminal:
 ```sh
   pip install -r requirements.txt
   ```
The Azure Function this program depends on was created using Azure Core Tools, which can be installed on the device if necessary by following this [link](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python). 
Lastly, using Azure's features requires a key and endpoint for each service. The 'read_line.py' script facilitates the implementation of these keys by storing them locally in a .txt file.

### Visualization in Power BI
To represent the results of the Custom Vision program, a Power BI map using Synoptic Design was chosen. This map is designed manually, and Synoptic Design enables the representation of data from an Excel file. As shown in the Power BI demo above, the program uploads the Custom Vision API results to an Excel file, marking workstations as occupied or free based on 0 or 1 (0 is free). The map then represents a workstation in green or red based on the information in the Excel file.

### Visualization in HTML
Another way to represent the results is by using a local website created with JavaScript and HTML. While the free version of Power BI is functional, it limits the program's implementation, for example, in automatic visual updates. For this reason, the same functionality was recreated using HTML. In this case, workstations can be updated automatically without writing to an Excel file, making this approach potentially more optimized. These files are located as 'app.js' and 'map.html'.


<p align="right">(<a href="#readme-top">Back to Top</a>)</p>

## References
* [Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/)
* [Azure Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python)
* [Floor Plan Power BI](https://www.youtube.com/watch?v=18UJYvl_c8s)

<p align="right">(<a href="#readme-top">Back to Top</a>)</p>




