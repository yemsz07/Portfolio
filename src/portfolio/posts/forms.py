from django import forms
from .models import Post # Import ang iyong Post model

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        
        # Isasama lang natin ang image at description
        # dahil ang ibang fields ay either automatic o user-related.
        fields = [
            'image', 
            'description'
        ]
        
        # Opsyonal: Widgets para sa mas magandang user interface (UI)
        widgets = {
            # Gawin nating mas malaki ang input area para sa description
            'description': forms.Textarea(attrs={'rows': 4}), 
        }