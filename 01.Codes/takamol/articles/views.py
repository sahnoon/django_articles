from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Articles
from django.contrib.auth.decorators import login_required # to be used on favorite lists
import requests
from datetime import datetime
import re
import logging

# Setup the logger for CloudWatch
logging.basicConfig(format=
                    '%(levelname)s (%(asctime)s): file %(filename)s: line %(lineno)d: %(message)s')
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)



def get_slug(title):
    """to generate slug from the title

    Args:
        title (str): string title

    Returns:
        str: slug
    """
    LOGGER.debug("start getting slug for %s", title)
    slug = re.sub('&', '-And-', title) # remove & and replace it with -And-
    slug = re.sub('[^A-Za-z0-9]+', r'-', title) # remove spaces and spical chractre
    LOGGER.debug("slug is: %s", slug)
    return slug

def feed_articles():
    """get the articles from the API
    """
    # TODO remove the APIkey

    url = ('https://newsapi.org/v2/everything?'
       'q=tech&language=en&'
       'from='+datetime.today().strftime('%Y-%m-%d')+'&'
       'sortBy=popularity&'
       'apiKey=92b54ba451c1476c966ecfedaf1c57b3')
    LOGGER.debug("url: %s",url)
    response = requests.get(url)
    LOGGER.debug("status code: %s",response.status_code)
    if response.status_code == 200:
        response = response.json()
        LOGGER.debug("we parsed json response")
        for article in response['articles']:
            
            slug = get_slug(article['title']).lower()
            temp = Articles(title= article['title'],slug= slug,body= article['description'],url_to_image= article['urlToImage'], date= article['publishedAt'])
            temp.save()
        LOGGER.info("fetching articles complated successfully")
        return True
    else:
        LOGGER.error("Failed to get the articles")

        return False
def articles_list(request):
    """article_list is function to manage article list view

    Args:
        request (request): urls request

    Returns:
        html: render template
    """
    # if we have the object the we will show them. or we will create them again then show them.
    if Articles.objects.all():
        LOGGER.debug("We have articles")
        articles = Articles.objects.all().order_by('date');
        return render(request, 'articles/articles_list.html', { 'articles': articles })
    LOGGER.debug("we need to get articles")
    flag = feed_articles()
    if flag:
        LOGGER.debug("we got articles")
        articles = Articles.objects.all().order_by('date');
        return render(request, 'articles/articles_list.html', { 'articles': articles })

def article_detail(request, slug):
    """to show article detail

    Args:
        request (request): urls request
        slug (str): slug string

    Returns:
        html: render html template
    """ 
    # TODO return the article detail
    return HttpResponse(slug)
    article = Articles.objects.get(slug=slug)
    return render(request, 'articles/article_detail.html', { 'article': article })