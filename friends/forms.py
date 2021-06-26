from django import forms


class SearchForFriendForm(forms.Form):
    query_friend_search = forms.CharField(label="",
                                            max_length=255,
                                            widget=forms.TextInput(
                                                attrs={
                                                    'class':'user_search',
                                                    }))