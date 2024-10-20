from django.urls import path, include
from .views import home, signup, signin, signout, UpdateTask, DeleteTask

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('update-task/<int:id>/', UpdateTask, name='update-task' ),
    path('delete-task/<int:id>/', DeleteTask, name='delete-task')
    
]
