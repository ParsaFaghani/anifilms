from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.forms.models import inlineformset_factory
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from .models import Profile
from user.models import Follow
from anim.models import anim, anim_sub,anim_video

# from notification.models import FollowNotification
from .forms import UserEditForm, ProfileEditForm, passwordChangeForm, SignupForm, LoginForm

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.core.exceptions import PermissionDenied
import json
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.utils import translation


def check_lang(request):
    if request.user.is_authenticated:
        translation.activate(request.user.user.language)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def signupView(request):
    check_lang(request)
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('user/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request,'لینک تایید ایمیل برای شما ارسال شد. لطفا ایمیل خود را چک کنید')
            return redirect('anime:list')

    else:
        form = SignupForm()
    return render(request,'user/signup.html', {'form':form})

def activate(request, uidb64, token):
    check_lang(request)
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request,user)
        messages.success(request,'حساب شما با موفقیت تایید شد.')
        return redirect('anime:list')
    else:
        messages.error(request,'این لینک نامعتبر است.')
        return redirect('anime:list')


class LoginView(LoginView):
    template_name="user/login.html"
    
    def form_valid(self, form):
        messages.success(self.request, 'شما با موفقیت وارد شدید.')
        return super().form_valid(form)
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return super().get_success_url()


@method_decorator(csrf_exempt, name='dispatch')
class followView(View):

    def post(self, request):
        user_name = request.POST.get('username')
        user2 = User.objects.get(username=user_name)

        following_queryset = request.user.following.all()
        following = [follow.reciever.username for follow in following_queryset]

        if(user2.username in following):
            u = Follow.objects.get(owner=request.user, reciever=user2).delete()
            followed = False
        else:
            u = Follow.objects.get_or_create(owner=request.user, reciever=user2)[0]
            # notification = FollowNotification.objects.create(follow=u)
            followed = True

        html = render_to_string(
            template_name="user/follow.html",
            context={'following':following, 'profile':user2}
        )
        response_data = {}
        response_data['html'] = html
        if request.POST.get("operation") == "follow" and is_ajax(request=request):
            ctx={"followed":followed,"content_id":user_name}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
        return JsonResponse(response_data)    


def followers(request, username):
    check_lang(request)
    profile = get_object_or_404(Profile, user__username=username)
    following_queryset = profile.user.following.all()
    following = [follow.reciever.username for follow in following_queryset]
    return render(request,'user/follow-re-ing.html',{'profile':profile,'following':following,'follow':'followers'})

def following(request, username):
    check_lang(request)
    profile = get_object_or_404(Profile, user__username=username)
    following_queryset = profile.user.following.all()
    following = [follow.reciever.username for follow in following_queryset]
    return render(request,'user/follow-re-ing.html',{'profile':profile,'following':following,'follow':'following'})
    
    
  
@login_required
def profileView(request, username):
    check_lang(request)
    profile = get_object_or_404(Profile, user__username=username)
    saves = request.user.save_owner.all()
    anims_save = [s.anim for s in saves]
    following_queryset = request.user.following.all()
    following = [follow.reciever.username for follow in following_queryset]
    Anim_videos = anim_video.objects.filter(added_by=profile.user).values('anim').distinct()
    Anim_subs = anim_sub.objects.filter(added_by=profile.user).values('anim').distinct()
    anims = anim.objects.filter(id__in=Anim_videos) | anim.objects.filter(id__in=Anim_subs)
    return render(request, 'user/profile.html',{'profile':profile,'following':following, 'anims':anims, 'saves':anims_save})




@login_required
def editView(request):
    check_lang(request)
    if request.method == 'POST':
        u_form = UserEditForm(request.POST, instance=request.user)
        p_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.user)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('accounts:profile',request.user.username)
    else:
        u_form = UserEditForm(instance=request.user)
        p_form = ProfileEditForm(instance=request.user.user)
    context = {
        'u_form':u_form,
        'p_form':p_form,
        'user_image':request.user.user.photo.url,
    }

    return render(request, 'user/edit.html', context)



@login_required
def change_password(request):
    check_lang(request)
    if request.method == 'POST':
        form = passwordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد')
            return redirect('change_password')
        else:
            messages.error(request, 'لطفاً مطمئن شوید که هر دو رمز عبور مطابقت دارند.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {
        'form': form
    })