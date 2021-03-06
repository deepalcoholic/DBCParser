import numpy as py
from bitarray import bitarray

class lz77_compressor:
    def __init__(self, window_size = 20):
        max_window_size = 100
        self.window_size = min(window_size, max_window_size)
        self.lookahead_buf_size = 15 # 4 bits
    def compress(self, data, verbose = False):
        outputBuf = bitarray(endian = 'big')
        i = 0
        while i < len(data):
            match = self.findLongestMatch(data, i)

            if match:
                (bestMatchDistance), (bestMatchLength) = match
                outputBuf.append(True)
                outputBuf.frombytes(chr(bestMatchDistance >> 4))
                if verbose:
                    print "<1,%i, %i>" % (bestMatchDistance, bestMatchLength) 
                i += bestMatchLength
            else:
                outputBuf.append(False)
                outputBuf.frombytes(data[i])
                if verbose:
                    print "<0, %s>" % data[i]
                i += 1
        # fill the buffer with zeros if the # of bits is not a multiple of 8
        outputBuf.fill()
        return outputBuf


    def findLongestMatch(self, data, current_pos):
        end_of_buf = min(current_pos + self.lookahead_buf_size, len(data)+1)
        best_match_distance = -1
        best_match_length = -1

        for j in range(current_pos+2, end_of_buf):
            start_idx = max(0, current_pos - self.window_size)
            substring = data[current_pos:j]
            for i in range(start_idx, current_pos):
                repititions = len(substring) / (current_pos - i)
                last = len(substring) % (current_pos - i)
                matched_string = data[i:current_pos] * repititions + data[i:i + last]
                if matched_string == substring and len(substring) > best_match_length:
                    best_match_distance = current_pos - i
                    best_match_length = len(substring)
        if best_match_distance > 0 and best_match_length >0:
            return (best_match_distance, best_match_length)
        return None


