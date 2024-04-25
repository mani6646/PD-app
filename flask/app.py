from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from torch import nn
from PDS.PDS import functions as pds
from torchvision.models import resnet18
from PIL import Image
from torchvision import transforms
import os

app = Flask(__name__)
CORS(app)

# Load the pre-trained model
CNN_backbone = resnet18(pretrained=True)
CNN_backbone.fc = nn.Flatten()

#Spiral model
model_spiral = pds.PrototypicalNetworks(CNN_backbone)
model_spiral.load_state_dict(torch.load('parkinson_spiral_model.pth',map_location=torch.device('cpu')))
model_spiral.eval()

#Wave model
model_wave = pds.PrototypicalNetworks(CNN_backbone)
model_wave.load_state_dict(torch.load('parkinson_wave_model.pth',map_location=torch.device('cpu')))
model_wave.eval()

support_set_data_spiral = torch.load('support_set_data_spiral.pth', map_location=torch.device('cpu'))
support_set_data_wave = torch.load('support_set_data_wave.pth', map_location=torch.device('cpu'))

#support data for spiral
loaded_support_images_spiral = support_set_data_spiral['images']
loaded_support_labels_spiral = support_set_data_spiral['labels']

#support data for wave
loaded_support_images_wave = support_set_data_wave['images']
loaded_support_labels_wave = support_set_data_wave['labels']


image_transform = transforms.Compose([
    transforms.Resize((300, 600)),  # Adjust size as per your model's input size
    transforms.ToTensor(),
])

# Define a function to process the uploaded image and make predictions
def predict_parkinsons(model, support_images, support_labels, query_image_path):
    # Load and preprocess the query image
    query_image = Image.open(query_image_path)
    query_input_tensor = image_transform(query_image)
    query_input_tensor = query_input_tensor.unsqueeze(0)
    query_input_tensor = query_input_tensor  

    # Perform inference
    with torch.no_grad():
        output = model(support_images, support_labels, query_input_tensor)

    # Assuming your model outputs class probabilities
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    predicted_class = torch.argmax(probabilities).item()

    return predicted_class

@app.route('/upload/<name>', methods=['POST'])
def upload_image(name):
    if name == "spiral":
        #/upload/spiral
        model = model_spiral
        support_image = loaded_support_images_spiral
        support_labels = loaded_support_labels_spiral
    else:
        #/upload/wave
        model = model_wave
        support_image = loaded_support_images_wave
        support_labels = loaded_support_labels_wave
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        result = predict_parkinsons(model, support_image, support_labels, file_path)
        if result:
            return jsonify({'result':"The image classified is Healthy"})
        else:
            return jsonify({'result': "Parkinson's disease detected"})

if __name__ == '__main__':
    app.run(debug=True)