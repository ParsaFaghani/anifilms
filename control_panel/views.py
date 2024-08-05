from django.shortcuts import render, get_list_or_404, redirect,get_object_or_404
from django.views import View
from anim.models import anim_video, anim
from .forms import pform, episodForm
from django.conf import settings as s
import boto3
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import random
from anim.forms import animForm, animForme
from user.models import Profile
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import Http404
from django.utils import translation


LIARA = {
    'endpoint': s.AWS_S3_ENDPOINT_URL,
    'accesskey': s.AWS_ACCESS_KEY_ID,
    'secretkey': s.AWS_SECRET_ACCESS_KEY,
    'bucket': s.AWS_STORAGE_BUCKET_NAME
}

def check_lang(request):
    if request.user.is_authenticated:
        translation.activate(request.user.user.language)
    


@login_required
def anims(request):
    check_lang(request)
    if get_object_or_404(Profile,user=request.user).admin == True:
        anims = anim.objects.all()
        return render(request, 'list/anims.html',{'anims':anims})
    else:
        raise Http404

@login_required
def accounts(request):
    check_lang(request)
    if get_object_or_404(Profile,user=request.user).admin == True:
        profiles = Profile.objects.all()
        return render(request, 'list/accounts.html',{'profiles':profiles})
    else:
        raise Http404


@login_required
def create_anim(request):
    check_lang(request)
    if get_object_or_404(Profile,user=request.user).admin == True:
        if request.method == 'GET':
            form = animForme()
            return render(request, 'form/create.html',{'form':form})
        if request.method == 'POST':
            form = animForme(request.POST, request.FILES)
            if form.is_valid():
                if request.user.is_authenticated:
                    anime = anim.objects.create(added_by=request.user, **form.cleaned_data)
                    anime.save()
                    messages.success(request, 'انیمه اضافه شد.')
                    return redirect('ControlPanel:anims')
                else:
                    messages.error(request, 'خطا در افزودن: کاربر احراز هویت نشده است.')
                    return render(request, 'form/create.html',{'form':form})
            else:
                messages.error(request, 'خطا در افزودن')
                return render(request, 'form/create.html',{'form':form})
    else:
        raise Http404


@login_required
def edit_anim(request, anim_id):
    check_lang(request)
    if get_object_or_404(Profile,user=request.user).admin == True:
        anime = get_object_or_404(anim,id=anim_id)
        if request.method == 'GET':
            form = animForme(instance=anime)
            return render(request, 'form/edit.html', {'form':form,'anim':anime})

        if request.method == 'POST':
            form = animForme(request.POST, request.FILES, instance=anime)
            if form.is_valid():
                form.save()
                messages.success(request, 'انیمه ویرایش شد')
                return redirect('ControlPanel:anims')
            else:
                messages.error(request, 'خطا در ویرایش:')
                return render(request, 'form/edit.html',{'form':form,'anim':anime})
    else:
        raise Http404


@login_required
def add_photo(request, anim_id):
    check_lang(request)
    if get_object_or_404(Profile,user=request.user).admin == True:
        anime = get_object_or_404(anim,id=anim_id)
        print('ok1')
        if request.method == 'POST':
            print('ok2')
            form = pform(request.POST, request.FILES)
            if form.is_valid():
                Cloudfile = request.FILES.get('file')
                filename = (anime.name_english +'/' + request.user.username + '/' + str(random.randint(0,99999)) + Cloudfile.name ) 
                s3 = boto3.client('s3',
                    endpoint_url=LIARA['endpoint'],
                    aws_access_key_id=LIARA['accesskey'],
                    aws_secret_access_key=LIARA['secretkey']
                )
                bucket_name = LIARA['bucket']
                anime.photo = Cloudfile
                anime.photo.name = filename
                anime.save()
                return redirect('ControlPanel:anims')
            else:
                return redirect('ControlPanel:anims')
    else:
        raise Http404


@login_required
def view_message(request,redirct,message):
    messages.success(request, message)
    return redirect(redirct)


