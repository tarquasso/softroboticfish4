#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Fri Jul 10 03:11:37 2015
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from optparse import OptionParser

class top_block(gr.top_block):

    def __init__(self, txstr, carrier=10000, samp_rate = 80000, bw=4000, amp=1):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate 
        self.carrier = carrier 

        ##################################################
        # Blocks
        ##################################################
        self.blocks_vector_source_x_1 = blocks.vector_source_b(tuple(bytearray(txstr)), False, 1, [])
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_LSB_FIRST)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(([0,1,1,0]), 2)

        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, samp_rate/bw)
        #XXX Hack: 0.07 should actually be parameter amp, but RPI crashes
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, carrier, 0.07, 0)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.audio_sink_0 = audio.sink(samp_rate, "")

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vector_source_x_1, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_repeat_0, 0))

        self.connect((self.blocks_repeat_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.audio_sink_0, 0))

def send(txstr, carrier, samp_rate, bw, amp):
    tb = top_block(txstr, carrier, samp_rate, bw, amp)
    tb.start()
    tb.wait()

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("-m", "--message", dest="txstr", default="Hello World!",
                      help="set tx string MSG", metavar="MSG")
    parser.add_option("-c", "--carrier", dest="carrier", default=10000, type="int",
                      help="set carrier to FREQ (Hz)", metavar="FREQ")
    parser.add_option("-s", "--samprate", dest="samp_rate", default=80000, type="int",
                      help="set sample rate to RATE (Hz)", metavar="RATE")
    parser.add_option("-b", "--bandwidth", dest="bw", default=4000, type="int",
                      help="set bandwidth to BW (Hz)", metavar="BW")
    parser.add_option("-a", "--amplitude", dest="amp", default=1, type="float",
                      help="set amplitude to AMP", metavar="AMP")

    (options, args) = parser.parse_args()

    send(options.txstr, options.carrier, options.samp_rate, options.bw, options.amp)

