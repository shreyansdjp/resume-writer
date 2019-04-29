from django.db import models

class BasicInfo(models.Model):
    contact_no = models.CharField(max_length=20, blank=True)
    website_link = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=500, blank=True)
    linkedin_link = models.CharField(max_length=100)
    user_id = models.IntegerField()

    def __str__(self):
        return str(self.user_id) + ' - ' + self.email

class Education(models.Model):
    from_where = models.CharField(max_length=200)
    date_started = models.DateField()
    date_ended = models.DateField(blank=True, null=True)
    is_going_on = models.BooleanField(default=False)
    grade = models.CharField(max_length=30)
    what = models.CharField(max_length=30)
    user_id = models.IntegerField()

    def __str__(self):
        return str(self.user_id)  + ' - ' + self.from_where

class Skills(models.Model):
    skill_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    user_id = models.IntegerField()

    def __str__(self):
        return str(self.user_id) + ' - ' + self.skill_name

class Achievements(models.Model):
    achievement = models.CharField(max_length=200)
    user_id = models.IntegerField()

    def __str__(self):
        return str(self.user_id)  + ' - ' + self.what

class WorkExperience(models.Model):
    where = models.CharField(max_length=200)
    date_started = models.DateField()
    date_ended = models.DateField(blank=True, null=True)
    is_going_on = models.BooleanField(default=False)
    time_worked = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    user_id = models.IntegerField()

    def __str__(self):
        return str(self.user_id)  + ' - ' + self.where
