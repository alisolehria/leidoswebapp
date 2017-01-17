from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import profile, projects, skills, staffWithSkills, projectsWithSkills, holidays, alerts, staffAlerts
from .models import location
from django.http import HttpResponse
import datetime
from django.contrib.auth.models import User
from .forms import UserForm,UserProfileForm,ProjectForm, SkillForm, LocationForm, UserUpdateForm
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q


@login_required
def dashboard_View(request):
    username = request.user
    query = profile.objects.get(user=username)
    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)
    num = profile.objects.exclude(workStatus="Not Employeed").count() #get number of staff
    projectNum = projects.objects.filter(status='On Going').count()#number of active projects


    today = datetime.date.today() #get todays date
    upcoming = projects.objects.filter(status="Approved") #check if greater than todays date

    return render(request, 'profile/dashboard.html',{"title":username,"info":query,'num':num,'projectNum':projectNum,'upcoming':upcoming})

@login_required()
def stafflist_View(request):
    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    list = profile.objects.all() #get all the objects from profile table
    title = "Staff List"
    if request.POST:
        staffList = request.POST.getlist('selectStaff')
        for staff in staffList:
             return staffprofile_View(request,staff)

    return render(request,'staff/stafflist.html',{"list":list,"title":title})

@login_required()
def projectlist_View(request):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    title = "Projects List"
    list = projects.objects.all() #get all the objects from profile table

    return render(request,'project/projectlist.html',{"list":list,"title":title})

@login_required()
def currentstaff_View(request):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)


    list = profile.objects.exclude(workStatus="Not Employeed") ##get all the objects from profile table exclueding not employeed
    title = "Currently Employeed"
    return render(request,'staff/stafflist.html',{"list":list,"title":title})

@login_required()
def currentprojects_View(request):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    title = "On Going Projects"
    list = projects.objects.filter(status="On Going") #get only projects which are ongoing
    return render(request,'project/projectlist.html',{"list":list,"title":title})

@login_required()
def upcomingprojects_View(request):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    title = "Upcoming Projects"
    list = projects.objects.filter(status="Approved")  #get only projects which are approved
    return render(request,'project/projectlist.html',{"list":list,"title":title})


@login_required()
def staffprofile_View(request, staff_id):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Admin":  # check if admin
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

    return render(request,'staff/staffprofile.html',{"info":info,"title":title,"ongoing":ongoing,"upcoming":upcoming,"completed":completed,"skillwithhrs":skillwithhrs})

@login_required()
def currentprojectsget_View(request, staff_id):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)
    #get ongoing project of specific user
    info = profile.objects.get(staffID=staff_id)
    title = "On Going Projects of " + info.user.first_name + " " + info.user.last_name
    list =  info.projects_set.filter(status="On Going")
    return render(request,'project/projectlist.html',{"list":list,"title":title})

@login_required()
def upcomingprojectsget_View(request, staff_id):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)
    #upcoming projects of specific user
    info = profile.objects.get(staffID=staff_id)
    title = "Upcoming Projects of " + info.user.first_name + " " + info.user.last_name
    list = info.projects_set.filter(status="Approved")
    return render(request,'project/projectlist.html',{"list":list,"title":title})

@login_required()
def completedprojectsget_View(request, staff_id):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)
    #completed projects of specific user
    info = profile.objects.get(staffID=staff_id)
    title = "Completed Projects of " + info.user.first_name + " " + info.user.last_name
    list = info.projects_set.filter(status="Completed")
    return render(request,'project/projectlist.html',{"list":list,"title":title})

@login_required()
def projectprofile_View(request, project_id):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Admin":  # check if admin
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

    if request.POST:
        if "decline" in request.POST:
            id = request.POST.getlist("decline")
            project = projects.objects.filter(projectID=id[0])
            project.update(status="Declined")
            alert = alerts.objects.create(fromStaff=query, alertType='Project', alertDate=datetime.date.today(),
                                          project=info)
            staffAlerts.objects.create(alertID=alert, staffID=info.projectManager, status="Unseen")
            alertobj = alerts.objects.get(Q(project=info) & Q(fromStaff=info.projectManager.staffID))
            staffalert = staffAlerts.objects.filter(alertID=alertobj.alertID)
            staffalert.update(status="Seen")
            messages.success(request, "Project Status Changed")
            return projectlist_View(request)
        elif "accept" in request.POST:
            id = request.POST.getlist("accept")
            project = projects.objects.filter(projectID=id[0])
            project.update(status="Approved")
            alert = alerts.objects.create(fromStaff=query, alertType='Project', alertDate=datetime.date.today(),
                                          project=info)
            staffAlerts.objects.create(alertID=alert, staffID=info.projectManager, status="Unseen")
            alertobj = alerts.objects.get(Q(project=info)&Q(fromStaff=info.projectManager.staffID))
            staffalert = staffAlerts.objects.filter(alertID=alertobj.alertID)
            staffalert.update(status="Seen")
            messages.success(request, "Project Status Changed")
            return projectlist_View(request)
        elif "discontinue" in request.POST:
            id = request.POST.getlist("discontinue")
            project = projects.objects.filter(projectID=id[0])
            info = projects.objects.get(projectID=id[0])
            project.update(status="Discontinued")
            alert = alerts.objects.create(fromStaff=query, alertType='Project', alertDate=datetime.date.today(),
                                          project=info)
            working = info.staffID.all()
            for staff in working:
                employee = profile.objects.get(staffID=staff.staffID)
                staffAlerts.objects.create(alertID=alert, staffID=employee, status="Unseen")
            messages.success(request, "Project Status Changed")
            return projectlist_View(request)

    return render(request,'project/projectprofile.html',{"info":info,"skillwithhrs":skillwithhrs})

