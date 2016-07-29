# Filter

import numpy as np
import wave
import scipy.signal as signal
# import matplotlib.pyplot as plt

def sound_filter(sound, pass_region, stop_region, op):
	wav = wave.open(sound)
	params = wav.getparams()
	nchannels, sampwidth, framerate, nframes = params[:4]
	string_data = wav.readframes(nframes)
	wav.close()

	wave_data = np.fromstring(string_data, dtype=np.short)
	if wave_data.size %	2 != 0:
		wave_data = np.delete(wave_data, -1)
	wave_data.shape = -1, 2
	wave_data = wave_data.T
	time = np.arange(0, nframes) * (1.0/framerate)


	left_channel = wave_data[0]
	wave_length = left_channel.size
	right_channel = wave_data[1]

	#plt.subplot(221)
	#plt.plot(time, left_channel)
	#plt.subplot(222)
	#plt.plot(time, right_channel, c='g')

	new_left_channel, new_right_channel = op(left_channel, right_channel, pass_region, stop_region, framerate)

	wave_data = np.zeros(2*wave_length, dtype=np.short)
	wave_data[::2] = new_left_channel
	wave_data[1::2] = new_right_channel
	wave_data = wave_data.tostring()

	f = wave.open(sound, 'wb')
	f.setnchannels(nchannels)
	f.setsampwidth(sampwidth)
	f.setframerate(framerate)
	f.writeframes(wave_data)
	f.close()

	#plt.subplot(223)
	#plt.plot(time, new_left_channel)
	#plt.subplot(224)
	#plt.plot(time, new_right_channel, c='g')
	#plt.show()

def butterworth_bandpass_filter(left_channel, right_channel, pass_region, stop_region, framerate):
	pass_region = 2*pass_region/framerate
	stop_region = 2*stop_region/framerate
	#print(pass_region, stop_region)
	pass_max_damp = 2
	stop_min_damp = 20
	b, a = signal.iirdesign(pass_region, stop_region, pass_max_damp, stop_min_damp)
	new_left_channel = signal.lfilter(b, a, left_channel)
	new_right_channel = signal.lfilter(b, a, right_channel)
	return new_left_channel, new_right_channel

def fft_bandpass_filter(left_channel, right_channel, pass_region, stop_region, framerate):
	length = left_channel.size
	'''Notice: Sampling frequency = 2*max signal frequency'''
	low = int(pass_region[0]/framerate*length*2)+1
	high = int(pass_region[1]/framerate*length*2)
	left_channel = np.fft.fft(left_channel)
	right_channel = np.fft.fft(right_channel)
	left_channel[:low] = .0
	left_channel[high:] = .0
	right_channel[:low] = .0
	right_channel[high:] = .0
	left_channel = np.fft.ifft(left_channel)
	right_channel = np.fft.ifft(right_channel)
	return left_channel, right_channel

def set_eq(left_channel, right_channel, pass_region, stop_region, framerate):	
	'''We use the EQ set by NETEASE MUSIC, and we use ORDER-3 D1 SPLINE INTERPOLATION to simulate the filter function:
		f(250)=f'(250)=0;
		f(1000)=f'(1000)=0;
		f(500)=1,f'(500)=0'''
	'''We start with a linear transform of x'''
	'''The solution of the problem is:
		f1(x) = -2x^3+9x^2-12x+5, x = x0/250, 250<=x0<=500;
		f2(x) = 3/4x^3-9/4x^2+6x-4, x = 0/250, 500<=x0<=1000.
	'''
	left_frequency = np.fft.fft(left_channel)
	right_frequency = np.fft.fft(right_channel)
	abs_left = abs(left_frequency)
	abs_right = abs(right_frequency)
	length = left_channel.size
	freq = lambda i: i*framerate/(length*2)
	index = lambda freq: int(2*length/framerate*freq)
	#f1 = lambda x: 0.4*(-2*(x**3)+9*(x**2)-12*x+5)
	#f2 = lambda x: 0.4*(0.75*(x**3)-2.25*(x**2)+6*x-4)

	rate1 = 1
	rate2 = 0.8

	f1 = lambda x: rate1*(0.5*np.sin(np.pi*(x-1.5)) + 0.5)
	f2 = lambda x: rate1*(0.5*np.sin(0.5*np.pi*(x-1)) + 0.5)

	x250 = index(250)
	x500 = index(500)
	x1000 = index(1000)

	left_frequency = left_frequency * rate2
	right_frequency = right_frequency * rate2

	left_frequency[x250:x500] = [left_frequency[i]*(1+(2-2*rate2)*f1(freq(i)/250)) for i in range(x250, x500)]
	right_frequency[x250:x500] = [right_frequency[i]*(1+(2-2*rate2)*f1(freq(i)/250)) for i in range(x250, x500)]
	left_frequency[x500:x1000] = [left_frequency[i]*(1+(2-2*rate2)*f2(freq(i)/250)) for i in range(x500, x1000)]
	right_frequency[x500:x1000] = [right_frequency[i]*(1+(2-2*rate2)*f2(freq(i)/250)) for i in range(x500, x1000)]

	left_channel = np.fft.ifft(left_frequency)
	right_channel = np.fft.ifft(right_frequency)

	return left_channel, right_channel





if __name__ == '__main__':
	sound = '/home/chuanlu/sound/HVC842379.wav'
	pass_region = np.asarray([400, 500])
	stop_region = np.asarray([150, 2500])
	sound_filter(sound, pass_region, stop_region, set_eq)