from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

# Create your views here.
class HomePageView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'all_posts_list'

class About_us(ListView):
    model = Post
    template_name='about_us.html'

class faq(ListView):
    model = Post
    template_name='faq.html'