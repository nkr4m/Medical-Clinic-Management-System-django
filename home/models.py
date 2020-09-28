from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Patient(models.Model):   #customer
	user = models.OneToOneField(User, null=True, blank=True,on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField( max_length=200, null=True)
	profile_pic = models.ImageField(default="default_pp.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)


	def __str__(self):
		return self.name


class Tag(models.Model):   #tag
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name


class Treatment(models.Model):   #product
	CATEGORY = (
			('category 1', 'category 1'),
			('category 2', 'category 2'),
            ('category 3', 'category 3'),
			) 

	name = models.CharField(max_length=200, null=True)
	cost = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name



class Appoinment(models.Model):  #order
	STATUS = (
			('Examination', 'Examination'),
			('Undertaking Treatment', 'Undertaking Treatment'),
			('Discharged', 'Discharged'),
			)

	patient = models.ForeignKey(Patient, null=True, on_delete= models.SET_NULL)
	treatment = models.ForeignKey(Treatment, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)

	def __str__(self):
		return self.treatment.name