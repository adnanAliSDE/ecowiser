from django.shortcuts import render, HttpResponse, redirect
import os

# from multiprocessing import Process
from . import processVideo
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("subtitles")


# Create your views here.
def index(request):
    if request.method == "POST":
        randomValue = request.POST["csrfmiddlewaretoken"]
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
            videoId = table.item_count + 1  # get from DB
            print(videoId)
            videoName = f"static/videos/vId_{videoId}_{title}"
            print(videoName)
            with open(videoName, "wb+") as f:
                for chunk in video:
                    f.write(chunk)

            subtitleFile = f"{videoId}_{randomValue}_{title}.srt"

            writeStatus = processVideo.writeSubtitles(videoName, subtitleFile)
            if writeStatus in {"empty file", "failed"}:
                return HttpResponse(
                    "Your file doesn't have any subtitles<a href='/'>Go back</a>"
                )
            # processVideo.saveVideoToS3(videoName)

            context = {
                "videoName": videoName,
                "videoId": videoId,
                "result": None,
                "title": title,
                "processed": True,
            }

            processVideo.saveSubsToDB(videoName, subtitleFile, videoId)

            # os.remove(videoName)
            os.remove(subtitleFile)

            return render(request, "index.html", context)
        else:
            return HttpResponse(
                "<h1>OOPs! an error occured</h1><p>Invalid data supplied</p> "
            )

    return render(request, "index.html")


def search(request):
    if request.method == "POST":
        videoId = request.POST["videoId"]
        videoName = request.POST["vName"]
        phrase = request.POST["phrase"]
        result = []
        result = processVideo.searchPhrase(phrase, videoId)
        context = {
            "results": result,
            "processed": True,
            "videoId": videoId,
            "videoName": videoName,
        }
        print(videoId,phrase)
        return render(request, "index.html", context)

    else:
        return redirect(request, "/")
