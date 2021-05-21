import io
import requests
import os
from google.cloud import vision


def analyze_picture(url):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    response = requests.get(url)
    image = vision.Image(content=response.content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    #if the label contains keywords, return true
    keywords = {'dog','mammal','Carnivore','wolf'}
    for label in labels:
        if label.description.lower() in keywords:
            return True
    return False

if __name__ == '__main__':
    res = analyze_picture('https://images.news18.com/ibnlive/uploads/2021/05/1620367611_untitled-design-2.jpg?impolicy=website&width=534&height=356')
    print(res)
