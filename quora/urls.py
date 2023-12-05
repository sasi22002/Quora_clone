from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls import handler404, handler500
from django.conf import settings
import json
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def not_found_view(request,*args, **kwargs):
    return JsonResponse({'message': 'URL NOT FOUND','status':False,'status_code':404,"data":[]}, status=404)


urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include([
            path('accounts/', include('masteradmin.urls')),
            path('<path:dummy>/', not_found_view),

        
        ])),
        path('api/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
        path('<path:dummy>/', not_found_view),

       
    ]



