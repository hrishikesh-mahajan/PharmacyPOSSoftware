import os
from datetime import datetime
from tkinter import END, INSERT, Button, Entry, Label, Text, Tk

import pandas as pd

# Import modules from reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

import Barcode
import Dictionary

now = datetime.now()
date_time = now.strftime("%Y/%m/%d  %H:%M:%S")


window = Tk()


item_index = 1.0

invoice_pdf = "Invoices\\Invoice_" + now.strftime("%Y%m%d_%H%M%S") + ".pdf"

order_history_csv = "History.csv"


def submit():
    excel()
    clear()
    invoice_date.insert(0, date_time)


def excel():
    user = {
        "INVOICE NUMBER": [invoice_number.get()],
        "INVOICE DATE AND TIME": [invoice_date.get()],
        "PATIENT NAME": [patient_name.get()],
        "PATIENT PHONE NUMBER": [patient_phone_number.get()],
        "PATIENT ADDRESS": [patient_address.get()],
        "DOCTOR NAME": [doctor_name.get()],
        " ": " ",
        "CROCIN": "",
        "BENADRYL": "",
        "COFSILS": "",
        "CHARAK KOFOL": "",
        "ASPIRIN": "",
        "CALTRATE VITAMINS": "",
        "IBUPROFEN": "",
        "ANTI-DIARRHEAL": "",
        "MOTIONCALM": "",
        "ACETAMINOPHEN": "",
    }
    a = pd.DataFrame()
    if not os.path.exists(order_history_csv):
        a.to_csv(order_history_csv)
    a = pd.read_csv(order_history_csv, index_col=0)
    b = pd.DataFrame(user)
    a = pd.concat([a, b], ignore_index=True, axis=0)
    # print(a)
    a.index += 1
    a.to_csv(order_history_csv)
    a = pd.read_csv(order_history_csv, index_col=0)
    print(a.index[-1])
    print(a)
    # print(a.iloc[[1]])
    # print(a[-1])


def reset():
    invoice_number.delete(0, END)
    invoice_date.delete(0, END)
    patient_id.delete(0, END)
    patient_name.delete(0, END)
    patient_phone_number.delete(0, END)
    patient_address.delete(0, END)
    doctor_name.delete(0, END)


def str_round(string):
    round_figure = round(float(string), 2)
    if int(round_figure * 10) == (round_figure * 10):
        return str(round_figure) + "0"
    else:
        return str(round_figure)


def scan_item():
    global item_index
    code = Barcode.capture()
    if code in Dictionary.Barcode_Dictionary.keys():
        name = Dictionary.Barcode_Dictionary[code][0]
        price = Dictionary.Barcode_Dictionary[code][1]
        for counter in range(0, int(item_index)):
            line = float(counter) + 1
            s = item_name.get(line, line + 1.0)
            s = s.strip()
            print(".", s.strip(), ".", line)
            print(".", s, ".", line)
            if name == s:
                break
        s = item_name.get(line, line + 1.0)
        s = s.strip()
        if name == s:
            old_item(line)
        else:
            new_item(name, price)
        sum_all()
        align_right()


def new_item(name, price):
    global item_index
    item_number.insert(INSERT, str(int(item_index)) + ".\n")
    item_name.insert(INSERT, name + "\n")
    mrp.insert(INSERT, str_round(price + 0.00) + "\n")
    quantity.insert(INSERT, "1" + "\n")
    rate.insert(INSERT, str_round(price / 1.12) + "\n")
    total.insert(
        INSERT,
        str_round(
            float(rate.get(item_index, "end-1c linestart"))
            * float(quantity.get(item_index, "end-1c linestart"))
        )
        + "\n",
    )
    disc_amt.insert(
        INSERT,
        str_round(
            float(total.get(item_index, "end-1c linestart"))
            * float(discount_percent.get(1.0, END))
            / 100
        )
        + "\n",
    )
    taxable_amt.insert(
        INSERT,
        str_round(
            float(total.get(item_index, "end-1c linestart"))
            - float(disc_amt.get(item_index, "end-1c linestart"))
        )
        + "\n",
    )
    c_gst.insert(
        INSERT,
        str_round(float(taxable_amt.get(item_index, "end-1c linestart")) * 0.06) + "\n",
    )
    s_gst.insert(
        INSERT,
        str_round(float(taxable_amt.get(item_index, "end-1c linestart")) * 0.06) + "\n",
    )
    total_amt.insert(
        INSERT,
        str_round(
            float(mrp.get(item_index, "end-1c linestart"))
            * float(quantity.get(item_index, "end-1c linestart"))
            * (1 - float(discount_percent.get(1.0, END)) / 100)
        )
        + "\n",
    )
    item_index = item_index + 1


