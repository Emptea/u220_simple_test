import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, sample_rate=1e6, frequency=1000, duty_cycle=0.1):
        gr.sync_block.__init__(self,
            name='Square with flexible duty',
            in_sig=None,
            out_sig=[np.float32])
        
        self.sample_rate = sample_rate
        self.frequency = frequency
        self.samples_per_period = sample_rate / frequency
        self.phase = 0
        
        # Register parameters
        self.sample_rate = sample_rate
        self.frequency = frequency
        self.duty_cycle = duty_cycle

    def work(self, input_items, output_items):
        out = output_items[0]
        n_samples = len(out)
        
        for i in range(n_samples):
            pos_in_period = self.phase / self.samples_per_period
            
            if pos_in_period < self.duty_cycle:
                out[i] = 1.0
            else:
                out[i] = 0.0
            
            self.phase += 1
            if self.phase >= self.samples_per_period:
                self.phase -= self.samples_per_period
        
        return n_samples
