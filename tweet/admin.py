from django.contrib import admin
#after migrate commonds then used models class
from .models import Tweet
# Register your models here.




admin.site.register(Tweet)