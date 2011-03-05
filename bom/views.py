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
		assert False
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
			if request.method == 'POST':
				assert False
				# Can be one of five things:
				if 'partLine' in request.POST:
					pass
				if 'part' in request.POST:
					pass
				if 'addPartLine' in request.POST:
					pass
				if 'subtractPartLine' in request.POST:
					pass
				# TODO add form submitted
		
			# Parts on board
			lines = PartLine.objects.filter(board__id=board_id)
			# Loop through filter commands in query string
			boardFilters = []
			for (field, val) in request.GET.items():
				if field == 'board:type__id__exact':
					lines = lines.filter(part__type__exact=val)
					boardFilters += PartType.objects.filter(id__exact=val)
				if field == 'board:subtype__id__exact':
					lines = lines.filter(part__subtype__exact=val)
					boardFilters += PartSubType.objects.filter(id__exact=val)
				if field == 'board:package':
					lines = lines.filter(part__package=val)
					boardFilters.append(val)
			
			# Filters
			boardTypes = PartType.objects.filter(part__partline__board__id=board_id).distinct()
			boardSubTypes = PartSubType.objects.filter(type__part__partline__board__id=board_id).distinct()
			allPackages = Part.objects.filter(partline__board__id=board_id).order_by('package').values('package') 	# A list of dictionaries
			boardPackages = {p['package'] for p in allPackages}
			# Parts not on board
			otherParts = Part.objects.exclude(partline__board__id=board_id)
			# Loop other filters
			otherFilters = []
			for (field, val) in request.GET.items():
				if field == 'other:type__id__exact':
					lines = lines.filter(part__type__exact=val)
					otherFilters += PartType.objects.filter(id__exact=val)
				if field == 'other:subtype__id__exact':
					lines = lines.filter(part__subtype__exact=val)
					otherFilters += PartSubType.objects.filter(id__exact=val)
				if field == 'other:package':
					lines = lines.filter(part__package=val)
					otherFilters.append(val)
			# Filters
			otherTypes = PartType.objects.filter(part=otherParts).distinct()
			otherSubTypes = PartSubType.objects.filter(type__part=otherParts).distinct()
			otherPackages = {p['package'] for p in otherParts.values('package')}
			
			c = RequestContext(request, {
				'board': board,
				'lines': lines,
				'boardTypes': boardTypes,
				'boardSubTypes': boardSubTypes,
				'boardPackages': boardPackages,
				'boardFilters': boardFilters,
				'otherParts': otherParts,
				'otherTypes': otherTypes,
				'otherSubTypes': otherSubTypes,
				'otherPackages': otherPackages,
				'otherFilters': otherFilters,
			}, [path_processor])
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
	
	
# Called by RequestContext
def path_processor(request):
    return {'path': request.path}