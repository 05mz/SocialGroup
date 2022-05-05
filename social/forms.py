from .models import Comment
from django import forms

#
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('name', 'email', 'body')

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
	content = forms.CharField(label ="", widget = forms.Textarea(
	attrs ={
		'class':'form-control',
		'placeholder':'Comment here !',
		'rows':4,
		'cols':50
	}))
	class Meta:
		model = Comment
		fields =['content']
