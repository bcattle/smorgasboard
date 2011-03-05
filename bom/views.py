from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from bom.models import Supplier, PartType, PartSubType, Part, PartLine, Order, Board
from bom.forms import BoardSelectForm
from django.conf import settings

BOARD_ERROR_URL = '/smorgasboard/'

# TODO: Merge board selection into board() view
# 		Index becomes a general view/redirects to last edited board

def index(request):
	if request.method == 'POST':
		form = BoardSelectForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/smorgasboard/board/' + request.POST['board'])
	else:
		f = BoardSelectForm()
		c = RequestContext(request, {'form': f})
		return render_to_response('pick_board.html', c)

def board(request, board_id=0):
	if board_id:
		board = Board.objects.get(id=board_id)
		if board:
			# Parts on board
			lines = PartLine.objects.filter(board__id=board_id)
			# Filters
			boardTypes = PartType.objects.filter(part__partline__board__id=board_id).distinct()
			boardSubTypes = PartSubType.objects.filter(type__part__partline__board__id=board_id).distinct()
			allPackages = Part.objects.filter(partline__board__id=board_id).order_by('package').values('package') 	# A list of dictionaries
			boardPackages = {p['package'] for p in allPackages}
			# Parts not on board
			otherParts = Part.objects.exclude(partline__board__id=board_id)
			# Filters
			# otherTypes = 
			# otherSubTypes = 
			# otherPackages = 
			
			c = RequestContext(request, {
				'board': board,
				'lines': lines,
				'boardTypes': boardTypes,
				'boardSubTypes': boardSubTypes,
				'boardPackages': boardPackages,
				'otherParts': otherParts,
				# 'otherTypes': otherTypes,
				# 'otherSubTypes': otherSubTypes,
				# 'otherPackages': otherPackages,
			})
			return render_to_response('board.html', c)
	# Else select a board
	return HttpResponseRedirect(BOARD_ERROR_URL)
		
def parts(reqest):
	return HttpResponse('Hello, world.')
	
def order(request, order_id=0):
	if order_id: 
		order = Order.objects.get(id=order_id)
		if order:
			return HttpResponse('Hello, world.')
	#Else select an order
	return HttpResponse('Select an order.')