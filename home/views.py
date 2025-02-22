from django.shortcuts import render
import json
# Create your views here.
def index(request):
    a = request.session.get("user")
    if a:
        print(a["userinfo"]["email"])
    return render(
        request,
        "home/index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )

