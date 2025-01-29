# classifier/forms.py

from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.content_type not in ['image/jpeg', 'image/png']:
                raise forms.ValidationError('Sadece JPEG ve PNG formatında görüntüler yükleyebilirsiniz.')
            if image.size > 5*1024*1024:
                raise forms.ValidationError('Görüntü boyutu 5MB\'ı geçemez.')
        return image