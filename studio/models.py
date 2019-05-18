from django.db import models

# Create your models here.

class Studio(models.Model):
    # 会自动生成id,自增的
    name=models.CharField(max_length=20,verbose_name="演出厅名")

    seat_rows=models.IntegerField()
    seat_cols=models.IntegerField()