@login_required
def table_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)
    # auto refresh view
    num = profile.objects.exclude(workStatus="Not Employeed").count() #get number of staff
    projectNum = projects.objects.filter(status='On Going').count()#number of active projects


    today = datetime.date.today() #get todays date
    upcoming = projects.objects.filter(status="Approved") #check if greater than todays date

    return render(request, 'profile/table.html',{"info":query,'num':num,'projectNum':projectNum,'upcoming':upcoming})

@login_required()
def addstaff_View(request):

    username = request.user
    query = profile.objects.get(user=username)  # get username
    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    title = "Add Staff"
    form = UserForm(request.POST or None)
    form2 = UserProfileForm(request.POST or None)

    #this is adding to tables
    if form.is_valid() and form2.is_valid():
        firstname = form.cleaned_data.get('first_name')
        lastname = form.cleaned_data.get('last_name')
        user_query = profile.objects.values_list('staffID',flat=True)
        firstletter = str(firstname[0])
        secondletter = str(lastname[0])
        new_password = "leidos123"
        new_username = str.lower(firstletter) + str.lower(secondletter) + (str(max(user_query)+1)) #take first letters of fname and lname along with staff id to generate username
        emailToSend = [form.cleaned_data.get('email')]
        #send_mail('Welcome To Leidos','Your account has been created. Following are your account credentials.\n\n Username= '+new_username+'\n Password: leidos123\n\n\nThank You.','leidos.syntax@gmail.com',emailToSend,fail_silently=False,)
        user= form.save(commit=False)
        user.username = new_username
        user.set_password(new_password)
        user.save()

        userprofile = form2.save(commit=False)
        userprofile.user= user;
        userprofile.workStatus="Working"
        userprofile.skillLevel="0"
        if userprofile.designation == "Admin":
            userprofile.salary=15000
        elif userprofile.designation == "Project Manager":
            userprofile.salary = 10000
        elif userprofile.designation == "Contractor":
            userprofile.salary = 5000
        else:
            userprofile.salary = 8000

        userprofile.save()
        messages.success(request, firstname+" "+lastname+"'s account created successfully!")
        return addskill_View(request,max(user_query)+1)

    return render(request,'staff/addstaff.html',{"title":title,"form":form,"form2":form2})


@login_required
def addskill_View(request, staff_id):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    user = profile.objects.get(staffID=staff_id)
    title = user.user.first_name + " " + user.user.last_name

    skillset = skills.objects.exclude(staffID=staff_id)

    if(request.POST and "submitskill" in request.POST):
        skill = request.POST.getlist('skillselec')
        hrs = request.POST.getlist('hours')
        hrs= filter(lambda x: x != "", hrs)
        count = len(skill)
        x = 0
        while x < count:
            staffWithSkills.objects.create(staffID_id=staff_id,skillID_id=skill[x],hoursAvailable=hrs[x])
            x = x + 1
        messages.success(request, "Skill added succesfully!")
        return staffprofile_View(request, staff_id)

    return render(request, 'staff/addskill.html', {"title":title, "skillset":skillset, "user":user})

@login_required
def addproject_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    title = "Add Project"
    pms = profile.objects.filter(designation="Project Manager")
    form = ProjectForm(request.POST or None)

    newID = projects.objects.values_list('projectID',flat=True)
    #testing
    if form.is_valid() and request.POST:
        project = form.save(commit=False)
        pm = request.POST.getlist('selectPM')
        pmquery = profile.objects.get(staffID=pm[0])
        project.projectManager= pmquery
        project.status = "Approved"
        project.save()
        project.staffID.add(pm[0])
        pm = profile.objects.get(staffID = pm[0])
        alert = alerts.objects.create(fromStaff=query, alertType='Staff', alertDate=datetime.date.today(),
                                      project=project)
        staffAlerts.objects.create(alertID=alert, staffID=pm, status="Unseen")
        messages.success(request, "Project added succesfully!")
        return addpskill_View(request,max(newID))


    return render(request,'project/addproject.html',{"title":title,"form":form,"pms":pms})




