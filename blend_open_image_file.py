#
#  Copyright (c) 2015 Shane Ambler
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import bpy
from sys import argv
import os

# UV Editing
blenderImageScreenName = 'ImageViewer'
# Video Editing
blenderMovieScreenName = 'MovieViewer'

acceptedImgFiles = ['.bmp', '.cin', '.dpx',  '.exr',
                    '.hdr', '.jpg', '.jpeg', '.jp2',
                    '.j2k', '.png', '.rgb',  '.tga',
                    '.tif'
                    ]
acceptedMovFiles = ['.avi',  '.flv', '.h264', '.mov',
                    '.mpeg', '.mpg', '.mp2',  '.mp3',
                    '.mp4',  '.mkv', '.ogg',  '.xvid'
                    ]

fileStartIdx = argv.index('--') + 2
numFilesToOpen = len(argv) - fileStartIdx
showAreaType = 'image'
curChann = 1

for i in range(numFilesToOpen):
    filename = argv[fileStartIdx + i]
    ext = os.path.splitext(filename)[1].lower()

    if ext in acceptedImgFiles:
        bpy.ops.image.open(filepath=os.path.abspath(argv[fileStartIdx + i]))
    elif ext in acceptedMovFiles:
        # while we will open video files, blender isn't the best option here
        # When opening multiple videos, each video is imported into a new track
        # tracks after the first will be muted to prevent a terrifying
        # mess of multiple audio tracks
        # end frame is set to the longest video track imported
        # frame rate is left default and will need to be adjusted for each video
        nc = bpy.context.scene.sequence_editor.sequences.new_movie(name=argv[fileStartIdx + i],
                filepath=os.path.abspath(argv[fileStartIdx + i]), frame_start=1, channel=curChann)
        if bpy.context.scene.frame_end < nc.frame_duration:
            bpy.context.scene.frame_end = nc.frame_duration
        # I expected new_movie() to import video and sound
        # but that doesn't happen so we also add sound from the same file
        nca = bpy.context.scene.sequence_editor.sequences.new_sound(name=argv[fileStartIdx + i],
                filepath=os.path.abspath(argv[fileStartIdx + i]), frame_start=1, channel=curChann+1)
        if curChann > 1:
            nc.mute = True
            nca.mute = True
        curChann += 2
        showAreaType = 'video'
    else:
        print("Don't know what type of file this is -",filename)

if showAreaType == 'image':
    bpy.context.window.screen = bpy.data.screens[blenderImageScreenName]
    # make first image active
    for area in bpy.data.screens[blenderImageScreenName].areas:
        if area.type == 'IMAGE_EDITOR':
            area.spaces.active.image = bpy.data.images[0]
else:
    bpy.context.window.screen = bpy.data.screens[blenderMovieScreenName]

