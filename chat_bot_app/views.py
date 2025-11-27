from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from chat_bot_app.models import *
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404




# Create your views here.
def home(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def admin_home(request):
    return render(request,'admin_home.html')

def therapist_home(request):
    return render(request,'therapist_home.html')


def user_home(request):
    return render(request,'user_home.html')

def login(request):
    if 'submit' in request.POST:
        uname = request.POST['username']
        pwd = request.POST['password']
        
        res = Login.objects.filter(username=uname, password=pwd).first()
        
        if res: 
            request.session['lid'] = res.pk  

            if res.usertype == 'admin':
                return HttpResponse("<script>alert('Login Success');window.location='admin_home'</script>")
            
            elif res.usertype == 'pending':
                return HttpResponse("<script>alert('Admin needs to approve');window.location='login'</script>")
            elif res.usertype == 'therapist':
                ress = Therapist.objects.filter(login_id=request.session['lid']).first()
                if ress:
                    request.session['tid'] = ress.pk  
                    print("Therapist id TID:", request.session['tid'])
                    return HttpResponse("<script>alert('Login to Therapist');window.location='therapist_home'</script>")
                else:
                    return HttpResponse("<script>alert('Invalid User Type');window.location='login'</script>")
            elif res.usertype == 'user':
                ress = User.objects.filter(login_id=request.session['lid']).first()
                if ress:
                    request.session['uid'] = ress.pk  
                    print("User id UID:", request.session['uid'])
                    return HttpResponse("<script>alert('Login to User');window.location='user_home'</script>")
                else:
                    return HttpResponse("<script>alert('Invalid User Type');window.location='login'</script>")
            
        else:
            return HttpResponse("<script>alert('Incorrect credentials');window.location='login'</script>")
    
    return render(request, 'login.html')

def therapist_register(request):
    if 'submit' in request.POST:
        place = request.POST['place']
        fnme = request.POST['fname']
        lnme = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        username = request.POST['username']
        password = request.POST['password']
        logg=Login(username=username,password=password,usertype="pending")
        logg.save()
        codi=Therapist(place=place,fname=fnme,lname=lnme,email=email,phone=phone,login_id=logg.pk)
        codi.save()
        return HttpResponse(f"<script>alert('Added sucessfully');window.location='/login'</script>")

    return render(request,'therapist_register.html')


def user_register(request):
    if 'submit' in request.POST:
        place = request.POST['place']
        fnme = request.POST['fname']
        lnme = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        username = request.POST['username']
        password = request.POST['password']
        logg=Login(username=username,password=password,usertype="user")
        logg.save()
        codi=User(place=place,fname=fnme,lname=lnme,email=email,phone=phone,login_id=logg.pk)
        codi.save()
        return HttpResponse(f"<script>alert('User Added sucessfully');window.location='/login'</script>")
    return render(request,'user_register.html')


def admin_therapistpending(request):
    pending_therapists = Therapist.objects.all()

    return render(request, 'admin_therapistpending.html', {'a': pending_therapists})


#accept_shop
def admin_therapistaccept(request,id2):
    b=Login.objects.get(id=id2)
    b.usertype='therapist'
    b.save()
    return HttpResponse("<script>alert('Therapist Accepted');window.location='/admin_therapistpending'</script>")

#admin_shopreject
def admin_therapistblock(request,id2):
    b=Login.objects.get(id=id2)
    b.usertype='pending'
    b.save()
    return HttpResponse("<script>alert('Admin Blocked');window.location='/admin_therapistpending'</script>")


def admin_therapist(request):
    pending_therapists = Therapist.objects.filter(login__usertype='therapist')

    return render(request, 'admin_viewtherapist.html', {'gi': pending_therapists})


def admin_userview(request):
    df = User.objects.all()

    return render(request, 'admin_userview.html', {'a': df})


def admin_feedback(request):
    df = Feedback.objects.all()

    return render(request, 'admin_feedback.html', {'tea': df})


def admin_viewratings(request):
    df = Rating.objects.all()

    return render(request, 'admin_viewratings.html', {'tea': df})

def admin_passwordchange(request):
    
    admin_user = Login.objects.get(usertype='admin')
    if 'submit' in request.POST:
        passwd = request.POST['pwd']
        admin_user.password = passwd
        admin_user.save()

        return HttpResponse("<script>alert('Password changed successfully');window.location='/admin_passwordchange'</script>")

    return render(request, 'admin_passwordchange.html', {'v': admin_user})


def therapist_schedule(request):
    df = Therapist.objects.get(id=request.session['tid'])
    hw=Schedule.objects.all()
    if 'submit' in request.POST:
        id = request.POST['id']
        week = request.POST['week']
        from_time = request.POST['from_time']
        to_time = request.POST['to_time']
        status = request.POST['status']
        qw=Schedule(therapist_id=id,week=week,from_time=from_time,to_time=to_time,status=status)
        qw.save()
        return HttpResponse("<script>alert('Added successfully');window.location='/therapist_schedule'</script>")

    return render(request, 'therapist_schedule.html', {'v': df,'hw':hw})

def therapist_scheduledelete(request,id2):
    b=Schedule.objects.get(id=id2)
    b.delete()
    return HttpResponse("<script>alert('Deleted');window.location='/therapist_schedule'</script>")


def therapist_scheduleupdate(request,id1):
    uv = Schedule.objects.get(id=id1)
    if 'update' in request.POST:
        week = request.POST['week']
        from_time = request.POST['from_time']
        to_time = request.POST['to_time']
        status = request.POST['status']
        uv.week=week
        uv.from_time=from_time
        uv.to_time=to_time
        uv.status=status
        uv.save()
        return HttpResponse("<script>alert('Updated');window.location='/therapist_schedule'</script>")
    return render(request, 'therapist_schedule.html', {'a': uv})


def therapist_changepasswrd(request):
    
    if 'tid' not in request.session:
        return HttpResponse("<script>alert('Session expired. Please login again.');window.location='/login'</script>")
    
    try:
       therapist = Login.objects.get(pk=request.session['tid'])
    except Login.DoesNotExist:
        return HttpResponse("<script>alert('Camp Coordinator not found. Please login again.');window.location='/login'</script>")

    if 'submit' in request.POST:
        passwd = request.POST['pwd']
        therapist.password = passwd
        therapist.save()

        return HttpResponse("<script>alert('Password changed successfully');window.location='/therapist_changepasswrd'</script>")

    return render(request, 'therapist_changepasswrd.html', {'v': therapist})


def therapist_motivationalvdo(request):
    df = Therapist.objects.get(id=request.session['tid'])
    der=Video.objects.filter(therapist_id=request.session['tid'])
    if 'submit' in request.POST:
        id = request.POST['id']
        title = request.POST['name']
        video=request.FILES['video']
        fs = FileSystemStorage(location='static/media')  # Define folder for storing videos
        filename = fs.save(video.name, video)
        qw=Video(therapist_id=id,title=title,video=filename)
        qw.save()
        return HttpResponse("<script>alert('Video Uploaded Sucessfully');window.location='/therapist_motivationalvdo'</script>")

    return render(request, 'therapist_motivationalvdo.html', {'v': df,'der':der})


def therapist_motivationalvdodelete(request,id2):
    b=Video.objects.get(id=id2)
    b.delete()
    return HttpResponse("<script>alert('Deleted');window.location='/therapist_motivationalvdo'</script>")



from django.db.models import Avg
from django.shortcuts import render
from .models import Rating

def therapist_view_rating(request):
    therapist_id = request.session['tid']  # Assuming 'tid' is the session key for therapist ID
    ratings = Rating.objects.filter(therapist_id=therapist_id)
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    return render(request, 'therapist_viewrating.html', {'ratings': ratings, 'average_rating': average_rating})




def admin_questionmanage(request):
    df = Question.objects.all()
    if 'submit' in request.POST:
        question = request.POST['question']
        qer=Question(question=question)
        qer.save()
        return HttpResponse("<script>alert('Question Added');window.location='/admin_questionmanage'</script>")
    return render(request, 'admin_questionmanage.html', {'tea': df})


# def admin_answermanage(request,id1):
#     df=Question.objects.get(id=id1)
#     return render(request, 'admin_answermanage.html', {'tea': df})


def admin_answermanage(request, id1):
    question = Question.objects.get(id=id1)  # Get the question instance

    if request.method == 'POST':
        # Fetching answers from the form
        answers = [
            {'option': request.POST.get('answer1'), 'status': request.POST.get('status1')},
            {'option': request.POST.get('answer2'), 'status': request.POST.get('status2')},
            {'option': request.POST.get('answer3'), 'status': request.POST.get('status3')},
            {'option': request.POST.get('answer4'), 'status': request.POST.get('status4')},
        ]

        # Check if the question already has answers
        existing_answers_count = Answer.objects.filter(question=question).count()
        if existing_answers_count + len([ans for ans in answers if ans['option']]) > 4:
            return HttpResponse("<script>alert('Cannot add more than 4 answers to this question'); window.location='/admin_answermanage/{}'</script>".format(id1))

        # Save answers in the database
        for ans in answers:
            if ans['option']:  # Ensure that an option is provided
                Answer.objects.create(
                    question=question,
                    option=ans['option'],
                    status=ans['status'] if ans['status'] else "no"
                )

        return HttpResponse("<script>alert('Answers Added Successfully'); window.location='/admin_answermanage/{}'</script>".format(id1))

    # Fetch existing answers for the question
    existing_answers = Answer.objects.filter(question=question)

    # Pass data to template
    context = {
        'tea': question,
        'd': [{'options': ans.option, 'optionstatus': ans.status} for ans in existing_answers],
    }
    return render(request, 'admin_answermanage.html', context)


def admin_questionmanagedelete(request, id2):
    try:
        question = Question.objects.get(id=id2)
        answers = Answer.objects.filter(question=question)
        answers.delete()
        question.delete()
        return HttpResponse("<script>alert('Deleted');window.location='/admin_questionmanage'</script>")
    except Question.DoesNotExist:
        return HttpResponse("<script>alert('Question not found');window.location='/admin_questionmanage'</script>")
    
def admin_questionmanageupdate(request,id1):
    question = Question.objects.get(id=id1)
    if 'update' in request.POST:
        qer = request.POST['question']
        question.question = qer
        question.save()
        return HttpResponse(f"<script>alert('Question Updated');window.location='/admin_questionmanage'</script>")
    return render(request, 'admin_questionmanage.html', {'q': question}) 


def user_quiz(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        selected_option_id = request.POST.get('option_id')
        
        question = get_object_or_404(Question, id=question_id)
        selected_option = get_object_or_404(Answer, id=selected_option_id)
        
        if selected_option.status == 'yes':
            return HttpResponse("<script>alert('Correct answer!');window.location='/user_quiz'</script>")
        else:
            return HttpResponse("<script>alert('Wrong answer!');window.location='/user_quiz'</script>")
    
    else:
        question = Question.objects.first()  # For simplicity, get the first question
        options = Answer.objects.filter(question=question)
        return render(request, 'user_quiz.html', {'question': question, 'options': options})
    
    
def user_bookshedule(request):
    schedules = Schedule.objects.all()
    return render(request, 'user_bookshedule.html', {'schedules': schedules})

def user_bookings(request, id2):
    a=Schedule.objects.get(id=id2)
    if 'submit' in request.POST:
        id = request.POST['id']
        date = request.POST['date']
        time = request.POST['time']
        user_id = request.session['uid']
        Booking.objects.create(
            schedule_id=id,
            user_id=user_id,
            date=date,
            time=time,
            status='Booked'
        )
        return HttpResponse("<script>alert('Booked successfully');window.location='/user_home'</script>")

    return render(request, 'user_bookings.html', {'schedule': a})


# def user_bookings(request, id2):
#     print(f"Request path: {request.path}")  # Log the incoming path
#     schedule = get_object_or_404(Schedule, id=id2)  # Fetch the schedule by ID

#     if request.method == "POST":
#         date = request.POST.get('date')
#         time = request.POST.get('time')

#         # Ensure user session is active
#         user_id = request.session['uid']
#         if not user_id:
#             return HttpResponse("<script>alert('Please log in first.');window.location='/login'</script>")

#         user = get_object_or_404(User, pk=user_id)

#         # Save booking
#         Booking.objects.create(
#             schedule=schedule,
#             user=user,
#             date=date,
#             time=time,
#             status='Booked'
#         )
#         return HttpResponse("<script>alert('Booked successfully');window.location='/user_bookshedule'</script>")

#     return render(request, 'user_bookshedule.html', {'schedule': schedule})



def user_viewbookings(request):
    schedules = Booking.objects.filter(user_id=request.session['uid'])
    if 'view' in request.POST:
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id)
        return HttpResponse(f"<script>alert('Booking Status: {booking.status}');window.location='/user_viewbookings'</script>")
    return render(request, 'user_viewbookings.html', {'d': schedules})

def user_viewmotivationalvdo(request):
    der=Video.objects.all()
    return render(request, 'user_viewmotivationalvdo.html', {'der': der})


def user_sentfeedback(request):
    qwe=Feedback.objects.filter(user_id=request.session['uid'])
    if 'submit' in request.POST:
        feedback = request.POST['feed']
        wer=Feedback(user_id=request.session['uid'],feedback=feedback,reply="Sent",date=timezone.now().date())
        wer.save()
        return HttpResponse("<script>alert('Feedback Sent');window.location='/user_sentfeedback'</script>")
    return render(request, 'user_sentfeedback.html',{'d':qwe})


def user_sentfeedbackdelete(request,id2):
    b=Feedback.objects.get(id=id2)
    b.delete()
    return HttpResponse("<script>alert('Deleted');window.location='/user_sentfeedback'</script>")


def user_rate_therapist(request):
    add=Therapist.objects.all()
   
    return render(request,'user_rate_therapist.html',{'ad':add})



def rate_therapist(request, therapist_id):
    if request.method == 'POST':
        rating = request.POST['rating']
        review = request.POST['review']
        user_id = request.session['uid']
        date = timezone.now().date()
        
        new_rating = Rating(user_id=user_id, therapist_id=therapist_id, rating=rating, review=review, date=date)        
        new_rating.save()
        
        return HttpResponse("<script>alert('Rating submitted successfully');window.location='/user_rate_therapist'</script>")
    
    return render(request, 'rate_therapist.html')



def user_changepasswrd(request):
    
    try:
       user = Login.objects.get(pk=request.session['uid'])
    except Login.DoesNotExist:
        return HttpResponse("<script>alert(' Please login again.');window.location='/login'</script>")

    if 'submit' in request.POST:
        passwd = request.POST['pwd']
        user.password = passwd
        user.save()

        return HttpResponse("<script>alert('Password changed successfully');window.location='/user_changepasswrd'</script>")

    return render(request, 'user_changepasswrd.html', {'v': user})



def therapist_viewbookings(request):
    der=Booking.objects.all()
    therapist_id = request.session.get('tid')
    if not therapist_id:
        return HttpResponse("<script>alert('Session expired. Please login again.');window.location='/login'</script>")

    der = Booking.objects.filter(schedule__therapist_id=therapist_id)
    return render(request, 'therapist_viewbookings.html', {'der': der})

def therapist_viewbookingsconfirm(request,id1):
    aer=Booking.objects.get(id=id1)
    aer.status="Confirmed"
    aer.save()
    return HttpResponse("<script>alert('Confirmed');window.location='/therapist_viewbookings'</script>")


def therapist_viewusers(request):
    der=User.objects.all()
    return render(request, 'therapist_viewusers.html', {'users': der})



# from django.shortcuts import render, redirect
# from .models import Chat
# from django.contrib.auth.decorators import login_required


# def chat_view(request, receiver_id):
#     sender_id = request.session.get('lid')
    
#     if request.method == 'POST':
#         chat_message = request.POST.get('chat')
#         Chat.objects.create(sender_id=sender_id, receiver_id=receiver_id, chat=chat_message)
#         return redirect('chat_view', receiver_id=receiver_id)

#     chats = Chat.objects.filter(sender_id=sender_id, receiver_id=receiver_id) | Chat.objects.filter(sender_id=receiver_id, receiver_id=sender_id)
#     chats = chats.order_by('date')
#     return render(request, 'chat.html', {'chats': chats, 'receiver_id': receiver_id})



def view_therapists(request):
    therapists = Therapist.objects.filter(login__usertype='therapist')
    return render(request, 'user_alltherapist.html', {'therapists': therapists})



# def user_chat(request, id1):
#     therapists = Therapist.objects.get(id=id1)
#     chats = Chat.objects.filter(sender_id=request.session['uid'], receiver_id=id1) | Chat.objects.filter(sender_id=id1, receiver_id=request.session['uid'])
#     chats = chats.order_by('date')
    
#     if 'submit' in request.POST:
#         chat = request.POST['chat_message']
#         ch = Chat(sender_id=request.session['uid'], receiver_id=id1, chat=chat, reply='pending', date=timezone.now().date())
#         ch.save()
#         return HttpResponse("<script>alert('Message Sent');window.location='/user_chat/" + str(id1) + "'</script>")
    
#     return render(request, 'user_chat.html', {'therapists': therapists, 'chats': chats})


from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Therapist, Chat

def user_chat(request, id1):
    therapists = Therapist.objects.get(id=id1)
    chats = Chat.objects.filter(sender_id=request.session['uid'], receiver_id=id1) | Chat.objects.filter(sender_id=id1, receiver_id=request.session['uid'])
    chats = chats.order_by('date')
    
    if 'submit' in request.POST:
        chat = request.POST['chat_message']
        ch = Chat(sender_id=request.session['uid'], receiver_id=id1, chat=chat, reply='pending', date=timezone.now().date())
        ch.save()
        return HttpResponse("<script>alert('Message Sent');window.location='/user_chat/" + str(id1) + "'</script>")
    
    return render(request, 'user_chat.html', {'therapists': therapists, 'chats': chats})



def therapist_chat(request, user_id):
    therapist_id = request.session.get('tid')
    
    chats = Chat.objects.filter(sender_id=user_id, receiver_id=therapist_id) | Chat.objects.filter(sender_id=therapist_id, receiver_id=user_id)
    chats = chats.order_by('date')
    
    if 'submit' in request.POST:
        reply_message = request.POST.get('reply_message')
        chat_id = request.POST.get('chat_id')
        
        # Update the chat with the reply
        chat = Chat.objects.get(id=chat_id)
        chat.reply = reply_message
        chat.save()
        
        return HttpResponse("<script>alert('Reply Sent');window.location='/therapist_chat/" + str(user_id) + "'</script>")
    
    return render(request, 'therapist_chat.html', {'chats': chats, 'user_id': user_id})



def therapist_previousbookings(request):
    ad=Booking.objects.filter(status='Confirmed')
    therapist_id = request.session.get('tid')
    if not therapist_id:
        return HttpResponse("<script>alert('Session expired. Please login again.');window.location='/login'</script>")

    ad = Booking.objects.filter(schedule__therapist_id=therapist_id, status='Confirmed')
    return render(request,'therapist_previousbookings.html',{'ad':ad})


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

                                #/////////////////Chat-Bot///////////////////////////#
from django.shortcuts import render
from django.http import JsonResponse
import textwrap
import google.generativeai as genai
import json


# Google Gemini API Key
GOOGLE_API_KEY = 'AIzaSyAdbPNd0d037Wad2-DZ8PKPzidNJ4H6anE'

genai.configure(api_key=GOOGLE_API_KEY)

model = None
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
        model = genai.GenerativeModel('gemini-1.5-flash')
        break

def to_markdown(text):
    text = text.replace('*', ' ')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

def generate_gemini_response(prompt):
    # Add a specific context for mental health
    context_prompt = f"This conversation focuses on mental health-related advice, support, and wellness. {prompt}"
    response = model.generate_content(context_prompt)
    return response.text


def chatbot(request):
    return render(request, 'chatbot.html')

def chat(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            user_message = body.get('message', '').strip()  # Safely extract and clean the message
        except json.JSONDecodeError:
            return JsonResponse({'response': 'Invalid JSON input.'})

        if not user_message:
            return JsonResponse({'response': 'Please provide a valid message.'})

        # Filter user input for specific topics (e.g., mental health-related)
        if 'mental health' not in user_message.lower():
            return JsonResponse({'response': 'Please ask questions related to mental health details and related content.'})

        # Generate a response
        gemini_response = generate_gemini_response(user_message)
        return JsonResponse({'response': gemini_response})

    return JsonResponse({'response': 'Invalid request method.'})


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////