from django.shortcuts import render, redirect, HttpResponse,get_list_or_404, get_object_or_404
from .models import anim, anim_video, anim_sub, View
from user.models import Save
from django.conf import settings as s
import boto3
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from time import gmtime, strftime
import datetime
import django
from taggit.models import Tag
from functools import reduce
from operator import or_
from django.db.models import Count,Avg,Q
from datetime import datetime, timedelta



LIARA = {
    'endpoint': s.LIARA_ENDPOINT,
    'accesskey': s.LIARA_ACCESS_KEY,
    'secretkey': s.LIARA_SECRET_KEY,
    'bucket': s.LIARA_BUCKET_NAME
}


def home(request):
    return render(request, 'anim/index.html')
    
    
def list(request):
    top_anime = anim.objects.annotate(view_count=Count('view')).order_by('-view_count', 'ratings__average').distinct()[:4]
    
    # Calculate the average rating for each anim
    anims = anim.objects.annotate(average_ratings=Avg('ratings__average'))

    paginator = Paginator(get_list_or_404(anims) , 20)

    page_number = request.GET.get('page')
    if page_number is not None and page_number != "":
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = paginator.get_page(1)
    totalpage=  page_obj.paginator.num_pages
    tags = Tag.objects.all()
    context = {
        'anims': page_obj,
        'page_number':page_number,
        'totalpage':totalpage,
        'tags':tags,
        'top_anime': top_anime,
    }

    if request.method == 'GET':
        query = request.GET.get('q')
        genre = request.GET.get('genre')
        rating = request.GET.get('rating')
        lookups = []
        if genre is not None and genre != "":
            lookups.append(Q(tags__slug=genre))
        if rating is not None and rating != "":
            lookups.append(Q(ratings__average__gte=rating))

        if query is not None and query != "":
            lookups.append(Q(name_english__icontains=query) | Q(name_Japanese__icontains=query) | Q(name_farsi__icontains=query) | Q(description__icontains=query))

        if lookups:
            print('lookups')
            anims = anim.objects.filter(reduce(or_, lookups)).distinct()

        context={
            'anims': anims,
            'tags':tags,
            'top_anime': top_anime,
            'page_number':page_number,
            'totalpage':totalpage
        }
    return render(request, 'anim/anims.html',context)


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    common_tags = anim.tags.most_common()
    posts = anim.objects.filter(tags=tag)
    top_anime = anim.objects.annotate(view_count=Count('view')).order_by('-view_count', 'ratings__average').distinct()[:4]
    context = {
        'tag':tag,
        'tags':common_tags,
        'top_anime': top_anime,
        'anims':posts,
    }
    return render(request, 'anim/anims.html', context)

def view(request,anim_name):
    anime = get_object_or_404(anim,name_Japanese=anim_name)
    anim_videos = anim_video.objects.filter(anim=anime)
    anim_subs = anim_sub.objects.filter(anim=anime)
    translators = set([video.added_by for video in anim_videos] + [sub.added_by for sub in anim_subs])
    similar = anime.tags.similar_objects()[:4]
    if not request.session.get(f'viewed-{anime.id}', False):
        View.objects.create(anim=anime)
        request.session[f'viewed-{anime.id}'] = True

    return render(request,'anim/view.html',context={'anim':anime,'similars':similar,'translators':translators})

def view_video(request, video_id):
    video = anim_video.objects.get(id=video_id)
    
    return render(request,'anim/play_anime.html',context={'video':video})

def SaveView(request, pk):
    post = get_object_or_404(anim, id=pk)
    save = Save(owner=request.user, anim=post)
    try:
        save.save()  # In case of duplicate key
    except IntegrityError as e:
        pass
    return redirect('accounts:profile',request.user.username)


def get_media(request, media_key):
    s3 = boto3.client('s3',
        endpoint_url=LIARA['endpoint'],
        aws_access_key_id=LIARA['accesskey'],
        aws_secret_access_key=LIARA['secretkey']
    )
    bucket_name = LIARA['bucket']
    file_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': 'media/' + media_key},
        ExpiresIn=3600  # 1 hour expiry
    )
    return redirect(file_url)

def delete_file(request, file_code):
    s3 = boto3.client('s3',
        endpoint_url=LIARA['endpoint'],
        aws_access_key_id=LIARA['accesskey'],
        aws_secret_access_key=LIARA['secretkey']
    )
    bucket_name = LIARA['bucket']
    s3.delete_object(Bucket=bucket_name, Key='media/' + file_code)
    return redirect('list_file')


