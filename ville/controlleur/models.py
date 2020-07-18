from django.db import models


# Create your models here.
class Objet(models.Model):
    pin = models.IntegerField()

    # class Meta:
    #     abstract = True

    def __str__(self):
        return str(self.pin)

    def __unicode__(self):
        return str(self.pin)
