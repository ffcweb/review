from django import forms
from .models import Review

# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['content', 'star_rating', 'spending', 'image_url', 'link_url']

class UpdateProfileForm(forms.Form):
    new_image_url = forms.URLField()