from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import profile, projects, skills, staffWithSkills, projectsWithSkills, holidays, alerts, staffAlerts
from adminUser.models import location
from django.http import HttpResponse
from django.db.models import Q
from adminUser.forms import ProjectForm, HolidaysForm
import datetime
from django.contrib import messages

@login_required
def alerttab_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Project Manager":  # check if project Manager
        return HttpResponse(status=201)
    title = "Alerts"
    alertList = alerts.objects.filter(Q(staffalerts__staffID=query.staffID) & Q(staffalerts__status='Unseen')).order_by('-alertID')


    return render(request, 'alerts/alertTab.html', {"title":title, "alertList":alertList})

@login_required
def profile_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Project Manager":  # check if project Manager
        return HttpResponse(status=201)

    info = profile.objects.get(user=username)

    ongoing = info.projects_set.filter(status="On Going").count()
    upcoming = info.projects_set.filter(status="Approved")
    completed = info.projects_set.filter(status="Completed").count()

    # this part takes skills and skill hours available and puts them in a dict
    skillset = []
    skills = info.skills_set.all()
    skillset = list(skills)

    skillhrset = []
    skillhrs = info.staffwithskills_set.all()
    skillhrset = list(skillhrs)

    skillwithhrs = {}
    time = datetime.date.today()

    i = 0
    while i < len(skillset):
        skillwithhrs.update({skillset[i]: skillhrset[i]})
        i = i + 1

    return render(request, 'profile/profile.html',{"title":username,"info":query,"ongoing":ongoing,"upcoming":upcoming,"completed":completed,"skillwithhrs":skillwithhrs,"time":time})

@login_required()
def upcomingprojectsget_View(request, staff_id):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Project Manager":  # check if admin
        return HttpResponse(status=201)
    #upcoming projects of specific user
    info = profile.objects.get(staffID=staff_id)
    title = "Upcoming Projects of " + info.user.first_name + " " + info.user.last_name
    list = info.projects_set.filter(status="Approved")
    return render(request,'projects/projectlist.html',{"list":list,"title":title})


@login_required()
def currentprojectsget_View(request, staff_id):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Project Manager":  # check if admin
        return HttpResponse(status=201)
    #get ongoing project of specific user
    info = profile.objects.get(staffID=staff_id)
    title = "On Going Projects of " + info.user.first_name + " " + info.user.last_name
    list =  info.projects_set.filter(status="On Going")
    return render(request,'projects/projectlist.html',{"list":list,"title":title})

@login_required()
def completedprojectsget_View(request, staff_id):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Project Manager":  # check if admin
        return HttpResponse(status=201)
    #completed projects of specific user
    info = profile.objects.get(staffID=staff_id)
    title = "Completed Projects of " + info.user.first_name + " " + info.user.last_name
    list = info.projects_set.filter(status="Completed")
    return render(request,'projects/projectlist.html',{"list":list,"title":title})

@login_required()
def projectlist_View(request):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Project Manager":  # check if admin
        return HttpResponse(status=201)

    title = "Projects List"
    list = projects.objects.all() #get all the objects from profile table
    return render(request,'projects/projectlist.html',{"list":list,"title":title})

@login_required()
def projectprofile_View(request, project_id):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Project Manager":  # check if admin
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

    if request.POST and 'complete' in request.POST:
        id = request.POST.getlist("complete")
        project = projects.objects.filter(projectID=id[0])
        info = projects.objects.get(projectID=id[0])
        project.update(status="Completed")
        alert = alerts.objects.create(fromStaff=query, alertType='Project', alertDate=datetime.date.today(),
                                      project=info, info="Project")
        working = info.staffID.all()
        for staff in working:
            employee = profile.objects.get(staffID=staff.staffID)
            staffAlerts.objects.create(alertID=alert, staffID=employee, status="Unseen")

        alertAdmin = alerts.objects.create(fromStaff=query, alertType='Staff', alertDate=datetime.date.today(),project=info)
        staffAlerts.objects.create(alertID=alertAdmin, staffID=profile.objects.get(staffID = 1), status="Unseen")
        messages.success(request, "Project Status Changed")
        return projectlist_View(request)

    return render(request, 'projects/projectprofile.html', {"info":info, "skillwithhrs":skillwithhrs,'user':query})