@login_required
def change_ep(request):
    response_data = {}
    if request.POST.get('action') == 'post' and get_object_or_404(Profile,user=request.user).admin == True:
        video = anim_video.objects.get(id=request.POST.get('id'))
        video.episod = request.POST.get('episod')
        if int(request.POST.get('episod')) <= int(video.anim.max_episod):
            video.save()
            response_data['saved'] = True
            return JsonResponse(response_data)
        else:
            return ValueError
    raise Http404

@login_required
def change_active_status(request):
    response_data = {}
       
    if request.POST.get('action') == 'post' and get_object_or_404(Profile,user=request.user).admin == True and request.user.is_staff:
        anime = anim.objects.get(id=request.POST.get('id'))
        if anime.accepted:
            anime.accepted = False 
            data = {'is_valid': False}
        else:
            anime.accepted = True
            data = {'is_valid': True}
        anime.save()
        
        return JsonResponse(data)
    else:
        raise Http404


@login_required
def set_admin(request):
    response_data = {}
       
    if request.POST.get('action') == 'post' and get_object_or_404(Profile,user=request.user).admin == True and request.user.is_staff:
        user = Profile.objects.get(id=request.POST.get('id'))
        if user.admin:
            user.admin = False 
            data = {'is_valid': False}
        else:
            user.admin = True
            data = {'is_valid': True}
        user.save()
        
        return JsonResponse(data)
    else:
        raise Http404



@login_required
def Upload(request, anim_id):
    check_lang(request)
    if get_object_or_404(Profile,user=request.user).admin == True:
        anime = get_object_or_404(anim,id=anim_id)
        if request.method == 'GET':
            videos_list = anim_video.objects.filter(anim=anime,added_by=request.user).order_by('-episod')
            form = episodForm()
            return render(request, 'upload/upload.html', {'videos': videos_list,'eform':form,'anim':anime})

        if request.method == 'POST':
            form = pform(request.POST, request.FILES)
            if form.is_valid():
                Cloudfile = request.FILES.get('file')
                filename = (anime.name_english +'/' + request.user.username + '/' + str(random.randint(0,99999)) + Cloudfile.name ) 
                videos = anim_video.objects.filter(anim=anime)
                if videos.last():
                    episod = videos.last().episod + 1
                else:
                    episod = 1
                vid_anim = anim_video.objects.create(
                    anim=anime,
                    added_by=request.user,
                    video=filename,
                    episod=episod
                )
                
                vid_anim.video = Cloudfile
                vid_anim.video.name = filename
                vid_anim.save()
                data = {'is_valid': True, 'name': Cloudfile.name, 'url': filename, 'episod':1}
            else:
                data = {'is_valid': False}
        return JsonResponse(data)
    else:
        raise Http404


@login_required
def clear_database(request, anim_id):
    if get_object_or_404(Profile,user=request.user).admin == True:
        anime = get_object_or_404(anim, id=anim_id)
        for photo in anime.anim_video_set.all():
            s3 = boto3.client('s3',
                endpoint_url=LIARA['endpoint'],
                aws_access_key_id=LIARA['accesskey'],
                aws_secret_access_key=LIARA['secretkey']
            )
            bucket_name = LIARA['bucket']
            s3.delete_object(Bucket=bucket_name, Key='media/' + photo.video.name)
            photo.delete()
        return redirect(request.POST.get('next'))
    else:
        raise Http404

@login_required
def delete(request):
    if get_object_or_404(Profile,user=request.user).admin == True:
        response_data = {}
        
        if request.POST.get('action') == 'post':
            video = anim_video.objects.get(id=request.POST.get('video_id'))
            s3 = boto3.client('s3',
                endpoint_url=LIARA['endpoint'],
                aws_access_key_id=LIARA['accesskey'],
                aws_secret_access_key=LIARA['secretkey']
            )
            bucket_name = LIARA['bucket']
            s3.delete_object(Bucket=bucket_name, Key=video.video.name)
            video.delete()
            response_data['saved'] = True
            return JsonResponse(response_data)
    else:
        raise Http404

