from django.shortcuts import render

# Create your views here.
from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model, REDIRECT_FIELD_NAME
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.decorators import user_passes_test
from rest_framework.views import APIView


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('myapp/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'myapp/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
            # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')




def logindetails(request):
    context={}
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)

        if request.user.is_authenticated:
            login(request,user)
            return HttpResponseRedirect(reverse('welcomee'))
        else:
            context['error']="provide correct information"
    return render(request, 'myapp/login.html',context)


def welcomee(request):
    context={}
    context['user']=request.user
    return render(request,'myapp/welcome.html', context)


def delete(request, id):
    author = User.objects.get(id=id)
    author.delete()
    return HttpResponse("User deleted")
 #   return redirect("logindetails")

class LoginMemberAPI(APIView):
    def get_queryset(self):
        return User.objects.all()

    def post(self, request, format=None):
        serializer = LoginMemberSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data['email'])
            member = User.objects.get(name = str(serializer.validated_data['name']))
            # serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



'''
def welcomee(request):

    all_users= get_user_model().objects.all()
    
    context= {'allusers': all_users}
        
    return render(request, 'myapp/welcome.html', context)

'''