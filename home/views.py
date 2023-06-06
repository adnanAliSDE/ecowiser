from django.shortcuts import render, HttpResponse, redirect
import os
from multiprocessing import Process
from . import processVideo
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("subtitles")


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
            videoId = table.item_count + 1  # get from DB
            videoName = f"vId_{videoId}_{title}"
            with open(videoName, "wb+") as f:
                for chunk in video:
                    f.write(chunk)
            subtitleFile = f"{videoId}.srt"
            processVideo.writeSubtitles(videoName, subtitleFile)

            context = {
                "videoId": videoId,
                "result": [],
                "title": title,
                "processed": True,
            }

            # Start the processes
            saveVideo = Process(target=processVideo.saveVideoToS3, args=(videoName,))
            saveSubs = Process(
                target=processVideo.saveSubsToDB,
                args=(videoName, subtitleFile, videoId),
            )

            saveVideo.start()
            saveSubs.start()

            # Wait for the processes to finish
            saveVideo.join()
            saveSubs.join()

            os.remove(videoName)
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
        phrase = request.POST["phrase"]
        videoId = int(videoId)
        result = processVideo.searchPhrase(phrase, videoId)
        context = {"result": result, "processed": True, "videoId": videoId}
        return render(request, "index.html", context)

    else:
        return redirect(request, "/")
