def set_eq(left, right, p_r, s_r, framerate):
	rate1 = 1
	rate2 = 0.8
	rate3 = (2-2*rate2)
	left_freq = np.fft.fft(left) * rate2
	right_freq = np.fft.fft(right) * rate2
	length = left.size

	f1 = np.vectorize(lambda x: rate1*(0.5*np.sin(np.pi*(x-1.5)) + 0.5))
	f2 = np.vectorize(lambda x: rate1*(0.5*np.sin(0.5*np.pi*(x-1)) + 0.5))
	freq = np.vectorize(lambda i: i*framerate/(length*2))
	index = lambda freq: int(2*length/framerate*freq)

	x250 = index(250)
	x500 = index(500)
	x1000 = index(1000)

	xx1 = f1(freq(np.asarray(range(x250, x500))))
	xx2 = f2(freq(np.asarray(range(x500, x1000))))

	left_freq[x250:x500] = left_freq[x250:x500] * (1+rate3*xx1)
	right_freq[x250:x500] = right_freq[x250:x500] * (1+rate3*xx1)
	left_freq[x500:x1000] = left_freq[x500:x1000] * (1+rate3*xx2)
	right_freq[x500:x1000] = right_freq[x500:x1000] * (1+rate3*xx2)

	left = np.fft.ifft(left_freq)
	right = np.fft.ifft(right_freq)

	return left, right