@login_required
def addpskill_View(request, project_id):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    title = projects.objects.get(projectID=project_id)
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
                                      project=title,info="Added Skills to Project" )
        staffAlerts.objects.create(alertID=alert, staffID=title.projectManager, status="Unseen")
        if 'continue' in request.POST:
            return addpstaff_View(request, project_id)
        elif 'save' in request.POST:
            return projectprofile_View(request, project_id)

    return render(request, 'project/addskill.html',{"title":title,"skillset":skillset})


@login_required
def addpstaff_View(request, project_id):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    title = projects.objects.get(projectID=project_id)
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
        staffAlerts.objects.create(alertID=alert, staffID=title.projectManager, status="Unseen")
        return projectprofile_View(request,project_id)


    return render(request, 'project/addstaff.html',{"title":title,"list":list,"number":number})

@login_required
def skill_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    title = "Add Skill"
    list = skills.objects.all()
    form = SkillForm(request.POST or None)

    if form.is_valid() and request.POST:
        skill = form.save(commit=False)
        skill.save()
        messages.success(request, "Skill added succesfully to the system!")

    return render(request, 'common/skill.html',{"title":title,"list":list,"form":form})

@login_required
def location_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    title = "Add Location"
    list = location.objects.all()
    form = LocationForm(request.POST or None)

    if form.is_valid() and request.POST:
        loc = form.save(commit=False)
        loc.save()
        messages.success(request, "Location added succesfully to the system!")

    return render(request, 'common/location.html',{"title":title,"list":list,"form":form})


@login_required
def editprofile_View(request,staff_id):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    info = profile.objects.get(staffID=staff_id)
    user = User.objects.get(username=info.user.username)
    title = "Edit Profile of User: " + info.user.first_name + " " + info.user.last_name
    form = UserUpdateForm(request.POST or None,instance=user)
    form2 = UserProfileForm(request.POST or None, instance=info)

    if form.is_valid() and form2.is_valid():
        form.save()
        form2.save()
        messages.success(request, info.user.first_name + " " + info.user.last_name + "'s account edited successfully!")
        return staffprofile_View(request,staff_id)

    return render(request, 'staff/editprofile.html',{"title":title,"form":form,"form2":form2})

@login_required
def editproject_View(request,project_id):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    project = projects.objects.get(projectID=project_id)
    title = "Edit Project: " + project.projectName
    pms = profile.objects.filter(designation="Project Manager")
    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid() and request.POST:
        pm = request.POST.getlist("selectPM")
        update = form.save(commit=False)
        pmquery = profile.objects.get(staffID=pm[0])
        update.projectManager = pmquery
        update.save()
        messages.success(request, project.projectName + " edited successfully!")
        return projectprofile_View(request, project_id)

    return render(request,'project/editproject.html',{"title":title,"pms":pms,"project":project,"form":form})

@login_required
def alert_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    title = "Alerts"


    alertList = alerts.objects.filter(staff=query.staffID).order_by('-alertID')
    staff_id = str(query.staffID)

    if request.POST:
        if "rejectProj" in request.POST:
            id = request.POST.getlist("rejectProj")
            project = projects.objects.filter(projectID=id[0])
            info = projects.objects.get(projectID=id[0])
            project.update(status="Declined")
            alert = alerts.objects.create(fromStaff=query, alertType='Project', alertDate=datetime.date.today(),
                                          project=info)
            staffAlerts.objects.create(alertID=alert, staffID=info.projectManager, status="Unseen")
            alertobj = alerts.objects.get(Q(project=info) & Q(fromStaff=info.projectManager.staffID))
            staffalert = staffAlerts.objects.filter(alertID=alertobj.alertID)
            staffalert.update(status="Seen")
            messages.success(request, "Project Status Changed")
            return projectlist_View(request)
        elif "acceptProj" in request.POST:
            id = request.POST.getlist("acceptProj")
            project = projects.objects.filter(projectID=id[0])
            info = projects.objects.get(projectID=id[0])
            project.update(status="Approved")
            alert = alerts.objects.create(fromStaff=query, alertType='Project', alertDate=datetime.date.today(),
                                          project=info)
            staffAlerts.objects.create(alertID=alert, staffID=info.projectManager, status="Unseen")
            alertobj = alerts.objects.get(Q(project=info) & Q(fromStaff=info.projectManager.staffID))
            staffalert = staffAlerts.objects.filter(alertID=alertobj.alertID)
            staffalert.update(status="Seen")
            messages.success(request, "Project Status Changed")
            return projectlist_View(request)

    return render(request,'common/alerts.html',{"title":title,"alertList":alertList,"staff_id":staff_id})

