# python_VideoChopper
Efficiently chops a video into sections based on an EDL file.

Copyright (c) 2021 Robin Parmar. MIT License.

**Requirements**

- Python 3.6 or greater
- FFmpeg recent build
- Blackmagic DaVinci Resolve 16+ or some other EDL source

**Process**

In Resolve, add Timeline markers to indicate where the source clip(s) should be split.
Be sure each of these has a unique name. The quick way to do this is to tap "M" to
add a marker and immediately tap "M" again to name. Or, use "shift-M" to edit an
existing marker. Ensure you have a marker to indicate the end of the final segment
you wish to create.

Render the entire file in the format required.

Export an EDL file by following these steps:
1. Go to the Media Pool.
2. Right-click on your Timeline to get the context menu.
3. Choose "Timelines" > "Export" > "Timeline Markers to EDL"

Edit the Configuration class below to correctly specify the input files.

A typical command looks like this:

> fmpeg -i input_file -ss 00:12.3 -to 00:24.6 -c copy -map 0 output_file

No transcoding occurs, ensuring the fastest possible speed.
However, clips may not be frame accurate, depending on the input file.

**Resources**

Watch the tutorial video:
https://youtu.be/3suPx9r3kpI

**Version**
1.01 4 May 2021 added video link and name change
1.00 2 May 2021
