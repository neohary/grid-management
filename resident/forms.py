from django import forms

class UploadFileForm(forms.Form):
    mgrid_pk = forms.IntegerField(widget=forms.HiddenInput())
    sheet_name = forms.CharField(
        label="工作表名称",
        widget=forms.TextInput(attrs={'class':'mb-3 form-control'})
    )
    file = forms.FileField(
        label='上传表格文件',
        help_text='',
        widget=forms.FileInput(attrs={'class':'mb-3 form-control','accept':'.xlsx,.xls'})
    )