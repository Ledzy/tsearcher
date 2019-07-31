import pandas as pd
import random
import os
from django.shortcuts import render
from django.utils.encoding import escape_uri_path
from django.http import StreamingHttpResponse
from .query import get_documents, get_index, get_slides
from .models import TeachingPlan, Slides, Subject


plan_df = pd.read_csv('teaching_outline.csv')
document_count = plan_df.shape[0]
avg_document_len = plan_df['text'].str.len().mean()
index = get_index(plan_df)
# base_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
base_path = os.getcwd()
slide_df = pd.read_csv('slides.csv')
index_slide = get_index(slide_df)

top_count = 10
#更新科目计数
for subject in Subject.objects.all():
    subject_name = subject.type_name
    subject.slide_count = slide_df['subject'].value_counts().get(subject_name,0)
    subject.plan_count = plan_df['subject'].value_counts().get(subject_name,0)


# if os.name!='nt':
#     plan_df = preprocess(plan_df)

# Create your views here.
def search_page(request):
    return render(request,'search.html')

def query_teaching_plan(request,query):
    context = {}
    document_idx = get_documents(query,index,document_count,plan_df,avg_document_len)
    files = []

    for i in document_idx:
        filename = plan_df.at[i,'file_name'].strip('.txt')
        content = plan_df.at[i,'text']
        subject = plan_df.at[i,'subject']
        star = random.randint(20,50)/10
        subject_model = Subject.objects.filter(type_name=subject)[0]

        TeachingPlan.objects.filter(index=i).delete()
        plan = TeachingPlan.objects.create(index=i,content=content,star=star,filename=filename,subject=subject_model)
        files.append(plan)
    
    context['subjects'] = Subject.objects.all()
    context['query'] = query
    context['files'] = files
    context['is_teaching_plan'] = True
    return render(request,'search.html',context)

def query_slide(request,query):
    context = {}
    slide_idx = get_slides(query,index_slide,slide_df)
    files = []

    for i in slide_idx:
        filename = slide_df.at[i,'file_name'].strip('.ppt')
        subject = slide_df.at[i,'subject']
        star = random.randint(20,50)/10
        subject_model = Subject.objects.filter(type_name=subject)[0]

        Slides.objects.filter(index=i).delete()
        slide = Slides.objects.create(index=i,star=star,filename=filename,subject=subject_model)
        files.append(slide)
    
    context['subjects'] = Subject.objects.all()
    context['query'] = query
    context['files'] = files
    context['is_teaching_plan'] = False
    return render(request,'search.html',context)
    

def download_plan(request,file_index):
    filename = plan_df.at[file_index,'file_name'].replace('.txt','.doc')
    strip_path = r"F:\Desktop\code\Other\Deloitte competition\tsearcher\tsearcher"
    filepath = plan_df.at[file_index,'file_path'].replace('.txt','.doc')
    filepath = filepath.replace(strip_path,"")[1:]

    if os.name != 'nt':
        filepath = filepath.replace('\\','/')

    filepath = os.path.join(base_path,filepath)
    response = StreamingHttpResponse(file_iterator(filepath))
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']= "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
    return response

def download_slide(request,file_index):
    filename = slide_df.at[file_index,'file_name']
    filepath = slide_df.at[file_index,'file_path']
    strip_path = r"F:\Desktop\code\Other\Deloitte competition\tsearcher\tsearcher"
    filepath = filepath.replace(strip_path,"")[1:]
    
    if os.name != 'nt':
        filepath = filepath.replace('\\','/')
    
    filepath = os.path.join(base_path,filepath)
    response = StreamingHttpResponse(file_iterator(filepath))
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']= "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
    return response

def query_subject_plan(request,subject_name):
    context = {}
    # document_idx = get_documents(query,index,document_count,plan_df,avg_document_len)
    document_idx = plan_df.loc[plan_df.subject==subject_name].index[:top_count]
    files = []

    for i in document_idx:
        filename = plan_df.at[i,'file_name'].strip('.txt')
        content = plan_df.at[i,'text']
        subject = plan_df.at[i,'subject']
        star = random.randint(20,50)/10
        subject_model = Subject.objects.filter(type_name=subject)[0]

        TeachingPlan.objects.filter(index=i).delete()
        plan = TeachingPlan.objects.create(index=i,content=content,star=star,filename=filename,subject=subject_model)
        files.append(plan)

    context['subjects'] = Subject.objects.all()
    context['files'] = files
    context['is_teaching_plan'] = True
    return render(request,'search.html',context)


def query_subject_slide(request,subject_name):
    context = {}
    # slide_idx = get_slides(query,index_slide,slide_df)
    slide_idx = slide_df.loc[slide_df.subject==subject_name].index[:top_count]
    files = []

    for i in slide_idx:
        filename = slide_df.at[i,'file_name'].strip('.ppt')
        subject = slide_df.at[i,'subject']
        star = random.randint(20,50)/10
        subject_model = Subject.objects.filter(type_name=subject)[0]

        Slides.objects.filter(index=i).delete()
        slide = Slides.objects.create(index=i,star=star,filename=filename,subject=subject_model)
        files.append(slide)
    
    context['subjects'] = Subject.objects.all()
    context['files'] = files
    context['is_teaching_plan'] = False
    return render(request,'search.html',context)


def file_iterator(file_name, chunk_size=1024):
    with open(file_name,'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

# if use non-windows system, process path
def preprocess(plan_df):
    strip_path = r"F:\Desktop\code\Other\Deloitte competition\tsearcher\tsearcher"
    for i, row in plan_df.iterrows():
        row['file_path'] = row['file_path'].replace('.txt','.doc')
        row['file_path'] = row['file_path'].replace(strip_path,'')[1:]
        row['file_path'] = row['file_path'].replace('\\','/')

        # print(row['file_path'])
    return plan_df