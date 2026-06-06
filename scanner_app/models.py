from django.db import models

class Scan(models.Model):
    url = models.URLField()
    risk_level = models.CharField(max_length=20)
    risk_percentage = models.IntegerField()
    scan_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
