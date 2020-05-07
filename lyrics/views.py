from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Album, Artist
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    FormView,
)
from django.db.models import Q
from django.core.mail import send_mail
from .forms import SubmitLyric
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from hitcount.views import HitCountDetailView
from django.contrib import messages


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 10
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['artist_list'] = Artist.objects.order_by('artist_name')
        context['album_list'] = Album.objects.order_by('album')
        return context

    def get_queryset(self):
        return Post.published.filter().order_by('-id')


class Search(ListView):
    model = Post
    template_name = 'blog/search.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ["-id"]
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.published.filter(
                Q(artist__icontains=query) |
                Q(artists__artist_name=query) |
                Q(album__icontains=query) |
                Q(title__icontains=query) |
                Q(albums__album=query)
            )
        else:
            object_list = self.model.published.none()
        return object_list


class Detail(HitCountDetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    count_hit = True
    #
    # def get_context_data(self, **kwargs):
    #     context = super(Detail, self).get_context_data(**kwargs)
    #     context.update({
    #         'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
    #     })
    #     return context


class AlbumList(ListView):
    model = Post
    template_name = 'blog/album.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ["-id"]

    def get_context_data(self, **kwargs):
        context = super(AlbumList, self).get_context_data(**kwargs)
        user = get_object_or_404(Album, album=self.kwargs.get('album'))
        context['album_list'] = Album.objects.filter(album=user).order_by('-id')
        return context

    def get_queryset(self):
        user = get_object_or_404(Album, album=self.kwargs.get('album'))
        return Post.published.filter(albums=user).order_by('-id')


class ArtistSongList(ListView):
    model = Post
    template_name = 'blog/artist_song_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ["-id"]
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(ArtistSongList, self).get_context_data(**kwargs)
        user = get_object_or_404(Artist, artist_name=self.kwargs.get('artist_name'))
        context['artist_list'] = Artist.objects.filter(artist_name=user).order_by('-id')
        return context

    def get_queryset(self):
        user = get_object_or_404(Artist, artist_name=self.kwargs.get('artist_name'))
        return Post.published.filter(artists=user).order_by('-id')


class SubmitLyrics(SuccessMessageMixin, FormView):  # LoginRequiredMixin hi Post siam tur chuan login a ngai tih na.
    form_class = SubmitLyric
    template_name = 'blog/submit_lyric.html'
    success_url = reverse_lazy('submit-lyric')
    success_message = 'Lyrics has been successful submitted'

    def form_valid(self, form):
        form.save()
        return super(SubmitLyrics, self).form_valid(form)


def mail(request):
    if request.method == "POST":
        name = request.POST['name']
        user_email = request.POST['email']
        message = request.POST['message']
        send_mail(
            name,
            message,
            user_email,
            ['hriatahpa6@gmail.com']
        )
        messages.info(request, 'Thanks ' + name + ' ! We received your email and will respond shortly...')
        return redirect('send_mail')
    else:
        return render(request, 'blog/email_form.html', {})


class SongList(ListView):
    model = Post
    template_name = 'blog/List/song_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'song'
    paginate_by = 15

    def get_queryset(self):
        return Post.published.filter().order_by('-id')


class AlbumView(ListView):
    model = Album
    template_name = 'blog/List/album_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'album'
    paginate_by = 15


class ArtistListView(ListView):
    model = Artist
    template_name = 'blog/List/artist_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'artist'
    paginate_by = 15

