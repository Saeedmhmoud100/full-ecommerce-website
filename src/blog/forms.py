from django import forms
from .models import PostComment,Post,PostVideoComment,video

class ItemPhotoPostForm(forms.ModelForm):
    Postitle = forms.CharField(label='Title',widget=forms.TextInput(attrs={'class':'form-control','style':'margin-bottom:10px'}))
    Possubject = forms.CharField(label='Subject',widget=forms.Textarea(attrs={'class':'form-control','style':'margin-bottom:15px'}))
    PostImg = forms.ImageField(label='Img',required=False)
    class Meta:
        model = Post
        fields = ('Postitle','Possubject','PostImg')


class ItemPhotoCommentForm(forms.ModelForm):
    PComessage = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':3,'style':'width:70%'}))
    class Meta:
        model=PostComment
        fields= ('PComessage',)


class ItemVideoCommentForm(forms.ModelForm):
    PVComessage = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':3,'style':'width:70%'}))
    class Meta:
        model=PostVideoComment
        fields= ('PVComessage',)

class ItemvideoPostForm(forms.ModelForm):
    Posvtitle = forms.CharField(label='Title',widget=forms.TextInput(attrs={'class':'form-control','style':'margin-bottom:10px'}))
    Posvsubject = forms.CharField(label='Subject',widget=forms.Textarea(attrs={'class':'form-control','style':'margin-bottom:15px'}))
    posvimg = forms.ImageField(label='Img',required=False)
    class Meta:
        model = video
        fields = ('Posvtitle','Posvsubject','posvimg')