# -*- coding: utf-8 -*-
import streamlit as st

import app
import utils

def orderlist():
    orderlist = utils.load_data()

    st.title("Orderlist")
    st.write("Orderlist test")
    st.dataframe(orderlist)