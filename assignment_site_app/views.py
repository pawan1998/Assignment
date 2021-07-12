# coding: utf8
from __future__ import unicode_literals
from django.http import response
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
import requests
from assignment_site_app.models import UserSearchDetails
from datetime import date
import datetime
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from assignment_site_app.forms import CreateUserForm, LoginUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import json

# Create your views here.


def registerPage(request):
    """ 
    This view is mapped to rendering a Registration page template 

    Args:
        request: HTTP request object

    Returns:
        JsonResponse: 
    """

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loginpage') 

    context = {'form': form}
    return render(request, 'registerpage.html', context)

def loginPage(request):
    """ 
    This view is mapped to rendering a Login page template 

    Args:
        request: HTTP request object

    Returns:
        JsonResponse: 
    """

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('pageone')

    context = {}
    return render(request, 'loginpage.html', context)   

def logoutUser(request):
    """ 
    This view is mapped to Logging out a user 

    Args:
        request: HTTP request object

    Returns:
        JsonResponse: 
    """

    logout(request)
    return redirect('loginpage')  

@login_required(login_url='loginpage')
def pageone(request):
    """ 
    This view takes into account the request type and then decides based on the params recieved, if the data neds to be 
    stored or updated, whether the actual API needs to be Hit or fetch data from DB 

    Args:
        request: HTTP request object

    Returns:
        JsonResponse: 
    """

    if request.method == 'POST':
        today = date.today()
        date_is = today.strftime("%Y-%m-%d")
        current_user = request.user
        languages_set = ['ar','de','en','es','fr','he','it','nl','no','pt','ru','se','ud','zh']


        if(request.POST.get('filters_applied_query')):

            """ This executes to fetch data from API with applied filters if applied """

            query = request.POST.get('filters_applied_query')
            source = request.POST.get('source')
            language = request.POST.get('language')
            publishedAt = request.POST.get('sort_by_latest')
            result_data = requests.get('https://newsapi.org/v2/everything?q='+query+'&apiKey=0652bf2fbb2547efb7782aaa02919e45').json()
            filter_result_data = requests.get('https://newsapi.org/v2/everything?q='+query+'&source='+source+'&language='+language+'&sortBy='+publishedAt+'&apiKey=0652bf2fbb2547efb7782aaa02919e45').json()   
            filter_result_data = json.dumps(filter_result_data, ensure_ascii=False)
            filter_result_data = json.loads(filter_result_data)
            filter_list_of_articles = filter_result_data.get('articles')
            date_pub = []
            source_name = []
            
            for items in filter_list_of_articles:
                source_name.append(items.get('source').get('name'))
                result_date = items.get('publishedAt')
                result_date = result_date.encode('ascii')
                date_pub.append(result_date)

            source_name = list(set(source_name))
            return render(request, 'pagethree.html', {'context':filter_list_of_articles, 'query':query, 'date_pub':date_pub, 'source_name':source_name, 'languages_set':languages_set })

        else:    

            """ This executes to fetch data from API w/o any filter """

            query = request.POST['search']  
            result_data = requests.get('https://newsapi.org/v2/everything?q='+query+'&apiKey=0652bf2fbb2547efb7782aaa02919e45').json()

        if UserSearchDetails.objects.filter(user=current_user, keyword=query).exists():

            """ This executes to update search term in exisiting User Detail object if exists """
            
            get_user_details = UserSearchDetails.objects.get(user=current_user, keyword=query)
            if ((timezone.now() - get_user_details.timestamp).total_seconds() < 900 ):

                """ This executes if time to last request is less than 15 mins (900 secs), fetch the stored results from DB and update exisiting User Detail object """
                	            
                text = UserSearchDetails.objects.get(user=current_user, keyword=query)
                result_data = text.result
                result_data = json.loads(result_data)
                list_of_articles = result_data.get('articles')
                date_pub = []
                source_name = []
                
                for items in list_of_articles:
                    source_name.append(items.get('source').get('name'))
                    result_date = items.get('publishedAt')
                    result_date = result_date.encode('ascii')
                    # result_date = datetime.datetime.strptime(result_date, "%Y-%m-%d %H:%M:%S")
                    # result_date = result_date.strftime("%Y-%m-%d")
                    # result_date = (result_date[:25] + '..') if len(result_date) > 25 else result_date
                    date_pub.append(result_date)

                source_name = list(set(source_name))    
                return render(request, 'pagethree.html', {'context':list_of_articles, 'query':query, 'date_pub':date_pub, 'source_name':source_name, 'languages_set':languages_set })

            else:    

                """ This executes if time to last request is more than 15 mins (900 secs), fetch the results from API and update exisiting User Detail object """

                result_data = requests.get('https://newsapi.org/v2/everything?q='+query+'&apiKey=0652bf2fbb2547efb7782aaa02919e45').json()
                result_data = json.dumps(result_data, ensure_ascii=False)
                UserSearchDetails.objects.filter(user=current_user,keyword=query).update(keyword=query,result=result_data,timestamp=timezone.now())
                result_data = json.loads(result_data)
                list_of_articles = result_data.get('articles')
                date_pub = []
                source_name = []
                
                for items in list_of_articles:
                    source_name.append(items.get('source').get('name'))
                    result_date = items.get('publishedAt')
                    result_date = result_date.encode('ascii')
                    # result_date = datetime.datetime.strptime(result_date, "%Y-%m-%d %H:%M:%S")
                    # result_date = result_date.strftime("%Y-%m-%d")
                    # result_date = (result_date[:25] + '..') if len(result_date) > 25 else result_date
                    date_pub.append(result_date)
                
                source_name = list(set(source_name))
                return render(request, 'pagethree.html', {'context':list_of_articles, 'query':query, 'date_pub':date_pub, 'source_name':source_name, 'languages_set':languages_set })
        else:

            """ This executes to create a new User Detail object if not exists """

            result_data = requests.get('https://newsapi.org/v2/everything?q='+query+'&apiKey=0652bf2fbb2547efb7782aaa02919e45').json()
            result_data = json.dumps(result_data, ensure_ascii=False)
            entry = UserSearchDetails(user=current_user,keyword=query,result=result_data)
            entry.save()
            result_data = json.loads(result_data)
            list_of_articles = result_data.get('articles')
            date_pub = []
            source_name = []
                
            for items in list_of_articles:
                source_name.append(items.get('source').get('name'))
                result_date = items.get('publishedAt')
                result_date = result_date.encode('ascii')
                # result_date = datetime.datetime.strptime(result_date, "%Y-%m-%d %H:%M:%S")
                # result_date = result_date.strftime("%Y-%m-%d")
                # result_date = (result_date[:25] + '..') if len(result_date) > 25 else result_date
                date_pub.append(result_date)

            source_name = list(set(source_name))
            return render(request, 'pagethree.html', {'context':list_of_articles, 'query':query, 'date_pub':date_pub, 'source_name':source_name, 'languages_set':languages_set })
    else:
        return render(request, 'pageone.html', {})


