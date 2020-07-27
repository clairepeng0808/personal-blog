from django import forms
from . import models

class PostForm(forms.ModelForm):

    class Meta():
        model = models.Post
        fields = ('author','title','text')
        widgets = {
            'author':forms.Select(attrs={'class':'edit post-author'}),
            'title':forms.TextInput(attrs={'class':'edit post-title'}),
            'text':forms.Textarea(attrs={'class':'edit editable medium-editor-textarea'}),  
        }

        label = {
            'text': 'Content',
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = models.Comment
        fields = ('author','text')
        widgets = {
                'author':forms.TextInput(attrs={'class':'comment-author'}),
                'text':forms.Textarea(attrs={'label':'comment','class':'editable medium-editor-textarea content'},),
            }

        label = {
            'text': 'Comment',
        }
    