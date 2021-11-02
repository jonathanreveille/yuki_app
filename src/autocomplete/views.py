from django.http import JsonResponse

from users.models import User


def complete(request):
    if request.method == "GET":
        searched_term = request.GET.get('term')
        users = User.objects.get_all_by_term(searched_term)
        users = [user.username for user in users]
        return JsonResponse(users, safe=False)
