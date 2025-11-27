from django.urls import path, include
from musics.views import index, create_album, edit_album, delete_album, details_album, create_song

urlpatterns = [
    path('', index, name='index'),
    path('album/', include([
        path('create/', create_album, name='create_album'),
        path('<int:pk>/', include([
            path('edit/', edit_album, name='edit_album'),
            path('delete/', delete_album, name='delete_album'),
            path('details/', details_album, name='details_album'),
        ])),
    ])),
    path('song/', include([
        path('create/', create_song, name='create_song'),
    ]))
]
