import pandas as pd
import random
from django.shortcuts import render
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