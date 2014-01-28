#/usr/bin/env python
#-*- coding:utf-8 -*-
import datetime
import hashlib

from django.shortcuts import HttpResponse, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError

from upfile_form import UpFileForm
from models import droidModel
from DroidBox23.scripts.send_email import mail_again

# from django.http import HttpResponseRedirect
# from django.template import Template,Context
# from django.template.loader import get_template


def upload_form(request):
    form = UpFileForm()
    return render_to_response('upload_template.html',{'form':form})

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        try:
            form = UpFileForm(request.POST,request.FILES)
            if form.is_valid():
                if request.FILES['apk'].name.endswith('apk'):
                    f = handle_upload_file(request.FILES['apk'])
                    md5 = get_file_md5(request.FILES['apk'].name)
                    email = request.POST['email']
                    is_checked = False
                    if not droidModel.objects.filter(md5=md5):
                        model = droidModel(name=request.FILES['apk'],
                                      md5=md5,email=email,is_checked=False,is_sent_email=False)
                        model.save()
                    else:
                        is_checked = True
                        mail_again(md5,email)

                    return render_to_response('success.html',{'file':f,'md5':md5,'email':email,'is_checked':is_checked})
                else:
                    return render_to_response('upload_template.html',{'form':form,'errors':'must be apk file!'})
            else:
                return render_to_response('upload_template.html',{'form':form})
        except MultiValueDictKeyError:
            return render_to_response('upload_template.html',{'errors':'sorry,upload failed!Our website got in some trouble,Please wait'})

###########################非view函数##########################################

def handle_upload_file(f):
    with open('./ApkFile/'+f.name,'wb+') as apk:
        for chunk in f.chunks():
            apk.write(chunk)
        return f

def get_file_md5(f):
    try:
        h = hashlib.md5()
        with open('./ApkFile/'+f,'rb') as apkfile:
            data = apkfile.read()
            h.update(data)
        return h.hexdigest()
    except IOError:
        return "get_md5 failed"



































###test###
def current_datetime(request):
    """get a current time and renturn """
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
#
# def hours_ahead(request,offset):
#     try:
#         offset = int(offset)
#     except ValueError:
#         raise Http404()
#     dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
#     html = "<html><body>In %s hours(s),it will be %s.</body></html>" % (offset,dt)
#     return HttpResponse(html)
#
# def current_datetime_template(request):
#     current_time = datetime.datetime.now()
#     # 第一种方法
#     # t = get_template('teplate_test.html')
#     # html = t.render(Context({'current_time':now}))
#     # return HttpResponse(html)
#     # 第二种方法
#     # return render_to_response('teplate_test.html',{'current_date':now})
#     # 第三种方法
#     return render_to_response('teplate_test.html',locals())

