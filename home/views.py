from django.shortcuts import render, HttpResponse, redirect
import os
from . import processVideo


# Create your views here.
def index(request):
    if request.method == "POST":
        videoFormats = [
            "webm",
            "mkv",
            "flv",
            "vob",
            "ogv",
            "ogg",
            "rrc",
            "gifv",
            "mng",
            "mov",
            "avi",
            "qt",
            "wmv",
            "yuv",
            "rm",
            "asf",
            "amv",
            "mp4",
            "m4p",
            "m4v",
            "mpg",
            "mp2",
            "mpeg",
            "mpe",
            "mpv",
            "m4v",
            "svi",
            "3gp",
            "3g2",
            "mxf",
            "roq",
            "nsv",
            "flv",
            "f4v",
            "f4p",
            "f4a",
            "f4b",
            "mod",
        ]
        videoId = None
        video = request.FILES["video"]
        title = str(video)
        videoFormat = title.split(".")[-1]
        videoName = ""
        if videoFormat in videoFormats:
            videoId = 2  # get from DB
            videoName = f"{videoId}.{videoFormat}"
            with open(videoName, "wb+") as f:
                for chunk in video:
                    f.write(chunk)
            subtitleFile = f"{videoId}.srt"
            processVideo.writeSubtitles(videoName, subtitleFile)
            processVideo.saveSubsToDB(videoId)
            processVideo.saveVideoToS3(videoId)
            # os.remove(videoName)
            # os.remove(subtitleFile)
            context = {
                "videoId": videoId,
                "result": [],
                "title": title,
                "processed": True,
            }
            return render(request, "index.html", context)
        else:
            return HttpResponse(
                "<h1>OOPs! an error occured</h1><p>Invalid data supplied</p> "
            )
    return render(request, "index.html")


def search(request):
    if request.method == "POST":
        videoId = request.POST["videoId"]
        phrase = request.POST["phrase"]
        result = processVideo.searchPhrase(phrase, videoId)
        context = {"result": result}
        print(len(result))
        return render(request, "index.html", context)

    else:
        return redirect(request, "/")
