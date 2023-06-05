"""Processes the video for subtitles"""
import subprocess


def writeSubtitles(fileName, output="output.srt"):
    command = [
        "C:\\Users\\ansari\Downloads\\CCExtractor_win_portable\\ccextractorwinfull.exe",
        fileName,
        "-o",
        output,
    ]

    result = subprocess.run(command)
    status = "success"
    if result.returncode == 0:
        return status
    else:
        status = "failed"
        return status


def parse_subtitles(rawSubtitleFile):
    raw_subtitles = ""
    with open(rawSubtitleFile, "r") as f:
        raw_subtitles = f.read()

    subtitle_lines = raw_subtitles.strip().split("\n\n")
    subtitle_segments = []

    for line in subtitle_lines:
        lines = line.strip().split("\n")
        start_time, end_time = lines[1].split(" --> ")
        text = " ".join(lines[2:])

        segment = {"start_time": start_time, "end_time": end_time, "text": text}
        subtitle_segments.append(segment)

    return subtitle_segments


def searchPhrase(phrase, videoId):
    result = [
        {
            "startTime": "00:30",
            "endTime": "00:45",
            "text": "Hi there newton was one of the greatest physicists of all time, one of his greatest acheivement was gravity. He his also considered as the father of calculus. If you will study newton's laws then you can get the real taste of his work. Apart from physics he was a good mathematician and was a hosrse of the long race.",
        },
        {
            "startTime": "01:30",
            "endTime": "01:45",
            "text": "Hi there newton was one of the greatest physicists of all time, one of his greatest acheivement was gravity. He his also considered as the father of calculus. If you will study newton's laws then you can get the real taste of his work. Apart from physics he was a good mathematician and was a hosrse of the long race.",
        },
        {
            "startTime": "2:30",
            "endTime": "02:45",
            "text": "Hi there newton was one of the greatest physicists of all time, one of his greatest acheivement was gravity. He his also considered as the father of calculus. If you will study newton's laws then you can get the real taste of his work. Apart from physics he was a good mathematician and was a hosrse of the long race.",
        },
        {
            "startTime": "03:30",
            "endTime": "03:45",
            "text": "Hi there newton was one of the greatest physicists of all time, one of his greatest acheivement was gravity. He his also considered as the father of calculus. If you will study newton's laws then you can get the real taste of his work. Apart from physics he was a good mathematician and was a hosrse of the long race.",
        },
        {
            "startTime": "04:30",
            "endTime": "04:45",
            "text": "Hi there newton was one of the greatest physicists of all time, one of his greatest acheivement was gravity. He his also considered as the father of calculus. If you will study newton's laws then you can get the real taste of his work. Apart from physics he was a good mathematician and was a hosrse of the long race.",
        },
        {
            "startTime": "05:30",
            "endTime": "05:45",
            "text": "Hi there newton was one of the greatest physicists of all time, one of his greatest acheivement was gravity. He his also considered as the father of calculus. If you will study newton's laws then you can get the real taste of his work. Apart from physics he was a good mathematician and was a hosrse of the long race.",
        },
    ]
    return result


def saveVideoToS3(videoId):
    pass


def saveSubsToDB(videoId):
    pass
