import wave

def change_frequency(sound, framerate):
	wav = wave.open(sound, 'rb')
	params = wav.getparams()
	channels, sampwidth, original_framerate, frames = params[:4]
	str_data = wav.readframes(frames)
	wav.close()

	wav2 = wave.open(sound, 'wb')
	wav2.setnchannels(channels)
	wav2.setsampwidth(sampwidth)
	wav2.setframerate(framerate)
	wav2.writeframes(str_data)
	wav2.close()


# sound = sys.argv[1]
# framerate = sys.argv[2]

# change_frequency(sound, framerate)

if __name__ == '__main__':
	framerate = 8000
	sound = 'Downloads/male.wav'
	change_frequency(sound, framerate)
	wav = wave.open(sound[:-4]+'_changed.wav', 'rb')
	params = wav.getparams()
	channels, sampwidth, original_framerate, frames = params[:4]
	print(original_framerate)
