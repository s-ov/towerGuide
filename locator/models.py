from django.db import models
from django.urls import reverse

from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

from locator import utils


class DistributiveSubstation(models.Model):
    title = models.CharField(max_length=25, choices=utils.DS_CHOICES)
    slug = models.SlugField(unique=True, db_index=True)
    level = models.CharField(max_length=25, choices=utils.LEVELS)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('substation', kwargs={'sub_num': self.id})


class MotorControlCenter(models.Model):
    title = models.CharField(max_length=25, choices=utils.MCC_CHOICES)
    slug = models.SlugField(unique=True, db_index=True, blank=True)
    substation = models.ForeignKey('DistributiveSubstation', on_delete=models.PROTECT, related_name='motor_centers')


    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('mcc', kwargs={'mcc_slug': self.slug})
    

class Node(models.Model):
    title = models.CharField(max_length=25)
    slug = models.SlugField(unique=True, db_index=True)
    label = models.ImageField(upload_to="photos/", default=None, blank=True, null=True,)
    level = models.CharField(max_length=25, choices=utils.LEVELS)
    round_per_minute = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3100)])
    power = models.DecimalField(max_digits=4, decimal_places=1,)
    mcc = models.ForeignKey('MotorControlCenter', on_delete=models.PROTECT, related_name='nodes')

    def __str__(self):
        return f'{self.title}_{self.slug}'
    
    def get_absolute_url(self):
        return reverse('node-detail', args=(self.slug,))