def old_item(line):
    current_quantity = int(quantity.get(line, line + 1.0))
    quantity.delete(line, line + 1.0)
    quantity.insert(line, str(current_quantity + 1) + "\n")
    total.delete(line, line + 1.0)
    total.insert(
        line,
        str_round(
            float(rate.get(line, line + 1.0)) * float(quantity.get(line, line + 1.0))
        )
        + "\n",
    )
    disc_amt.delete(line, line + 1.0)
    disc_amt.insert(
        line,
        str_round(
            float(total.get(line, line + 1.0))
            * float(discount_percent.get(1.0, END))
            / 100
        )
        + "\n",
    )
    taxable_amt.delete(line, line + 1.0)
    taxable_amt.insert(
        line,
        str_round(
            float(total.get(line, line + 1.0)) - float(disc_amt.get(line, line + 1.0))
        )
        + "\n",
    )
    c_gst.delete(line, line + 1.0)
    c_gst.insert(
        line, str_round(float(taxable_amt.get(line, line + 1.0)) * 0.06) + "\n"
    )
    s_gst.delete(line, line + 1.0)
    s_gst.insert(
        line, str_round(float(taxable_amt.get(line, line + 1.0)) * 0.06) + "\n"
    )
    total_amt.delete(line, line + 1.0)
    total_amt.insert(
        line,
        str_round(
            float(mrp.get(line, line + 1.0))
            * float(quantity.get(line, line + 1.0))
            * (1 - float(discount_percent.get(1.0, END)) / 100)
        )
        + "\n",
    )


def align_right():
    item_number.tag_add("Right", "1.0", "end")
    mrp.tag_add("Right", "1.0", "end")
    quantity.tag_add("Right", "1.0", "end")
    rate.tag_add("Right", "1.0", "end")
    total.tag_add("Right", "1.0", "end")
    disc_amt.tag_add("Right", "1.0", "end")
    taxable_amt.tag_add("Right", "1.0", "end")
    c_gst.tag_add("Right", "1.0", "end")
    s_gst.tag_add("Right", "1.0", "end")
    total_amt.tag_add("Right", "1.0", "end")
    sum_total.tag_add("Right", "1.0", "end")
    sum_disc_amt.tag_add("Right", "1.0", "end")
    sum_taxable_amt.tag_add("Right", "1.0", "end")
    sum_c_gst.tag_add("Right", "1.0", "end")
    sum_s_gst.tag_add("Right", "1.0", "end")
    sum_total_amt.tag_add("Right", "1.0", "end")


def sum_all():
    sum(total, sum_total)
    sum(disc_amt, sum_disc_amt)
    sum(taxable_amt, sum_taxable_amt)
    sum(c_gst, sum_c_gst)
    sum(s_gst, sum_s_gst)
    sum(total_amt, sum_total_amt)
    sum(total, sum_total)
    sum(disc_amt, sum_disc_amt)
    sum(taxable_amt, sum_taxable_amt)
    sum(c_gst, sum_c_gst)
    sum(s_gst, sum_s_gst)
    sum(total_amt, sum_total_amt)


def sum(data, result):
    count = 0.00
    for counter in range(1, int(item_index)):
        line = float(counter)
        count = count + float(data.get(line, line + 1))
    result.delete("1.0", "end")
    result.insert(1.0, str_round(count))


def clear():
    invoice_number.delete(0, END)
    invoice_date.delete(0, END)
    patient_id.delete(0, END)
    patient_name.delete(0, END)
    patient_phone_number.delete(0, END)
    patient_address.delete(0, END)
    doctor_name.delete(0, END)

    item_number.delete("1.0", "end")
    item_name.delete("1.0", "end")
    mrp.delete("1.0", "end")
    quantity.delete("1.0", "end")
    rate.delete("1.0", "end")
    total.delete("1.0", "end")
    disc_amt.delete("1.0", "end")
    taxable_amt.delete("1.0", "end")
    c_gst.delete("1.0", "end")
    s_gst.delete("1.0", "end")
    total_amt.delete("1.0", "end")
    discount_percent.delete("1.0", "end")
    discount_percent.insert(1.0, "0.00")
    sum_total.delete("1.0", "end")
    sum_disc_amt.delete("1.0", "end")
    sum_taxable_amt.delete("1.0", "end")
    sum_c_gst.delete("1.0", "end")
    sum_s_gst.delete("1.0", "end")
    sum_total_amt.delete("1.0", "end")


