from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import profile, projects, skills, staffWithSkills, projectsWithSkills, holidays, alerts, staffAlerts
from adminUser.models import location
from django.http import HttpResponse
from django.db.models import Q
from adminUser.forms import ProjectForm
import datetime
from django.contrib import messages

@login_required
def alerttab_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Employee":  # check if project Manager
        return HttpResponse(status=201)
    title = "Alerts"
    alertList = alerts.objects.filter(Q(staffalerts__staffID=query.staffID) & Q(staffalerts__status='Unseen')).order_by('-alertID')


    return render(request, 'sideBar/alertTab.html', {"title":title, "alertList":alertList})

@login_required
def profile_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Employee":  # check if project Manager
        return HttpResponse(status=201)

    info = profile.objects.get(user=username)

    ongoing = info.projects_set.filter(status="On Going").count()
    upcoming = info.projects_set.filter(status="Approved")
    completed = info.projects_set.filter(status="Completed").count()

    if request.POST:
        if 'project' in request.POST:
            project = request.POST.getlist('project')
            return projectprofile_View(request, project[0])
        elif 'staff' in request.POST:
            staff = request.POST.getlist('staff')
            return staffprofile_View(request, staff[0])
    return render(request, 'eprofile/profile.html',{"title":username,"info":query,"ongoing":ongoing,"upcoming":upcoming,"completed":completed})

@login_required()
def myprojects_View(request):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Employee":  # check if admin
        return HttpResponse(status=201)
    #completed projects of specific user
    info = profile.objects.get(staffID=query.staffID)
    title = "My Projects"
    list = info.projects_set.all()
    if request.POST:
        if 'project' in request.POST:
            project = request.POST.getlist('project')
            return projectprofile_View(request, project[0])
        elif 'staff' in request.POST:
            staff = request.POST.getlist('staff')
            return staffprofile_View(request, staff[0])
    return render(request,'eprojects/myprojects.html',{"list":list,"title":title})

@login_required()
def projectlist_View(request):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Employee":  # check if admin
        return HttpResponse(status=201)

    title = "Projects List"
    list = projects.objects.filter(status="Approved") #get all the objects from profile table

    if request.POST:
        if 'project' in request.POST:
            project = request.POST.getlist('project')
            return projectprofile_View(request,project[0])
        elif 'staff' in request.POST:
            staff = request.POST.getlist('staff')
            return staffprofile_View(request, staff[0])
    return render(request,'eprojects/projectlist.html',{"list":list,"title":title})

@login_required()
def upcomingprojectsget_View(request):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Employee":  # check if admin
        return HttpResponse(status=201)
    #upcoming projects of specific user

    title = "Upcoming Projects of " + query.user.first_name + " " + query.user.last_name
    list = query.projects_set.filter(status="Approved")
    return render(request,'eprojects/projectlist.html',{"list":list,"title":title})


@login_required()
def currentprojectsget_View(request):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Employee":  # check if admin
        return HttpResponse(status=201)
    #get ongoing project of specific user

    title = "On Going Projects of " + query.user.first_name + " " + query.user.last_name
    list =  query.projects_set.filter(status="On Going")
    return render(request,'eprojects/projectlist.html',{"list":list,"title":title})

@login_required()
def completedprojectsget_View(request):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Employee":  # check if admin
        return HttpResponse(status=201)
    #completed projects of specific user

    title = "Completed Projects of " + query.user.first_name + " " + query.user.last_name
    list = query.projects_set.filter(status="Completed")
    return render(request,'eprojects/projectlist.html',{"list":list,"title":title})

@login_required()
def projectprofile_View(request, project_id):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Employee":  # check if admin
        return HttpResponse(status=201)

    info = projects.objects.get(projectID=project_id)
    # this part takes skills and skill hours req. and puts them in a dict
    skillset = []
    skills = info.skills_set.all()
    skillset = list(skills)

    skillhrset = []
    skillhrs = info.projectswithskills_set.all()
    skillhrset = list(skillhrs)

    skillwithhrs = {}

    i = 0
    while i < len(skillset):
        skillwithhrs.update({skillset[i]: skillhrset[i]})
        i = i + 1

    if request.POST and 'staff' in request.POST:
        staff = request.POST.getlist('staff')
        print(staff)
        return staffprofile_View(request, staff[0])

    title = info.projectName
    return render(request, 'eprojects/projectprofile.html', {"info":info, "skillwithhrs":skillwithhrs,'user':query,"title":title})

@login_required()
def staffprofile_View(request, staff_id):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Employee":  # check if admin
        return HttpResponse(status=201)

    title = staff_id
    info = profile.objects.get(staffID = staff_id)



    title = info.user.first_name + " " + info.user.last_name

    # this part takes skills and skill hours available and puts them in a dict
    skillset = []
    skills = info.skills_set.all()
    skillset = list(skills)

    skillhrset = []
    skillhrs = info.staffwithskills_set.all()
    skillhrset = list(skillhrs)

    skillwithhrs = {}

    i = 0
    while i < len(skillset):
        skillwithhrs.update({skillset[i]: skillhrset[i]})
        i = i + 1

    return render(request,'eprofile/staffprofile.html',{"info":info,"title":title, "skillwithhrs":skillwithhrs})

@login_required
def alert_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Employee":  # check if admin
        return HttpResponse(status=201)

    title = "Alerts"


    alertList = alerts.objects.filter(staff=query.staffID).order_by('-alertID')
    staff_id = str(query.staffID)

    if request.POST:
        if 'unseen' in request.POST:
            alertID = request.POST.getlist('unseen')
            alertObj = staffAlerts.objects.filter(Q(alertID=alertID[0])&Q(staffID=query.staffID))
            alertObj.update(status="Seen")
        elif 'project' in request.POST:
            project = request.POST.getlist('project')
            return projectprofile_View(request, project[0])

    return render(request,'sideBar/alerts.html',{"title":title,"alertList":alertList,"staff_id":staff_id})