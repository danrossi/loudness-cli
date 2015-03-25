#loudness-cli
Python script to analyze loudness of audio and video files with returned data to be used in programs. Gain adjustment calculated to the target LUFS of -16 by default for web.  using <a href="http://www.ffmpeg.org/">FFmpeg</a> for analysis and gain adjustment.
Run the program with a single argument to video or audio file. The file will be handed to FFmpeg for EBU R128 analysis and loudness stats returned with a gain adjustment value.
Correct usage:
```bash
$ loudness-cli -i /path/to/file.mp4 -s 0 -t -16
```

Where -i is the input file, -s is the audio stream index, -t is the target LUFS. -i is the only required argument.

This file is based on Neg23 however it doesn't do gain adjustments on files, just returns stats data for later processing. Intending on loudness specifications for audio and video players.