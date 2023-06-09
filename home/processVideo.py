"""Processes the video for subtitles"""
import subprocess
import boto3
import os

os.environ["AWS_PROFILE"] = "adnan"
os.environ["AWS_DEFAULT_REGION"] = "ap-south-1"


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("subtitles")

# for windows
binPath = r"C:\Program Files (x86)\CCExtractor\ccextractorwinfull.exe"

# for linux
# binPath = "ccextractor"


def writeSubtitles(fileName, output="output.srt"):
    command = [
        binPath,
        fileName,
        "-o",
        output,
    ]

    result = subprocess.run(command)
    data = ""
    with open(output, "r") as f:
        data = f.read()

    if result.returncode == 0 and data == "":
        return "empty file"
    elif data != "":
        return "success"
    else:
        raise ValueError("Process failed")


def getSubtitles(videoId):
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("videoId").eq(videoId)
    )
    response = response["Items"][0]["subtitles"]
    return response


def searchPhrase(phrase, videoId):
    subtitles = getSubtitles(videoId)
    result = []
    # searching and returning the items - case insensitive search
    for subtitle in subtitles:
        if phrase.lower() in subtitle["text"].lower():
            result.append(subtitle)
    if result == []:
        result = None

    return result


def parse_subtitles(rawSubtitleFile):
    raw_subtitles = ""
    with open(rawSubtitleFile, "r") as f:
        raw_subtitles = f.read()
    if raw_subtitles == "":
        raise ValueError("Empty subtitle file")
    subtitle_lines = raw_subtitles.strip().split("\n\n")
    subtitle_segments = []

    for line in subtitle_lines:
        lines = line.strip().split("\n")
        start_time, end_time = lines[1].split(" --> ")
        start_time = start_time.split(",")[0]
        end_time = end_time.split(",")[0]
        text = " ".join(lines[2:])
        text = text.strip()

        segment = {"start_time": start_time, "end_time": end_time, "text": text}
        subtitle_segments.append(segment)

    return subtitle_segments


def saveVideoToS3(videoName):
    saved = False
    # s3 = boto3.resource("s3")
    # data = open(videoName, "rb")
    # s3.Bucket("ecowiser-assignment").put_object(Key=videoName, Body=data)
    print(videoName)
    saved = True
    return saved


def saveSubsToDB(videoName, subtitleFile, videoId):
    saved = False
    subtitles = parse_subtitles(subtitleFile)
    table.put_item(
        Item={"videoId": str(videoId), "title": videoName, "subtitles": subtitles}
    )
    saved = True
    return saved
