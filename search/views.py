import pandas as pd
import random
from django.shortcuts import render
from django.http import StreamingHttpResponse
from .query import get_documents, get_index
from .models import TeachingPlan, Slides


df = pd.read_csv('teaching_outline.csv')
document_count = df.shape[0]
avg_document_len = df['text'].str.len().mean()
index = get_index(df)


# Create your views here.
def search_page(request):
    return render(request,'search.html')

def query_info(request,query):
    context = {}
    document_idx = get_documents(query,index,document_count,df,avg_document_len)
    files = []

    for i in document_idx:
        filename = df.at[i,'file_name']
        content = df.at[i,'text']
        star = random.randint(20,50)/10

        TeachingPlan.objects.filter(index=i).delete()
        plan = TeachingPlan.objects.create(index=i,content=content,star=star,filename=filename)
        files.append(plan)
    
    context['files'] = files
    return render(request,'search.html',context)

def download(request,filename):
    filepath = "manage.py"
    response = StreamingHttpResponse(file_iterator(filepath))
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="manage.py"'
    return response


def file_iterator(file_name, chunk_size=1024):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break