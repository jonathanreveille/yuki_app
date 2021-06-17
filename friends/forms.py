from django import forms


class SearchForFriendForm(forms.Form):
    query_friend_search = forms.CharField(max_length=200, label="")

