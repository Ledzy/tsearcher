from django.shortcuts import render
import pandas as pd
from .query import get_documents, get_index


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
    filenames = [df.at[i,'file_name'] for i in document_idx]
    context['filenames'] = filenames
    
    return render(request,'search.html',context)