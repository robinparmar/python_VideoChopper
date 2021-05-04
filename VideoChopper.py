"""
	PROGRAM
		VideoChopper.py

	DESCRIPTION
		Efficiently chops a video file into sections, based on an EDL file.

	COPYRIGHT
		(c) 2021 Robin Parmar <robin@robinparmar.com>. MIT License.

	REQUIREMENTS
		Python 3.6 or greater
		FFmpeg recent build
		Blackmagic DaVinci Resolve 16+ or some other EDL source

	PROCESS
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
			ffmpeg -i input_file -ss 00:12.3 -to 00:24.6 -c copy -map 0 output_file

		No transcoding occurs, ensuring the fastest possible speed.
		However, clips may not be frame accurate, depending on the input file.

	RESOURCES
		Watch the tutorial video:

	HOME
		https://github.com/robinparmar/python_VideoChopper

	VERSION
		1.00 2 May 2021
"""
import os

# convenient place to hold settings
class Configuration:
	# name of EDL file
	edl = "input.edl"

	# name of input video file
	input = "input.mov"

	# output folder
	output = "./result/"

	# frame rate of input video file
	fps = 24.

	# do you want more ffmpeg output?
	verbose = False

# execution starts here
def main():
	# array of text lines from EDL file
	content = []

	# read file, accumulating lines with contents
	print()
	with open(cfg.edl) as f:
		for line in f:
			line = line.strip()
			if len(line) > 0:
				content.append(line)

	# first two lines are junk
	content = content[2:]

	# collection of segments
	segments = Collection(content)
	segments.fix()
	segments.run()

# list of Segment instances
class Collection:
	collect = []

	def __init__(self, content):
		# temporary Segment instance
		s = None

		# flag tracks a data record, which is split over two lines
		firstLine = True

		# create instances
		for line in content:
			tokens = line.split()

			if firstLine:
				# create instance with start time, eg: "01:00:00:00"
				s = Segment(tokens[4])
			else:
				# augment instance with name, eg: "|M:marker01"
				s.addName(tokens[1])
				self.collect.append(s)

			firstLine = not firstLine

	def fix(self):
		# a segment ends where the next one begins
		for i in range(len(self.collect)-1):
			s1 = self.collect[i]
			s2 = self.collect[i+1]
			s1.addStop(s2.start)
			self.collect[i] = s1

		# we no longer need the last entry
		self.collect.pop( len(self.collect)-1 )

	def run(self):
		# run system commands for entire collection
		print()
		print("dividing \"{}\" into segments:".format(cfg.input))

		for s in self.collect:
			s.dump()
			os.system( s.makeCommand() )

		print()

# an individual video segment
class Segment:
	template = "ffmpeg {}-i {} -ss {} -to {} -c copy -map 0 {}{}{}"
	quiet = "-hide_banner -loglevel error "

	start = ""
	stop = ""
	name = ""

	def __init__(self, start):
		# trim prefix, eg. "01:00:00:00" -> "00:00:00"
		self.start = self.convert( start[3:] )

	def addStop(self, stop):
		self.stop = stop

	def addName(self, name):
		# trim prefix, eg. "|M:marker01" -> "marker01"
		self.name = name[3:]

	def makeCommand(self):
		extra = ""
		if not cfg.verbose:
			extra = self.quiet

		ext = os.path.splitext(cfg.input)[1]

		return self.template.format(extra, cfg.input, self.start, self.stop, cfg.output, self.name, ext)

	def dump(self):
		print( "  {}: {}-{}".format(self.name, self.start, self.stop) )

	def convert(self, s):
		# convert time format to decimal, eg. "00:13:13" -> "00:13.54"
		# calculation depends on the frame rate
		parts = s.split(":")

		if parts[2] == "00":
			frac = "0"
		else:
			frac = str( float(parts[2]) * 100. / cfg.fps )[3:6]

		return "{}:{}.{}".format(parts[0], parts[1], frac)

if __name__ == '__main__':
	cfg = Configuration()
	main()
