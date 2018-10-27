from django.shortcuts import render
from Application.forms import UserForm, UserProfileInfoForm
from django.views.generic import View, TemplateView, ListView, DetailView
from . import models
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


class SchoolListView(ListView):
    context_object_name = 'schools'
    model = models.School
    template_name = 'Application/school_list1.html'

class SchoolDetailView(DetailView):
    context_object_name = 'school_detail'
    model = models.School
    template_name = 'Application/school_detail1.html'

# # Create your views here.
class IndexView(TemplateView):
    template_name = 'basic_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inject'] = 'injection'
        return context



# def index(request):
#     return render(request, 'basic_app/index.html')


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html', {'registered': registered, 'user_form': user_form,
                                                           'profile_form': profile_form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account not active')
        else:
            print('Login and failed')
            print(str(username))
            return HttpResponse('Invalid login')
    else:
        return render(request, 'basic_app/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def special(request):
    return HttpResponse("You are logged in, nice!")



from django.shortcuts import render
from django.http import HttpResponse
from urllib import request
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
import re
import datetime

# Create your views here.

def show(request):
    driver = webdriver.Chrome('C://chromedriver')
    url_to_parse = 'https://auto.ria.com/legkovie/subaru/?page=2'
    driver.get(url_to_parse)
    html = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(html, "html.parser").find_all('section', {"class": "ticket-item new__ticket t paid"})
    for block in soup:
        print(block.find("a", {"class": "m-link-ticket"}).get("href"))

    return render(request, 'Application/Main.html')
#parse each currency
#     for link in links:
#         #get and read link into html
#         req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
#         html = urlopen(req).read()
#         #convert to BS4
#         bs = BeautifulSoup(html, "html.parser")
#         #use soup to find all tables
#         table = bs.find("table")
#         #use soup to find all inner tr and put content into rows[]
#         rows = table.findAll(lambda tag: tag.name == 'tr')
#         #go throu each element in rows using regex to match what we need
#         for element in rows:
#             match = re.search("mfcur-nbu-full-wrap", str(element))
#             #if match by class name use another regex
#             if match:
#                 nums = re.findall(r'\s\d{2}\.\d{3}\s', str(element))
#                 #if matching regex contains nums we will get [] of matching nums
#                 for n in nums:
#                     #and then append to list
#                     mylist.append(n)
#             else:
#                 print()
#     #put into context
#     context1 = {
#         "usd_buy": mylist[0],
#         "usd_sell": mylist[1],
#         "euro_buy": mylist[2],
#         "euro_sell": mylist[3],
#         "head": head,
#         "date": datetime.datetime.now(),
#         #"tweets": tweets
#     }
# def show(request):
#
#     #CoinMarketCal
#     req = Request("https://coinmarketcal.com/", headers={'User-Agent': 'Mozilla/5.0'})
#     html = urlopen(req).read()
#     bs = BeautifulSoup(html, "html.parser")
#     Title = {}
#     articles = bs.findAll("article")
#     i = 0
#     for article in articles:
#         card_date = article.select('h5')
#         for element in card_date:
#             if "card__coins" in str(element):
#                 Title.update({"card__coins"+str(i): re.sub(r"<.*?>", "", element.getText().strip())})
#             if "card__date" in str(element):
#                 Title.update({"card__date"+str(i): re.sub(r"<.*?>", "", element.getText().strip())})
#             if "card__title" in str(element):
#                 Title.update({"card__title"+str(i): re.sub(r"<.*?>", "", element.getText().strip())})
#         tag_p = article.p.getText()
#         Title.update({"card__description"+str(i): str(tag_p.lstrip())})
#
#         myurl = article.find("a", {"class": "btn-sm btn btn-border-b btn-circle btn-block"}).get("href")
#         Title.update({"source"+str(i): str(myurl)})
#
#         div_vote = article.find("div", {"class": "progress__votes"})
#         votes = div_vote.getText()
#         votes_num = str(re.findall(r'\d+?\s', str(votes)))[2:-4]
#         Title.update({"votes"+str(i): votes_num})
#
#         span_vote = str(article.find("div", {"class": "progress-bar"}))
#         m = re.match(r'<div aria-valuemax="100" aria-valuemin="0" aria-valuenow="(?P<value>\d{3}|\d{2}\.?\d*|\d{0}).*', span_vote)
#         # if m:
#         #     print(m.group('value'))
#         # else:
#         #     print(type(m))
#         n = m.group('value')
#         Title.update({"votes_perc"+str(i): n})
#         #vote_perc = re.match(r".*(?P<value>\d{2}\.\d*).*", str(article.find("div", {"class": "progress-bar"})))
#         #Title.update({"votes_perc" +str(i): str(vote_perc.group("value"))})
#
#         i = i+1
#
#
#     #links for currency
#     links = ['https://minfin.com.ua/currency/banks/usd/', 'https://minfin.com.ua/currency/banks/eur/']
#     mylist = list()
#     #template = loader.get_template("Main.html")
#
#     #head = ''
#     # get and read link into html
#     req = Request("https://minfin.com.ua/currency/banks/usd/", headers={'User-Agent': 'Mozilla/5.0'})
#     html = urlopen(req).read()
#     # convert to BS4
#     bs = BeautifulSoup(html, "html.parser")
#
#     # get some data
#     head = bs.find("h1").getText()
#
#     #parse each currency
#     for link in links:
#         #get and read link into html
#         req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
#         html = urlopen(req).read()
#         #convert to BS4
#         bs = BeautifulSoup(html, "html.parser")
#         #use soup to find all tables
#         table = bs.find("table")
#         #use soup to find all inner tr and put content into rows[]
#         rows = table.findAll(lambda tag: tag.name == 'tr')
#         #go throu each element in rows using regex to match what we need
#         for element in rows:
#             match = re.search("mfcur-nbu-full-wrap", str(element))
#             #if match by class name use another regex
#             if match:
#                 nums = re.findall(r'\s\d{2}\.\d{3}\s', str(element))
#                 #if matching regex contains nums we will get [] of matching nums
#                 for n in nums:
#                     #and then append to list
#                     mylist.append(n)
#             else:
#                 print()
#     #put into context
#     context1 = {
#         "usd_buy": mylist[0],
#         "usd_sell": mylist[1],
#         "euro_buy": mylist[2],
#         "euro_sell": mylist[3],
#         "head": head,
#         "date": datetime.datetime.now(),
#         #"tweets": tweets
#     }
#     #context = dict(context1, **Title)
#     context1.update(Title)
#
#     #use render on our template and add context and request
#     #return HttpResponse(template.render(context, request))
#     #another way to return page
#     return render(request, 'Application/Main.html', context1)