# classifier/views.py

import os
import random
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import ImageClassifier
from django.conf import settings

# Model dosyasının yolu
MODEL_PATH = os.path.join(settings.BASE_DIR, 'classifier/models/model.pth')
classifier = ImageClassifier(MODEL_PATH)

# Test görüntüleri klasörü
TEST_IMAGES_PATH = os.path.join(settings.BASE_DIR, 'classifier/static/classifier/test_images')

def home(request):
    return render(request, 'classifier/home.html')

def classify_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)
        
        image_path = fs.path(filename)
        prediction = classifier.predict(image_path)
        
        context = {
            'uploaded_file_url': uploaded_file_url,
            'prediction': prediction,
        }
        return render(request, 'classifier/result.html', context)
    return render(request, 'classifier/home.html')

def random_classify_image(request):
    if request.method == 'POST':
        # Test klasörünün doğru yolunu ayarlayın
        test_images_dir = TEST_IMAGES_PATH
        
        # Klasörün var olup olmadığını kontrol edin
        if not os.path.exists(test_images_dir):
            context = {
                'uploaded_file_url': None,
                'prediction': "Test klasörü bulunamadı. Lütfen test görüntüleri ekleyin.",
            }
            return render(request, 'classifier/result.html', context)
        
        try:
            # Geçerli görüntü formatlarını seçin
            valid_extensions = ['.jpg', '.jpeg', '.png']
            images = [f for f in os.listdir(test_images_dir) if os.path.splitext(f)[1].lower() in valid_extensions]
            
            if not images:
                raise FileNotFoundError("Test klasöründe geçerli bir görüntü bulunamadı.")
            
            # Rastgele bir görüntü seçin
            random_image = random.choice(images)
            random_image_path = os.path.join(test_images_dir, random_image)
            
            # Tahmin yapın
            prediction = classifier.predict(random_image_path)
            
            # Görüntünün URL'sini oluşturun
            uploaded_file_url = os.path.join('/static/classifier/test_images/', random_image)
            
            context = {
                'uploaded_file_url': uploaded_file_url,
                'prediction': prediction,
            }
            return render(request, 'classifier/result.html', context)
        
        except FileNotFoundError as e:
            # Test klasörü boşsa veya geçerli dosya yoksa
            context = {
                'uploaded_file_url': None,
                'prediction': str(e),
            }
            return render(request, 'classifier/result.html', context)
        
    return render(request, 'classifier/home.html')