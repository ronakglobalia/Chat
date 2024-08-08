from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Room, TextMessage
 
 
def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chat/chatPage.html", context)

def create_room(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    
    all_member = User.objects.all()
    if request.method == "POST":
        data = request.POST.copy()
        room = data["room"]
        members = data.getlist("member")
        users = User.objects.filter(pk__in=members)
        
        create_room = Room()
        create_room.name = room
        create_room.save()
        create_room.member.set(users)
        create_room.save()
        context = { 'room':create_room }
        return redirect(reverse("room-list"))
    
    context = { 'members':all_member }
    return render(request, "chat/room.html", context)

def room_list(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    
    all_member = Room.objects.all()
    members = []
    for member in all_member:
        for user in member.member.all():
            if user.id == request.user.id:
                members.append(member)
    context = { 'rooms':members }
    return render(request, "chat/room_list.html", context)

def chat(request, uuid, *args, **kwargs, ):
    if not request.user.is_authenticated:
        return redirect("login-user")
    try:
        request.session['group_name']=uuid
        request.session['username']=request.user.username
        messages = TextMessage.objects.filter(room__room_id=uuid)
    except Exception as e:
        pass
    context = {'messages':messages}
    return render(request, "chat/room_chat.html", context)