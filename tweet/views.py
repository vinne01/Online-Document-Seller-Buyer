from django.shortcuts import render
#import Tweet from models and tweetform form form
from .models import Tweet
from .forms import  TweetForm,UserRegistrationForm
from django.shortcuts import get_list_or_404,redirect,get_object_or_404
#decorate help to prevent from login only login user edit or delete or update
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
#for sending gmail import library
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from .forms import HealthcareServiceForm
import razorpay


# Razorpay client setup
client = razorpay.Client(auth=("rzp_test_kW8rMFTvHKTTSU", "QMeAga0CCVDybdDKhNvd3cc0"))

# Create your views here.
def index(request):
    return render(request,'index.html')
# def tweet_list(request):
#     tweets=Tweet.objects.all().order_by('-created_at')
#     return render(request,'tweet_list.html',{'tweets':tweets})
def tweet_list(request):
    query = request.GET.get('search', '')
    if query:
        #here syntax (Q(description/name/title __icontains=query)) where name,descr..,title is also name of model
        tweets = Tweet.objects.filter(Q(description__icontains=query)).order_by('-created_at')
    else:
        tweets = Tweet.objects.all().order_by('-created_at')
    
    return render(request, 'tweet_list.html', {'tweets': tweets})
@login_required
def tweet_create(request):
    if request.method=='POST':
     form= TweetForm(request.POST,request.FILES)
     if form.is_valid():
         tweet=form.save(commit=False)
         tweet.user=request.user
         tweet.save()
         return redirect('tweet_list')
     
    else:
     form=TweetForm()
    return render(request,'tweet_form.html',{'form':form})
#for edit and delete one id is required
@login_required
def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user) 
    
    if request.method == 'POST':
        form=TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')
   
    else:
        form=TweetForm(instance=tweet)
    return render(request,'tweet_form.html',{'form':form})
@login_required
def tweet_delete(request,tweet_id):
 tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
 if request.method == 'POST':
     tweet.delete()
     return redirect('tweet_list')
 return render(request,'tweet_confirm_delete.html',{'tweet':tweet})

def register(request):
  if request.method == "POST":
     form=UserRegistrationForm(request.POST)
     if form.is_valid():
         user=form.save(commit=False)
         user.set_password(form.cleaned_data['password1'])
         user.save()
         login(request,user)
         return redirect('tweet_list')
  else:
   form=UserRegistrationForm()  
 
  return render(request,'registration/register.html',{'form':form}) 
def about(request):
    return render(request,'about.html')

#logic for sends emails
def index(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        class_name = request.POST.get('class')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Construct the email message
        full_message = f"Name: {name}\nClass: {class_name}\nSubject: {subject}\n\nMessage:\n{message}"
        
        # Send the email
        send_mail(
            subject,               # Subject of the email
            full_message,          # Message body
            settings.EMAIL_HOST_USER,  # From email
            ['vku563786@gmail.com'],   # Recipient list
            fail_silently=False
        )
    
    return render(request, 'emailform.html')
# def detail(request):
#     return render(request,'#')

#edited part

#payment integration part
@login_required
def paywithrazorpay(request):
    if request.method == 'POST':
        tweet_id = request.POST.get('tweet_id')
        tweet = Tweet.objects.get(id=tweet_id)

        # Amount should be in paise (1 INR = 100 paise)
        amount = int(tweet.price )* 100  # Converting INR to paise

        # Create an order with Razorpay
        payment = client.order.create({
            'amount': amount,  # Amount in paise
            'currency': 'INR',
            'payment_capture': '1'
        })

        # You may save the payment details in your database for further reference
        order_id = payment['id']
        # Here, you could save this order id to the user's record or tweet record if necessary
        
        
        

        # Send back the order details to the frontend
        return render(request, 'payment.html', {
            'order_id': order_id,
            'amount': amount / 100,  # Convert back to INR for display
            'tweet': tweet,
           
        })

    return redirect('tweet_list')

# A success page after payment
  # Construct URLs for document and preview image

@csrf_exempt
def success(request):
    tweet_id = request.GET.get('tweet_id')
    tweet = Tweet.objects.get(id=tweet_id)
    document_url = tweet.document.url if tweet.document else None
    preview_image_url = tweet.preview_image.url if tweet.preview_image else None
    return render(request, "success.html",{
           'document_url': document_url,
          'preview_image_url': preview_image_url
    })
