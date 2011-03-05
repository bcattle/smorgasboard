from django import forms
from bom.models import Board
#from django.forms import ModelForm

class BoardSelectForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(BoardSelectForm, self).__init__(*args, **kwargs)
		# Grab list of boards out of db
		self.fields['board'].choices = [(b.id, str(b)) for b in Board.objects.all()]

	board = forms.ChoiceField(choices=())

class NewPartForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(BoardSelectForm, self).__init__(*args, **kwargs)
		# Grab list of boards out of db
		self.fields['board'].choices = [(b.id, str(b)) for b in Board.objects.all()]

	type = forms.ChoiceField(choices=())
	subtype = forms.ChoiceField(choices=())
	# value
	# desc
	# comment
	# package
	# mfr
	# supplier
	# pn
	# datasheetUrl
	# price
	# minQty
	# inStock
	# qty