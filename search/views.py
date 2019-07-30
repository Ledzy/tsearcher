import pandas as pd
import random
import os
from django.shortcuts import render
from django.utils.encoding import escape_uri_path
from django.http import StreamingHttpResponse
from .query import get_documents, get_index
from .models import TeachingPlan, Slides, Subject


df = pd.read_csv('teaching_outline.csv')
document_count = df.shape[0]
avg_document_len = df['text'].str.len().mean()
index = get_index(df)
base_path = os.path.abspath(os.path.join(os.getcwd(), ".."))

# Create your views here.
def search_page(request):
    return render(request,'search.html')

def query_info(request,query):
    context = {}
    document_idx = get_documents(query,index,document_count,df,avg_document_len)
    files = []

    for i in document_idx:
        filename = df.at[i,'file_name'].strip('.txt')
        content = df.at[i,'text']
        subject = df.at[i,'subject']
        star = random.randint(20,50)/10
        subject_model = Subject.objects.filter(type_name=subject)[0]

        TeachingPlan.objects.filter(index=i).delete()
        plan = TeachingPlan.objects.create(index=i,content=content,star=star,filename=filename,subject=subject_model)
        files.append(plan)
    
    context['files'] = files
    return render(request,'search.html',context)

def download(request,file_index):
    filename = df.at[file_index,'file_name'].replace('.txt','.doc')
    filepath = df.at[file_index,'file_path'].replace('.txt','.doc')
    filepath = filepath.replace(r"F:\Desktop\code\Other\Deloitte competition\tsearcher\tsearcher\\","")
    filepath = os.path.join(base_path,filepath)
    response = StreamingHttpResponse(file_iterator(filepath))
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']= "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
    return response


def file_iterator(file_name, chunk_size=1024):
    with open(file_name,'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break