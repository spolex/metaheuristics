#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Init principal
"""

from os.path import join as pj
import os


def data_file(fname):
    """
    acceso a los datos/instancias
    """
    return pj(os.path.split(__file__)[0], fname)
