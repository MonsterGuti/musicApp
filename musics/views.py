from django.shortcuts import render, redirect
from musicApp.settings import session
from musicApp.utils import handle_session
from musics.forms import (
    AlbumCreateForm,
    AlbumEditForm,
    AlbumDeleteForm,
    SongCreateForm
)
from musics.models import Album, Song
from decimal import Decimal


# -------------------------
# Album Views
# -------------------------
@handle_session(session)
def index(request):
    context = {'albums': session.query(Album).all()}
    return render(request, 'common/index.html', context)


@handle_session(session)
def create_album(request):
    form = AlbumCreateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        new_album = Album(
            album_name=form.cleaned_data['album_name'],
            image_url=form.cleaned_data['image_url'],
            price=Decimal(form.cleaned_data['price'])
        )
        session.add(new_album)
        session.commit()
        return redirect('index')

    return render(request, 'albums/create-album.html', {"form": form})


@handle_session(session)
def edit_album(request, pk):
    album = session.query(Album).filter_by(id=pk).first()
    if not album:
        return redirect('index')

    if request.method == 'POST':
        form = AlbumEditForm(request.POST)
        if form.is_valid():
            album.album_name = form.cleaned_data['album_name']
            album.image_url = form.cleaned_data['image_url']
            album.price = Decimal(form.cleaned_data['price'])
            session.commit()
            return redirect('details_album', pk=pk)
    else:
        form = AlbumEditForm(initial={
            'album_name': album.album_name,
            'image_url': album.image_url,
            'price': album.price,
        })

    return render(request, 'albums/edit-album.html', {"form": form, "album": album})


@handle_session(session)
def delete_album(request, pk):
    album = session.query(Album).filter_by(id=pk).first()
    if not album:
        return redirect('index')

    if request.method == 'POST':
        session.delete(album)
        session.commit()
        return redirect('index')

    form = AlbumDeleteForm(initial={
        'album_name': album.album_name,
        'image_url': album.image_url,
        'price': album.price,
    })

    return render(request, 'albums/delete-album.html', {"form": form, "album": album})


@handle_session(session)
def details_album(request, pk):
    album = session.query(Album).filter_by(id=pk).first()
    if not album:
        return redirect('index')
    return render(request, 'albums/album-details.html', {"album": album})


# -------------------------
# Song Views
# -------------------------
@handle_session(session)
def create_song(request):
    form = SongCreateForm(request.POST or None, session=session)

    if request.method == 'POST' and form.is_valid():
        new_song = Song(
            song_name=form.cleaned_data['song_name'],
            album_id=int(form.cleaned_data['album'])  # FK
        )
        session.add(new_song)
        session.commit()
        return redirect('details_album', pk=form.cleaned_data['album'])

    return render(request, 'songs/create-song.html', {"form": form})
