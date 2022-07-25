import os
from datetime import datetime
from tkinter import *

import matplotlib.pyplot as plt
import pandas as pd

# Import modules from reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

import Barcode

now = datetime.now()
date_time = now.strftime("%Y/%m/%d  %H:%M:%S")

window = Tk()

database_csv = "Database.csv"

Barcode_Dictionary = pd.read_csv(database_csv, index_col=0).T.to_dict(orient="list")

item_index = 1.0

invoice_pdf = "Invoices\\Invoice_" + now.strftime("%Y%m%d_%H%M%S") + ".pdf"

order_history_csv = "History.csv"


def order_to_csv():
    user = {
        "INVOICE DATE AND TIME": [invoice_date.get()],
        "PATIENT NAME": [patient_name.get()],
        "PATIENT PHONE NUMBER": [patient_phone_number.get()],
        "PATIENT ADDRESS": [patient_address.get()],
        "DOCTOR NAME": [doctor_name.get()],
    }
    order_history_df = pd.DataFrame()
    if not os.path.exists(order_history_csv):
        order_history_df.to_csv(order_history_csv)
    order_history_df = pd.read_csv(order_history_csv, index_col=0)
    # order_history_df.at[order_history_df.index[-1], "INVOICE NUMBER"] = (
    #     invoice_number.get()
    # )
    # order_history_df.at[order_history_df.index[-1], "INVOICE DATE AND TIME"] = (
    #     invoice_date.get()
    # )
    # order_history_df.at[order_history_df.index[-1], "PATIENT NAME"] = patient_name.get()
    # order_history_df.at[order_history_df.index[-1], "PATIENT PHONE NUMBER"] = (
    #     patient_phone_number.get()
    # )
    # order_history_df.at[order_history_df.index[-1], "PATIENT ADDRESS"] = (
    #     patient_address.get()
    # )
    # order_history_df.at[order_history_df.index[-1], "DOCTOR NAME"] = doctor_name.get()
    current_order_df = pd.DataFrame(user)
    order_history_df.index += 1
    # print(order_history_df)
    # print(order_history_df.index[-1])
    order_history_df = pd.concat(
        [order_history_df, current_order_df], ignore_index=True, axis=0
    )
    order_history_df.to_csv(order_history_csv)
    global item_index
    for counter in range(1, int(item_index)):
        line = float(counter)
        order_history_df.at[
            order_history_df.index[-1],
            str(item_name.get(line, line + 1.0).strip() + " Quantity"),
        ] = quantity.get(line, line + 1.0).strip()
        order_history_df.at[
            order_history_df.index[-1],
            str(item_name.get(line, line + 1.0).strip() + " Price"),
        ] = total_amt.get(line, line + 1.0).strip()
    order_history_df.to_csv(order_history_csv)


def graphs():
    plt.figure("Analysis")
    order_history_df = pd.read_csv(order_history_csv, index_col=0)
    end_col = list(order_history_df.columns).index(order_history_df.columns[-1]) + 1

    plt.subplot(121)  # Quantity
    labels = []
    plt_quantity = []
    for col in range(5, end_col, 2):
        labels.append(order_history_df.columns[col])
        index = int((col - 5) / 2)
        plt_quantity.append(order_history_df[labels[index]].sum())
        labels[index] = labels[index][:-9]
    # explode = [0, 0, 0, 0.05, 0]
    # plt.pie(values, labels=labels, autopct="%.1f%%", explode=explode)
    plt.pie(plt_quantity, labels=labels, autopct="%.1f%%")
    plt.title("Quantity")
    plt.subplot(122)  # Price
    labels = []
    plt_price = []
    for col in range(6, end_col, 2):
        labels.append(order_history_df.columns[col])
        index = int((col - 5) / 2)
        plt_price.append(order_history_df[labels[index]].sum())
        labels[index] = labels[index][:-6]
    # explode = [0, 0, 0, 0.05, 0]
    # plt.pie(values, labels=labels, autopct="%.1f%%", explode=explode)
    plt.pie(plt_price, labels=labels, autopct="%.1f%%")
    plt.title("Price")
    plt.show()

    plt.figure("Analysis")
    position = range(0, len(labels))
    plt.bar(position, plt_quantity)
    plt.xticks(position, labels)
    plt.tick_params(labelrotation=30)
    plt.title("Quantity")
    plt.show()

    plt.figure("Analysis")
    position = range(0, len(labels))
    plt.bar(position, plt_price)
    plt.xticks(position, labels)
    plt.tick_params(labelrotation=30)
    plt.title("Price")
    plt.show()


