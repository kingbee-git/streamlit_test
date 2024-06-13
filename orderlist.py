# -*- coding: utf-8 -*-
import streamlit as st

import utils
import app


def orderlist():
    orderlist = utils.load_data()

    st.title("Orderlist")
    st.write("Orderlist test")
    st.dataframe(orderlist)