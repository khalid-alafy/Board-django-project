from django import forms
from .models import Topic,Post
from froala_editor.widgets import FroalaEditor

class NewTopicForm(forms.ModelForm):
    message=forms.CharField(widget=FroalaEditor(theme='dark'
  ),
        max_length=4000,help_text='The max length of the text is 4000')
    
    class Meta:
        model=Topic
        fields=['subject','message'] 
        
class PostForm(forms.ModelForm):
    message=forms.CharField(widget=FroalaEditor(theme='dark'
  ),
        max_length=4000,help_text='The max length of the text is 4000')
    
    class Meta:
        # widgets = {'message' : FroalaEditor,}
        model=Post
        fields=['message']
