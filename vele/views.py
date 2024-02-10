# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User
import random
import firebase_admin
from firebase_admin import firestore

db = firestore.client()

def home(request):
    return render(request, 'form.html')

def process_form(request):
    if request.method == 'POST':
        name = request.POST['name']
        sex = request.POST['sex']
        branch = request.POST['branch']
        year = request.POST['year']
        instagram_id = request.POST['instagram_id']

        # Check if the Instagram ID already exists
        if User.objects.filter(instagram_id=instagram_id).exists():
            return render(request, 'form.html', {'message': 'Instagram ID already exists. Please use a different one.'})

        user = User.objects.create(name=name, sex=sex, branch=branch, year=year, instagram_id=instagram_id)

        # Check if there are unmatched users of opposite gender
        opposite_gender_users = User.objects.filter(sex=sex=='male' and 'female' or 'male', matched=False).exclude(id=user.id)

        if opposite_gender_users.exists():
            matched_user = random.choice(opposite_gender_users)
            user.matched = True
            user.save()
            matched_user.matched = True
            matched_user.save()
            doc_ref = db.collection('matches').document()
            doc_ref.set({
                'user1_id': str(user.id),
                'user2_id': str(matched_user.id)
            })
            context = {
                'matched_user': matched_user
            }
            return render(request, 'match_result.html', context)
        else:
            return render(request, 'form.html', {'message': 'Patience is key! Your love story might be just a DM away...'})
