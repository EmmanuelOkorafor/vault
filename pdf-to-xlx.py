# Copyright (c) 2026 Flare by Goyerv Ltd. All rights reserved.

import fitz  # PyMuPDF
import pandas as pd
import re 
from num2words import num2words 
from openpyxl import load_workbook 
from openpyxl.drawing.image import image 
from openpyxl.styles import Font, Alignment 


pdf_path = "reciept.pdf"
excel_path = "PAYMENT VOUCHER.xlsx"

doc = fitz.open(pdf_path)

transactions = []
sm_counter = 1

amount_pattern = re.compile(r"")
narration_keywords = ["narration", "description", "details"]

for page in doc:
    text = page.get_text().lower()
    lines = text.split("\n")

    narration = None
    amount = None 

    for line in lines:
        if any(keyword in line for keyword in narration_keywords):
            narration = line

            amount_match = amount_pattern.search(line)
            if amount_match:
                raw_amount = amount_match.group(1)
                cleaned_amount = float(raw_amount.replace(",", ""))
                amount = cleaned_amount 

            if narration and amount:
