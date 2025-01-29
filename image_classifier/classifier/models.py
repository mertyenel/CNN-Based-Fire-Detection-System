# classifier/model.py

import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import os

# CNN Modeli (Eğitim Kodunuza Göre Güncellenmiş)
class CNNModel(nn.Module):
    def __init__(self, num_classes):
        super(CNNModel, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(128, 256, kernel_size=3, padding=1), 
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * 4 * 4, 256),  # Görüntü boyutunuza bağlı olarak ayarlayın
            nn.ReLU(),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x

class ImageClassifier:
    def __init__(self, model_path):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Modelinizi 2 sınıflı olacak şekilde ayarlıyoruz
        self.model = CNNModel(num_classes=2)
        self.model.to(self.device)
        
        # Eğittiğiniz yeni model ağırlıklarını yükleyin
        state_dict = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(state_dict)
        self.model.eval()
        
        # Eğitim sırasında kullandığınız görüntü işleme adımları
        self.transform = transforms.Compose([
            transforms.Resize((64, 64)),  # Eğitimde kullandığınız boyut
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])  # Normalize [-1, 1] aralığı
        ])
        
        # Sınıf isimleri
        self.classes = [
            "yangın var",
            "yangın yok"
        ]
    
    def predict(self, image_path):
        image = Image.open(image_path).convert('RGB')
        image = self.transform(image).unsqueeze(0).to(self.device)
        
        # Transformed image shape log
        print(f"Transformed image shape: {image.shape}")
        
        with torch.no_grad():
            outputs = self.model(image)
            # Model çıktısını log
            print(f"Model outputs: {outputs}")
            _, predicted = torch.max(outputs, 1)
            print(f"Predicted index: {predicted.item()}")
            return self.classes[predicted.item()]