def invoice():
    global invoice_pdf
    # data which we are going to display as tables
    data = [
        [
            "Sr. No.",
            "Description of goods",
            "MRP",
            "Qty",
            "Rate",
            "Total",
            "Disc Amt",
            "Taxable Amt",
            "CGST\n@6%",
            "SGST\n@6%",
            "Total Amt\n(inc. Tax)",
        ]
    ]
    # y = 1.00
    for counter in range(0, int(item_index)):
        # global y
        # counter = int(counter)
        # print(type(counter), type(y))
        # print(counter, y)
        y = float(counter) + 1
        data.append(
            [
                item_number.get(y, y + 0.99),
                item_name.get(y, y + 0.99),
                mrp.get(y, y + 0.99),
                quantity.get(y, y + 0.99),
                rate.get(y, y + 0.99),
                total.get(y, y + 0.99),
                disc_amt.get(y, y + 0.99),
                taxable_amt.get(y, y + 0.99),
                c_gst.get(y, y + 0.99),
                s_gst.get(y, y + 0.99),
                total_amt.get(y, y + 0.99),
            ]
        )
        # counter = int(counter)
        # counter -= 1
        # y = y + 1
    data.append(
        [
            "",
            "",
            "",
            "",
            "Total",
            sum_total.get(1.0, 1.99),
            sum_disc_amt.get(1.0, 1.99),
            sum_taxable_amt.get(1.0, 1.99),
            sum_c_gst.get(1.0, 1.99),
            sum_s_gst.get(1.0, 1.99),
            sum_total_amt.get(1.0, 1.99),
        ]
    )
    # creating a Base Document Template of page size A4
    pdf = SimpleDocTemplate(invoice_pdf, pagesize=A4)

    # standard stylesheet defined within reportlab itself
    styles = getSampleStyleSheet()

    # fetching the style of Top level heading (Heading1)
    title_style = styles["Heading1"]

    # 0: left, 1: center, 2: right
    title_style.alignment = 1

    # creating the paragraph with
    # the heading text and passing the styles of it
    title = Paragraph("Invoice", title_style)

    # creates a Table Style object and in it,
    # defines the styles row wise
    # the tuples which look like coordinates
    # are nothing but rows and columns
    style = TableStyle(
        [
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            # ("TEXTCOLOR", (0, 0), (10, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]
    )

    customer_details = [
        ["Invoice", invoice_number.get()],
        ["Date", date_time],
        ["Patient"],
        ["ID", patient_id.get()],
        ["Name", patient_name.get()],
        ["Contact", patient_phone_number.get()],
        ["Address", patient_address.get()],
        ["Doctor Name", doctor_name.get()],
    ]

    # creates a table object and passes the style to it
    customer = Table(customer_details, style=style)
    table = Table(data, style=style)

    # final step which builds the
    # actual pdf putting together all the elements
    # pdf.build([title, customer, "", table, "", "Discount : " + str(discount_percent.get(1.0, END)), "", "Net Payable : " + str(sum_total_amt.get(1.0, END))])
    pdf.build([title, customer, table])


def print_bill():
    invoice()
    reset()
    clear()
    os.startfile(invoice_pdf)


def exit_function():
    window.destroy()
    """
    exit_window = Tk()
    exit_window.title = "Are you sure?"
    Label(exit_window, text="Confirm Exit?").pack()
    Button(
        exit_window,
        text="Yes",
        command=lambda: [window.destroy(), exit_window.destroy()],
    ).pack()
    Button(exit_window, text="No", command=exit_window.destroy).pack()
    exit_window.mainloop()
    """


# window.geometry("1000x400")
window.title("Medical Billing Software")

Label(window, text="Invoice No.").grid(row=0, column=0, sticky="e")
Label(window, text="Invoice Date").grid(row=1, column=0, sticky="e")
Label(window, text="Patient ID").grid(row=2, column=0, sticky="e")
Label(window, text="Patient Name").grid(row=3, column=0, sticky="e")
Label(window, text="Patient Contact").grid(row=4, column=0, sticky="e")
Label(window, text="Patient Address").grid(row=5, column=0, sticky="e")
Label(window, text="Doctor Name").grid(row=6, column=0, sticky="e")

invoice_number = Entry(window, width=25)
invoice_number.grid(row=0, column=1, sticky="w")

invoice_date = Entry(window, width=25)
invoice_date.grid(row=1, column=1, sticky="w")
invoice_date.insert(0, date_time)

patient_id = Entry(window, width=25)
patient_id.grid(row=2, column=1, sticky="w")

patient_name = Entry(window, width=25)
patient_name.grid(row=3, column=1, sticky="w")

patient_phone_number = Entry(window, width=25)
patient_phone_number.grid(row=4, column=1, sticky="w")

patient_address = Entry(window, width=25)
patient_address.grid(row=5, column=1, sticky="w")

doctor_name = Entry(window, width=25)
doctor_name.grid(row=6, column=1, sticky="w")

submit_button = Button(window, text="Submit", command=submit)
submit_button.grid(row=8, column=0)

scan_button = Button(window, text="Scan", command=scan_item)
scan_button.grid(row=8, column=1)

clear_button = Button(window, text="Clear", command=clear)
clear_button.grid(row=8, column=2)

print_button = Button(window, text="Print", command=print_bill)
print_button.grid(row=8, column=3)

exit_button = Button(window, text="Exit", command=exit_function)
exit_button.grid(row=8, column=4)

Label(window, text="NO").grid(row=9, column=0)
Label(window, text="NAME").grid(row=9, column=1)
Label(window, text="MRP").grid(row=9, column=2)
Label(window, text="QTY").grid(row=9, column=3)
Label(window, text="RATE").grid(row=9, column=4)
Label(window, text="TOTAL").grid(row=9, column=5)
Label(window, text="DISC").grid(row=9, column=6)
Label(window, text="TAX AMT").grid(row=9, column=7)
Label(window, text="CGST").grid(row=9, column=8)
Label(window, text="SGST").grid(row=9, column=9)
Label(window, text="TOTAL AMT").grid(row=9, column=10)

item_number = Text(window, height=10, width=4)
item_number.tag_configure("Right", justify="right")
item_number.grid(row=10, column=0)

item_name = Text(window, height=10, width=25)
item_name.grid(row=10, column=1)

mrp = Text(window, height=10, width=6)
mrp.tag_configure("Right", justify="right")
mrp.grid(row=10, column=2)

quantity = Text(window, height=10, width=3)
quantity.tag_configure("Right", justify="right")
quantity.grid(row=10, column=3)

rate = Text(window, height=10, width=6)
rate.tag_configure("Right", justify="right")
rate.grid(row=10, column=4)

total = Text(window, height=10, width=7)
total.tag_configure("Right", justify="right")
total.grid(row=10, column=5)

disc_amt = Text(window, height=10, width=6)
disc_amt.tag_configure("Right", justify="right")
disc_amt.grid(row=10, column=6)

taxable_amt = Text(window, height=10, width=7)
taxable_amt.tag_configure("Right", justify="right")
taxable_amt.grid(row=10, column=7)

c_gst = Text(window, height=10, width=6)
c_gst.tag_configure("Right", justify="right")
c_gst.grid(row=10, column=8)

s_gst = Text(window, height=10, width=6)
s_gst.tag_configure("Right", justify="right")
s_gst.grid(row=10, column=9)

total_amt = Text(window, height=10, width=7)
total_amt.tag_configure("Right", justify="right")
total_amt.grid(row=10, column=10)

Label(window, text="TOTAL").grid(row=11, column=4, sticky="e")

sum_total = Text(window, height=1, width=6)
sum_total.tag_configure("Right", justify="right")
sum_total.grid(row=11, column=5)

sum_disc_amt = Text(window, height=1, width=6)
sum_disc_amt.tag_configure("Right", justify="right")
sum_disc_amt.grid(row=11, column=6)

sum_taxable_amt = Text(window, height=1, width=7)
sum_taxable_amt.tag_configure("Right", justify="right")
sum_taxable_amt.grid(row=11, column=7)

sum_c_gst = Text(window, height=1, width=6)
sum_c_gst.tag_configure("Right", justify="right")
sum_c_gst.grid(row=11, column=8)

sum_s_gst = Text(window, height=1, width=6)
sum_s_gst.tag_configure("Right", justify="right")
sum_s_gst.grid(row=11, column=9)

sum_total_amt = Text(window, height=1, width=7)
sum_total_amt.tag_configure("Right", justify="right")
sum_total_amt.grid(row=11, column=10)


Label(window, text="Discount %").grid(row=11, column=0)
discount_percent = Text(window, height=1, width=6)
discount_percent.grid(row=11, column=1)
discount_percent.insert(1.0, "0.00")

window.mainloop()
