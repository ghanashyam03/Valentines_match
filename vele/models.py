# models.py
from django.db import models
import firebase_admin
from firebase_admin import firestore

db = firestore.client()

class User(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=GENDER_CHOICES)
    branch = models.CharField(max_length=100)
    year = models.IntegerField()
    instagram_id = models.CharField(max_length=100, unique=True)
    matched = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        doc_ref = db.collection('users').document(str(self.id))
        doc_ref.set({
            'name': self.name,
            'sex': self.sex,
            'branch': self.branch,
            'year': self.year,
            'instagram_id': self.instagram_id,
            'matched': self.matched
        })
