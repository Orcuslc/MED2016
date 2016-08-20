import numpy as np
import wave
import matplotlib.pyplot as plt
import scipy.signal as signal

def segment_bandpass_filter(left, right, freq_low, freq_high, framerate):
	length = len(left)
	'''Sampling frequency = 2 * max frequency'''
	low = int(freq_low/framerate*length*2)+1
	high = int(freq_high/framerate*length*2)
	left = np.fft.fft(left)
	right = np.fft.fft(right)
	left[:low] = 0.0
	left[high:] = 0.0
	right[:low] = 0.0
	right[high:] = 0.0
	left = np.fft.ifft(left)
	right = np.fft.ifft(right)
	return left, right


def noise_reduction(sound, freq_low = 499, freq_high = 3501, op = segment_bandpass_filter):

	wav = wave.open(sound)
	params = wav.getparams()
	channels, sampwidth, framerate, frames = params[:4]
	str_data = wav.readframes(frames)
	wav.close()

	wave_data = np.fromstring(str_data, dtype = np.short)
	wave_data.shape = -1, 2
	wave_data = wave_data.T
	time = np.arange(0, frames) * (1.0/framerate)

	left = wave_data[0]
	length = len(left)
	right = wave_data[1]

	plt.subplot(221)
	plt.plot(time, left)
	plt.subplot(222)
	plt.plot(time, right, c='g')

	left, right = op(left, right, freq_low, freq_high, framerate)

	plt.subplot(223)
	plt.plot(time, left)
	plt.subplot(224)
	plt.plot(time, right, c='g')
	plt.show()

	wave_data = np.zeros(2*length, dtype = np.short)
	wave_data[::2] = left
	wave_data[1::2] = right
	wave_data = wave_data.tostring()

	f = wave.open('/home/chuanlu/test/HVC998004_changed.wav', 'wb')
	f.setnchannels(channels)
	f.setsampwidth(sampwidth)
	f.setframerate(framerate)
	f.writeframes(wave_data)
	f.close()


def continuous_bandpass_filter(left, right, freq_low, freq_high, framerate):
	pass_region = [0.075, 0.2]
	stop_region = [0.05, 0.8]
	pass_max_damp = 1
	stop_min_damp = 80
	b, a = signal.iirdesign(pass_region, stop_region, pass_max_damp, stop_min_damp)
	w, h = signal.freqz(b, a)
	new_left = signal.lfilter(b, a, left)
	new_right = signal.lfilter(b, a, right)
	return new_left, new_right

def naive_dsp(left, right, freq_low, freq_high, framerate):
	low_pass = 0.05
	low_stop = 0.1
	high_pass = low_stop
	high_stop = low_pass
	pass_max_damp = 2
	stop_min_damp = 40

	b1, a1 = signal.iirdesign(low_pass, low_stop, pass_max_damp, stop_min_damp)
	b2, a2 = signal.iirdesign(high_pass, high_stop, pass_max_damp, stop_min_damp)

	left = signal.lfilter(b1, a1, left)
	right = signal.lfilter(b1, a1, right)

	new_left = left - right
	new_right = left - right

	left = signal.lfilter(b2, a2, new_left)
	right = signal.lfilter(b2, a2, new_right)

	return left, right

#def naive_naive_dsp(left, right, freq_low, freq_high, framerate):


if __name__ == '__main__':
	sound = "/home/chuanlu/test/HVC998004.wav"
	noise_reduction(sound, 300, 3000, continuous_bandpass_filter)