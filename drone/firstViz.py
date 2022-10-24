from cnn_test import *
import streamlit as st
import numpy as np
import pandas as pd


chart_data1 = MinimalSubscriber.test()

st.line_chart(chart_data1)