@login_required()
def myprojects_View(request):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Project Manager":  # check if admin
        return HttpResponse(status=201)
    #completed projects of specific user
    info = profile.objects.get(staffID=query.staffID)
    title = "My Projects"
    list = info.projects_set.all()
    return render(request,'projects/myprojects.html',{"list":list,"title":title})

@login_required()
def staffprofile_View(request, staff_id):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Project Manager":  # check if admin
        return HttpResponse(status=201)

    title = staff_id
    info = profile.objects.get(staffID = staff_id)


    ongoing = info.projects_set.filter(status="On Going").count()
    upcoming = info.projects_set.filter(status="Approved").count()
    completed = info.projects_set.filter(status="Completed").count()


    #this part takes skills and skill hours available and puts them in a dict
    skillset = []
    skills = info.skills_set.all()
    skillset = list(skills)

    skillhrset = []
    skillhrs = info.staffwithskills_set.all()
    skillhrset = list(skillhrs)

    skillwithhrs = {}

    i = 0
    while i < len(skillset):
        skillwithhrs.update({skillset[i]:skillhrset[i]})
        i=i+1

    return render(request,'employee/staffprofile.html',{"info":info,"title":title,"ongoing":ongoing,"upcoming":upcoming,"completed":completed,"skillwithhrs":skillwithhrs})

@login_required
def alert_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Project Manager":  # check if admin
        return HttpResponse(status=201)

    title = "Alerts"


    alertList = alerts.objects.filter(staff=query.staffID).order_by('-alertID')
    staff_id = str(query.staffID)

    if request.POST:
        if "unseen" in request.POST:
            alertID = request.POST.getlist('unseen')
            alertObj = staffAlerts.objects.filter(Q(alertID=alertID[0])&Q(staffID=query.staffID))
            alertObj.update(status="Seen")
        elif "accept" in request.POST:
            staffID = request.POST.getlist("accept")
            alertID = request.POST.getlist('seen')
            alertObj = staffAlerts.objects.filter(Q(alertID=alertID[0]) & Q(staffID=query.staffID))
            alertObj.update(status="Seen")
            project = request.POST.getlist("projectNum")
            proj = projects.objects.get(projectID=project[0])
            alert = alerts.objects.create(fromStaff=query, alertType='Staff', alertDate=datetime.date.today(),
                                          project=proj)
            proj.staffID.add(staffID[0])
            staff = profile.objects.get(staffID=staffID[0])
            staffAlerts.objects.create(alertID=alert, staffID=staff, status="Unseen")
            messages.success(request,staff.user.first_name+" "+staff.user.last_name+" Added Succesfully to "+alert.project.projectName )
            return projectprofile_View(request,project[0])
        elif "reject" in request.POST:
            staffID = request.POST.getlist("reject")
            alertID = request.POST.getlist('seen')
            alertObj = staffAlerts.objects.filter(Q(alertID=alertID[0]) & Q(staffID=query.staffID))
            alertObj.update(status="Seen")
            project = request.POST.getlist("projectNum")
            proj = projects.objects.get(projectID=project[0])
            alert = alerts.objects.create(fromStaff=query, alertType='Project Request', alertDate=datetime.date.today(),
                                         project=proj )
            staff = profile.objects.get(staffID=staffID[0])
            staffAlerts.objects.create(alertID=alert, staffID=staff, status="Unseen")
            messages.success(request,
                             staff.user.first_name + " " + staff.user.last_name + "'s Request to join " +alert.project.projectName+" Declined")
            return projectprofile_View(request,project[0])
    return render(request,'alerts/alerts.html',{"title":title,"alertList":alertList,"staff_id":staff_id})

