import numpy as np
import cv2

def draw_results(path, results):
    img = cv2.imread(path)
    resolution = img.shape
    for prediction in results.predictions:
        if prediction.probability > 0.8:
            left = int(prediction.bounding_box.left * resolution[0])
            top = int(prediction.bounding_box.top * resolution[1])
            width = int(prediction.bounding_box.width * resolution[0])
            height= int(prediction.bounding_box.height * resolution[1])
            if prediction.tag_name == "Occupied":
                cv2.rectangle(img, (left,top), (left+width,top+height), (0,255,0), 2)
            elif prediction.tag_name == "Unoccupied":
                cv2.rectangle(img, (left,top), (left+width,top+height), (0,0,255), 2)
    cv2.imwrite('WorkspaceWithBoxes.jpg', img)
    cv2.imshow('WorkspaceWithBoxes', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows
