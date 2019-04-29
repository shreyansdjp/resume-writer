from django.db import models

class UserTemplate(models.Model):
    user_id = models.IntegerField()
    template_name = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return str(self.user_id) + ' - ' + self.template_name
