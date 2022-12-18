from django.db import models

# class Marks(models.Model):
#     name = models.CharField(max_length=12, unique=True, primary_key=True)
#     coord_string = models.CharField(max_length=24, null=True)
#     format = models.CharField(max_length=24, null=True)
#     precision_value = models.DecimalField(max_digits=12, decimal_places=4, default=0)
#     precision_units = models.CharField(max_length=12)
#
# class CourseObjects(models.Model):
#     name = models.CharField(max_length=12, unique=True, primary_key=True)
#     description = models.CharField(max_length=255)
#     type = models.CharField(max_length=12)
#     points = models.ForeignKey(Marks, on_delete=models.CASCADE, null=True)
#
# class CourseMetaData(models.Model):
#     course_number = models.IntegerField(primary_key=True)
#     # Calculate this on initialization
#     #distance = models.DecimalField(max_digits=12, decimal_places=4, default=None, null=True)
#
# class CourseMarkOrder(models.Model):
#     course = models.ForeignKey(CourseMetaData, on_delete=models.CASCADE)
#     mark = models.ForeignKey(Marks, on_delete=models.CASCADE)
#     rounding_direction = models.CharField(max_length=1)
#     mark_order = models.IntegerField(primary_key=True)