@login_required
def requestproject_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Project Manager":  # check if admin
        return HttpResponse(status=201)

    title = "Request Project"

    form = ProjectForm(request.POST or None)

    newID = projects.objects.values_list('projectID',flat=True)
    admin = profile.objects.get(staffID=1)
    if form.is_valid():
        project = form.save(commit=False)
        pm = request.POST.getlist('selectPM')
        project.projectManager= query
        project.status = "Pending Approval"
        project.save()
        project.staffID.add(query)
        alert = alerts.objects.create(fromStaff=query,alertType='Project',alertDate=datetime.date.today(),project=project)
        staffAlerts.objects.create(alertID=alert,staffID=admin,status="Unseen")
        messages.success(request, "Project requested succesfully!")
        return addpskill_View(request, max(newID))


    return render(request,'projects/requestproject.html',{"title":title,"form":form,"query":query})


@login_required
def addpskill_View(request, project_id):

    username = request.user
    query = profile.objects.get(user = username) #get username
    admin = profile.objects.get(staffID = 1)
    if query.designation != "Project Manager":  # check if admin
        return HttpResponse(status=201)

    title = projects.objects.get(projectID=project_id)

    if title.projectManager != query:
        return HttpResponse(status=201)  # check if user is pm of that project


    skillset = skills.objects.exclude(projectID=project_id)

    if request.POST and ('continue' in request.POST or 'save' in request.POST):
        skill = request.POST.getlist('skillselec')
        hrs = request.POST.getlist('hours')
        hrs = filter(lambda x: x != "", hrs)
        count = len(skill)
        x = 0
        while x < count:
            projectsWithSkills.objects.create(projectID_id=project_id, skillID_id=skill[x], hoursRequired=hrs[x])
            x = x + 1
        messages.success(request, "Skill added succesfully!")
        alert = alerts.objects.create(fromStaff=query, alertType='Edit Project', alertDate=datetime.date.today(),
                                      project=title, info="Added Skills to Project")
        staffAlerts.objects.create(alertID=alert, staffID=admin, status="Unseen")
        if 'continue' in request.POST:
            return addpstaff_View(request, project_id)
        elif 'save' in request.POST:
            return projectprofile_View(request, project_id)

    return render(request, 'projects/addskill.html', {"title":title, "skillset":skillset})

@login_required
def addpstaff_View(request, project_id):

    username = request.user
    query = profile.objects.get(user = username) #get username
    admin = profile.objects.get(staffID = 1)
    if query.designation != "Project Manager":  # check if admin
        return HttpResponse(status=201)


    title = projects.objects.get(projectID=project_id)
    if title.projectManager != query:
        return HttpResponse(status=201) #check if user is pm of that project

    # exclude project managers and admins also staff which have holidays during the project
    list = profile.objects.exclude(projects=project_id).exclude(designation="Project Manager").exclude(designation="Admin").exclude(holidays__endDate__gt=title.startDate)

    number = title.numberOfStaff - profile.objects.filter(projects=project_id).count()

    if request.POST and 'add' in request.POST:
        staff = request.POST.getlist('selectStaff')
        alert = alerts.objects.create(fromStaff=query, alertType='Staff', alertDate=datetime.date.today(),
                                      project=title)
        for id in staff:
            title.staffID.add(id)
            staffAlerts.objects.create(alertID=alert, staffID=profile.objects.get(staffID=id), status="Unseen")

        messages.success(request, "Staff added succesfully!")
        alert = alerts.objects.create(fromStaff=query, alertType='Edit Project', alertDate=datetime.date.today(),
                                      project=title, info="Added Staff to Project")
        staffAlerts.objects.create(alertID=alert, staffID=admin, status="Unseen")
        return projectprofile_View(request,project_id)


    return render(request, 'projects/addstaff.html',{"title":title,"list":list,"number":number})

@login_required
def holiday_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Project Manager":  # check if admin
        return HttpResponse(status=201)

    title = "Request Leave"

    form = HolidaysForm(request.POST or None)
    admin = profile.objects.get(staffID=1)
    if form.is_valid() and request.POST:
        hol = form.save(commit=False)
        hol.status="Pending Approval"
        hol.staffID_id = query.staffID
        hol.save()
        alert = alerts.objects.create(fromStaff=query, alertType='Leave', alertDate=datetime.date.today(),
                                      holiday=hol, info="Your Project Request")
        staffAlerts.objects.create(alertID=alert, staffID=admin, status="Unseen")
        messages.success(request, "Leave Requested!")

    return render(request, 'profile/requestholiday.html', {"title":title, "form":form})
