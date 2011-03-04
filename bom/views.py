from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from bom.models import Supplier, PartType, PartSubType, Part, Order, Board
from bom.forms import BoardSelectForm

# Create your views here.
def index(request):
	if request.method == 'POST':
		form = BoardSelectForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/smorgasboard/board/' + request.POST['board'])
	else:
		f = BoardSelectForm()
		return render_to_response('pick_board.html', {'form': f})

	
def board(request, board_id):
	return HttpResponse('Hello, world. You\'re at board ' + str(board_id) + '.')