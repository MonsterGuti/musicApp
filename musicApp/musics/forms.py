from django import forms
from decimal import Decimal
from musics.models import Album, Song


# -------------------------
# Mixins
# -------------------------
class DisabledFieldMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
            field.widget.attrs['readonly'] = True


# -------------------------
# Album Forms
# -------------------------
class AlbumBaseForm(forms.Form):
    album_name = forms.CharField(max_length=30, required=True, label='Album Name')
    image_url = forms.URLField(required=True, label='Image URL')
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True, label='Price')


class AlbumCreateForm(AlbumBaseForm):
    pass


class AlbumEditForm(AlbumBaseForm):
    pass


class AlbumDeleteForm(DisabledFieldMixin, AlbumBaseForm):
    pass


# -------------------------
# Song Forms
# -------------------------
class SongBaseForm(forms.Form):
    song_name = forms.CharField(max_length=30, required=True, label='Song Name')
    album = forms.ChoiceField(label='Album', choices=[])

    def __init__(self, *args, session=None, **kwargs):
        super().__init__(*args, **kwargs)
        if session:
            self.fields['album'].choices = [
                (album.id, album.album_name) for album in session.query(Album).all()
            ]


class SongCreateForm(SongBaseForm):
    pass
