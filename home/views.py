from django.shortcuts import render, HttpResponse


# Create your views here.
def index(request):
    if request.method == "POST":
        testValue = request.POST["test"]
        src = request.FILES
        print(testValue)
        # print(type(src.video))
    return render(request, "index.html")
