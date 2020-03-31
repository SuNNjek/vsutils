from vapoursynth import core as _core, GRAY8 as _GRAY8, RGB24 as _RGB24
import math as _math
import functools as _functools
import sys as _sys

def Overlay(bottom, top, x, y):
	# crop the top clip if needed
	if x + top.width > bottom.width:
		top = top.std.CropRel(right=((x + top.width) - bottom.width))
	if y + top.height > bottom.height:
		top = top.std.CropRel(right=((y + top.height) - bottom.height))
	# create a mask for the overlay
	mask = _core.std.BlankClip(clip=top, format=_GRAY8, color=255).std.AddBorders(x, bottom.width - (x + top.width), y, bottom.height - (y + top.height), color=0)
	# add boarders to the top clip
	top = top.std.AddBorders(x, bottom.width - (x + top.width), y, bottom.height - (y + top.height))
	# return return the merged clip
	return _core.std.MaskedMerge(bottom, top, mask)

def Subtitle(clip, message, x, y, font="sans-serif", size=20, align=7, primary_colour="00FFFFFF", secondary_colour="00000000FF", outline_colour="00000000", back_colour="00000000"):
	return clip.assvapour.Subtitle(
		"{\\pos("+str(x)+","+str(y)+")}{\\an"+str(align)+"}" + message, 
		style=font+","+str(size)+",&H"+primary_colour+",&H"+secondary_colour+",&H"+outline_colour+",&H"+back_colour+",0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1",
		blend=True)

def FadeEachFrame(clipa, clipb, n, number_frames):
	weight = (n+1)/(number_frames+1)
	return _core.std.Merge(clipa, clipb, weight=[weight, weight])

def FadeIn(clip, duration):
	fps = clip.fps_num/clip.fps_den
	number_frames = _math.ceil(duration * fps)
	return CrossFade(_core.std.BlankClip(clip, length=number_frames), clip, duration)

def FadeOut(clip, duration):
	fps = clip.fps_num/clip.fps_den
	number_frames = _math.ceil(duration * fps)
	return CrossFade(clip, _core.std.BlankClip(clip, length=number_frames), duration)

def CrossFade(clip1, clip2, duration):
	fps = clip1.fps_num/clip1.fps_den
	number_frames = _math.floor(duration * fps) - 2
	clip1_start_frame = clip1.num_frames - (number_frames + 1)
	clip1_end_frame = clip1.num_frames - 1
	clip2_start_frame = 1
	clip2_end_frame = number_frames + 1
	a=clip1[0:clip1_start_frame]
	b1=clip1[clip1_start_frame:clip1_end_frame]
	b2=clip2[clip2_start_frame:clip2_end_frame]
	b=_core.std.FrameEval(b1, _functools.partial(FadeEachFrame, clipa=b1, clipb=b2, number_frames=number_frames))
	c=clip2[clip2_end_frame:clip2.num_frames]
	return a+b+c

def Colorbars(width=640, height=480, fpsnum=25, fpsden=1, format=_RGB24, duration=600):
	length = round((duration*fpsnum)/fpsden)
	colorbars = _core.std.BlankClip(width=width, height=height, fpsnum=fpsnum, fpsden=fpsden, format=_RGB24, color=[16,16,16], length=length)
	top_width = _math.ceil(width / 7.0)
	bottom_width = _math.ceil(width / 6.0)
	bottom_width_small = _math.ceil(top_width/3)
	top_height = _math.ceil(height * 2 / 3.0)
	bottom_height = _math.ceil(height / 4.0)
	mid_height = height - top_height - bottom_height
	top_colors = [
		[180, 180, 180],
		[180, 180, 16],
		[16, 180, 180],
		[16, 180, 16],
		[180, 16, 180],
		[180, 16, 16],
		[16, 16, 180]
	]
	for (i, color) in enumerate(top_colors):
		colorbars = Overlay(colorbars, _core.std.BlankClip(width=top_width, height=top_height, fpsnum=fpsnum, fpsden=fpsden, format=_RGB24, color=color, length=length), i * top_width, 0)
	mid_colors = [
		[16, 16, 180],
		[16, 16, 16],
		[180, 16, 180],
		[16, 16, 16],
		[16, 180, 180],
		[16, 16, 16],
		[180, 180, 180]
	]
	for (i, color) in enumerate(mid_colors):
		colorbars = Overlay(colorbars, _core.std.BlankClip(width=top_width, height=mid_height, fpsnum=fpsnum, fpsden=fpsden, format=_RGB24, color=color, length=length), i * top_width, top_height)
	bottom_colors = [
		[0, 58, 98],
		[235, 235, 235],
		[75, 15, 126]
	]
	for (i, color) in enumerate(bottom_colors):
		colorbars = Overlay(colorbars, _core.std.BlankClip(width=bottom_width, height=bottom_height, fpsnum=fpsnum, fpsden=fpsden, format=_RGB24, color=color, length=length), i * bottom_width, top_height + mid_height)
	colorbars = Overlay(colorbars, _core.std.BlankClip(width=bottom_width_small, height=bottom_height, fpsnum=fpsnum, fpsden=fpsden, format=_RGB24, color=[0,0,0], length=length), 5 * top_width, top_height + mid_height)
	colorbars = Overlay(colorbars, _core.std.BlankClip(width=bottom_width_small, height=bottom_height, fpsnum=fpsnum, fpsden=fpsden, format=_RGB24, color=[25,25,25], length=length), (5 * top_width) + (bottom_width_small * 2), top_height + mid_height)
	
	return colorbars.resize.Point(format=format, matrix_s="709")

def GetFrameTime(clip, frame_number):
	clip_fps = clip.fps_num / clip.fps_den
	all_in_seconds = frame_number / clip_fps
	minutes = _math.floor(all_in_seconds / 60)
	seconds = _math.floor(all_in_seconds) % 60
	milliseconds = _math.floor((all_in_seconds - _math.floor(all_in_seconds)) * 1000)
	return "{:1.0f}:{:02.0f}.{:03.0f}".format(minutes, seconds, milliseconds)

def TimeEachFrame(clip, n, x, y, align):
	time = GetFrameTime(clip, n)
	frame = str(n)
	text = frame+" - "+time
	
	clip = Subtitle(clip, text, x, y, align=align)
	return clip

def ShowFrameAndTime(clip, x=0, y=0, align=7):
	return clip.std.FrameEval(_functools.partial(TimeEachFrame, clip=clip, x=x, y=y, align=align))
