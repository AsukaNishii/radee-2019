#!usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('test.csv', names=['date', 'num'])
plt.plot(range(0,20),df['num'],markar='.')
plt.show()