def str_round(string):
    round_figure = round(float(string), 2)
    if int(round_figure * 10) == (round_figure * 10):
        return str(round_figure) + "0"
    else:
        return str(round_figure)


def scan_item():
    global item_index
    code = Barcode.capture()
    if code in Barcode_Dictionary.keys():
        name = Barcode_Dictionary[code][0]
        price = Barcode_Dictionary[code][1]
        for counter in range(0, int(item_index)):
            line = float(counter) + 1
            if name == item_name.get(line, line + 1.0).strip():
                break
        if name == item_name.get(line, line + 1.0).strip():
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
    global item_index

    item_index = 1.0

    invoice_number.delete(0, END)
    invoice_date.delete(0, END)
    invoice_date.insert(0, date_time)
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
    invoice_item_table = [
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
    for counter in range(1, int(item_index)):
        line = str(float(counter))
        invoice_item_table.append(
            [
                item_number.get(line, line + " lineend"),
                item_name.get(line, line + " lineend"),
                mrp.get(line, line + " lineend"),
                quantity.get(line, line + " lineend"),
                rate.get(line, line + " lineend"),
                total.get(line, line + " lineend"),
                disc_amt.get(line, line + " lineend"),
                taxable_amt.get(line, line + " lineend"),
                c_gst.get(line, line + " lineend"),
                s_gst.get(line, line + " lineend"),
                total_amt.get(line, line + " lineend"),
            ]
        )
    invoice_item_table.append(
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
    pdf = SimpleDocTemplate(invoice_pdf, pagesize=A4)
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    # 0: left, 1: center, 2: right
    title_style.alignment = 1
    title = Paragraph("Invoice", title_style)
    style = TableStyle(
        [
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]
    )
    customer_details = [
        ["Invoice", invoice_number.get()],
        ["Date", date_time],
        ["Patient"],
        ["Name", patient_name.get()],
        ["Contact", patient_phone_number.get()],
        ["Address", patient_address.get()],
        ["Doctor Name", doctor_name.get()],
    ]
    customer = Table(customer_details, style=style)
    table = Table(invoice_item_table, style=style)
    # pdf.build(
    #     [
    #         title,
    #         customer,
    #         "",
    #         table,
    #         "",
    #         "Discount : " + str(discount_percent.get(1.0, END)),
    #         "",
    #         "Net Payable : " + str(sum_total_amt.get(1.0, END)),
    #     ]
    # )
    pdf.build([title, customer, table])


def print_bill():
    order_to_csv()
    invoice()
    clear()
    os.startfile(invoice_pdf)


def exit_function():
    window.destroy()
    """
    if exit_window:
        exit_window.destroy()
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
# Label(window, text="Patient ID").grid(row=2, column=0, sticky="e")
Label(window, text="Patient Name").grid(row=3, column=0, sticky="e")
Label(window, text="Patient Contact").grid(row=4, column=0, sticky="e")
Label(window, text="Patient Address").grid(row=5, column=0, sticky="e")
Label(window, text="Doctor Name").grid(row=6, column=0, sticky="e")

invoice_number = Entry(window, width=25)
invoice_number.grid(row=0, column=1, sticky="w")

# invoice_date = Label(window, text=date_time)
invoice_date = Entry(window, width=25)
invoice_date.grid(row=1, column=1, sticky="w")
invoice_date.insert(0, date_time)

patient_name = Entry(window, width=25)
patient_name.grid(row=3, column=1, sticky="w")

patient_phone_number = Entry(window, width=25)
patient_phone_number.grid(row=4, column=1, sticky="w")

patient_address = Entry(window, width=25)
patient_address.grid(row=5, column=1, sticky="w")

doctor_name = Entry(window, width=25)
doctor_name.grid(row=6, column=1, sticky="w")

scan_button = Button(
    window, text="Database", command=lambda: os.startfile(database_csv)
)
scan_button.grid(row=8, column=0)

scan_button = Button(window, text="Scan", command=scan_item)
scan_button.grid(row=8, column=1)

clear_button = Button(window, text="Clear", command=clear)
clear_button.grid(row=8, column=2)

print_button = Button(window, text="Print", command=print_bill)
print_button.grid(row=8, column=3)

history_button = Button(
    window, text="History", command=lambda: os.startfile(order_history_csv)
)
history_button.grid(row=8, column=4)

analysis_button = Button(window, text="Analysis", command=graphs)
analysis_button.grid(row=8, column=5)

exit_button = Button(window, text="Exit", command=exit_function)
exit_button.grid(row=8, column=6)

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
