#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms

class UpFileForm(forms.Form):
    email = forms.EmailField(required=True)
    apk = forms.FileField(required=True)

