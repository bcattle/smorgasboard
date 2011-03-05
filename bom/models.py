from django.db import models

class Supplier(models.Model):
	name = models.CharField(max_length=50, unique=True)
	abbr = models.CharField(max_length=5, unique=True)
	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ['name']

class PartType(models.Model):
	name = models.CharField(max_length=20, unique=True)
	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ['name']
	
class PartSubType(models.Model):
	type = models.ForeignKey(PartType)
	name = models.CharField(max_length=20)
	def __unicode__(self):
		return self.type.name + ', ' + self.name
	class Meta:
		ordering = ['type','name']
		unique_together = ('type', 'name')
		
# Create your models here.
class Part(models.Model):
	supplier = models.ForeignKey(Supplier)
	pn = models.CharField(max_length=50)		# Supplier part number
	supplierUrl = models.URLField(blank=True)
	
	type = models.ForeignKey(PartType)
	subtype = models.ForeignKey(PartSubType, blank=True, null=True)
	value = models.CharField(max_length=20, blank=True)
	desc = models.CharField(max_length=100, blank=True)
	package = models.CharField(max_length=20, blank=True)
	mfr = models.CharField(max_length=20)
	datasheet = models.URLField(blank=True)
	comment = models.CharField(max_length=200, blank=True)
	
	price = models.DecimalField(max_digits=6, decimal_places=3)
	minQty = models.PositiveSmallIntegerField()
	inStock = models.BooleanField()
	lastUpdated = models.DateTimeField(blank=True, null=True)
	
	substitutes = models.ManyToManyField('self', blank=True)
	
	created = models.DateTimeField(auto_now_add=True)		# Automatically set when record is created
	def __unicode__(self):
		if self.subtype:
			return self.pn + ': ' + self.type.name + ', ' + self.subtype.name + ', ' + self.value + ', ' + self.desc
		else:
			return self.pn + ': ' + self.type.name + ', ' + self.value + ', ' + self.desc
	class Meta:
		ordering = ['type','subtype','value','created']
		unique_together = ('supplier', 'pn')

# class BoardSubsection(models.Model):
	# name = models.CharField(max_length=100, unique=True)
	# comment = models.CharField(max_length=200, blank=True)

	
class Board(models.Model):
	pn = models.CharField(max_length=50)		# Karem part number
	rev = models.CharField(max_length=10)
	desc = models.CharField(max_length=200)
	#subsections = models.ManyToManyField(BoardSubsection, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	last_edited = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.pn + '.' + self.rev + ': ' + self.desc
	class Meta:
		unique_together = ('pn', 'rev')
	
class PartLine(models.Model):
	#subsection = models.ForeignKey(BoardSubsection)
	board = models.ForeignKey(Board)
	part = models.ForeignKey(Part)
	qty = models.PositiveSmallIntegerField(default = 0)
	def __unicode__(self):
		return self.board.pn + ' - p/n ' + self.part.pn + ': ' + str(self.qty)
	class Meta:
		unique_together = ('board', 'part')
		#unique_together = ('subsection', 'part')

class Order(models.Model):
	supplier = models.ForeignKey(Supplier)
	boards = models.ManyToManyField(Board)
	comment = models.CharField(max_length=200, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return 'Order ' + str(self.created)
	class Meta:
		get_latest_by = '-created'
		
class OrderLine(models.Model):
	order = models.ForeignKey(Order)
	part = models.ForeignKey(Part)
	qty = models.PositiveSmallIntegerField(default = 0)
	def __unicode__(self):
		return 'p/n ' + self.part.pn + ': ' + str(self.qty)
	class Meta:
		unique_together = ('order', 'part')
		
	
