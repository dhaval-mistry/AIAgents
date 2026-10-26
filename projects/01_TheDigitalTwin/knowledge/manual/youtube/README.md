# YouTube transcript import

YouTube's public feeds supply titles/descriptions, **not full video transcripts**.
YouTube's official captions download API requires owner OAuth permission.

Export captions for YOUR videos from YouTube Studio and put files here.
Name each file using the 11-character video ID:

    dQw4w9WgXcQ.vtt
    dQw4w9WgXcQ.srt
    dQw4w9WgXcQ.txt

This ID is an illustration only, not a video belonging to this project.
Optionally add `videos.json` with `[{"id": "YOUR_VIDEO_ID", "title": "Your real video title"}]`.
Do NOT commit private transcripts or any copyrighted transcript without permission.
Run `python refresh_knowledge.py` to rebuild vectors after updating files.
