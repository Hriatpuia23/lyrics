from django.urls import path, include
from .views import (
PostListView,
Search,
Detail,
AlbumList,
ArtistSongList,
SubmitLyrics,
AlbumView,
ArtistListView,
SongList,
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('search/', Search.as_view(), name='search'),
    path('detail/<int:pk>/<slug:slug>/', Detail.as_view(), name='detail'),
    path('album/<str:album>/', AlbumList.as_view(), name='album'),
    path('artist/<str:artist_name>/', ArtistSongList.as_view(), name='artist'),
    path('submit/lyric/', SubmitLyrics.as_view(), name='submit-lyric'),
    path('send/mail/', views.mail, name='send_mail'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('al/list/', AlbumView.as_view(), name='al-list'),
    path('ar/list/', ArtistListView.as_view(), name='ar-list'),
    path('song/list/', SongList.as_view(), name='song-list'),
]