@login_required
def alerttab_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    title = "Alerts"

    alertList = alerts.objects.filter(Q(staffalerts__staffID=query.staffID) & Q(staffalerts__status='Unseen')).order_by(
        '-alertID')
    return render(request,'common/alertTab.html',{"title":title,"alertList":alertList})

@login_required
def alert_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    title = "Alerts"


    alertList = alerts.objects.filter(staff=query.staffID).order_by('-alertID')
    staff_id = str(query.staffID)

    if request.POST:
        if "rejectProj" in request.POST:
            id = request.POST.getlist("rejectProj")
            project = projects.objects.filter(projectID=id[0])
            info = projects.objects.get(projectID=id[0])
            project.update(status="Declined")
            alert = alerts.objects.create(fromStaff=query, alertType='Project', alertDate=datetime.date.today(),
                                          project=info)
            staffAlerts.objects.create(alertID=alert, staffID=info.projectManager, status="Unseen")
            alertobj = alerts.objects.get(Q(project=info) & Q(fromStaff=info.projectManager.staffID))
            staffalert = staffAlerts.objects.filter(alertID=alertobj.alertID)
            staffalert.update(status="Seen")
            messages.success(request, "Project Status Changed")
            return projectlist_View(request)
        elif "acceptProj" in request.POST:
            id = request.POST.getlist("acceptProj")
            project = projects.objects.filter(projectID=id[0])
            info = projects.objects.get(projectID=id[0])
            project.update(status="Approved")
            alert = alerts.objects.create(fromStaff=query, alertType='Project', alertDate=datetime.date.today(),
                                          project=info)
            staffAlerts.objects.create(alertID=alert, staffID=info.projectManager, status="Unseen")
            alertobj = alerts.objects.get(Q(project=info) & Q(fromStaff=info.projectManager.staffID))
            staffalert = staffAlerts.objects.filter(alertID=alertobj.alertID)
            staffalert.update(status="Seen")
            messages.success(request, "Project Status Changed")
            return projectlist_View(request)
        elif "seen" in request.POST:
            alertID = request.POST.getlist('seen')
            alertObj = staffAlerts.objects.filter(Q(alertID=alertID[0]) & Q(staffID=query.staffID))
            alertObj.update(status="Seen")

    return render(request,'common/alerts.html',{"title":title,"alertList":alertList,"staff_id":staff_id})

@login_required
def projectrequests_View(request):

    username = request.user
    query = profile.objects.get(user = username) #get username

    if query.designation != "Admin":  # check if admin
        return HttpResponse(status=201)

    title = "Project Requests"


    alertList = alerts.objects.filter(Q(staff=query.staffID)&Q(alertType="Project")&Q(project__status="Pending Approval")).order_by('-alertID')
    staff_id = str(query.staffID)

    if request.POST:
        if "rejectProj" in request.POST:
            id = request.POST.getlist("rejectProj")
            project = projects.objects.filter(projectID=id[0])
            info = projects.objects.get(projectID=id[0])
            project.update(status="Declined")
            alert = alerts.objects.create(fromStaff=query, alertType='Project', alertDate=datetime.date.today(),
                                          project=info)
            staffAlerts.objects.create(alertID=alert, staffID=info.projectManager, status="Unseen")
            alertobj = alerts.objects.get(Q(project=info) & Q(fromStaff=info.projectManager.staffID))
            staffalert = staffAlerts.objects.filter(alertID=alertobj.alertID)
            staffalert.update(status="Seen")
            messages.success(request, "Project Status Changed")
            return projectlist_View(request)
        elif "acceptProj" in request.POST:
            id = request.POST.getlist("acceptProj")
            project = projects.objects.filter(projectID=id[0])
            info = projects.objects.get(projectID=id[0])
            project.update(status="Approved")
            alert = alerts.objects.create(fromStaff=query, alertType='Project', alertDate=datetime.date.today(),
                                          project=info)
            staffAlerts.objects.create(alertID=alert, staffID=info.projectManager, status="Unseen")
            alertobj = alerts.objects.get(Q(project=info) & Q(fromStaff=info.projectManager.staffID))
            staffalert = staffAlerts.objects.filter(alertID=alertobj.alertID)
            staffalert.update(status="Seen")
            messages.success(request, "Project Status Changed")
            return projectlist_View(request)

    return render(request,'project/projectrequests.html',{"title":title,"alertList":alertList,"staff_id":staff_id})