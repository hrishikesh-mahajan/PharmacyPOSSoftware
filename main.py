import cv2
from pyzbar.pyzbar import decode

from tkinter import *
from datetime import datetime

import matplotlib.pyplot as plt

import os
import pandas as pd

# Import modules from reportlab
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


date_time_format = "%Y/%m/%d  %H:%M:%S"

window = Tk()

database_csv = "Database.csv"

Barcode_Dictionary = pd.read_csv(database_csv, index_col=0).T.to_dict(orient='list')

item_index = 1.0

invoice_pdf = "Invoices\\Invoice_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".pdf"

order_history_csv = "History.csv"

image_path = "Product.png"

order_history_df = pd.DataFrame()
if not os.path.exists(order_history_csv):
    order_history_df.to_csv(order_history_csv)
order_history_df = pd.read_csv(order_history_csv, index_col=0)

if not os.path.isdir("Invoices"):
    os.mkdir("Invoices")


def barcode_reader(image):
    img = cv2.imread(str(image))
    os.remove(image)
    detected_barcodes = decode(img)
    if not detected_barcodes:
        return 0
    else:
        for barcode in detected_barcodes:
            if barcode.data != "":
                return int(barcode.data)


def capture():
    # 0 for native, 1 for DroidCam
    cam_port = 0
    cam = cv2.VideoCapture(cam_port, cv2.CAP_DSHOW)
    while True:
        result, captured_image = cam.read()
        cv2.imwrite(image_path, captured_image)
        cv2.imshow("Capture Barcode", captured_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        item = barcode_reader(image_path)
        if item:
            break
    cam.release()
    cv2.destroyAllWindows()
    return item


def order_to_csv():
    global order_history_df
    user = {'INVOICE DATE AND TIME': [invoice_date.cget("text")], 'PATIENT NAME': [patient_name.get()],
            'PATIENT PHONE NUMBER': [patient_phone_number.get()], 'PATIENT ADDRESS': [patient_address.get()],
            'DOCTOR NAME': [doctor_name.get()]}
    current_order_df = pd.DataFrame(user)
    order_history_df.index += 1
    order_history_df = pd.concat([order_history_df, current_order_df], ignore_index=True, axis=0)
    order_history_df.to_csv(order_history_csv)
    global item_index
    for counter in range(1, int(item_index)):
        line = float(counter)
        order_history_df.at[order_history_df.index[-1], str(item_name.get(line, line + 1.0).strip() + " Quantity")] \
            = quantity.get(line, line + 1.0).strip()
        order_history_df.at[order_history_df.index[-1], str(item_name.get(line, line + 1.0).strip() + " Price")] \
            = total_amt.get(line, line + 1.0).strip()
    order_history_df.to_csv(order_history_csv)


def graphs():
    plt.figure("Analysis", figsize=(14, 5))
    end_col = list(order_history_df.columns).index(order_history_df.columns[-1]) + 1

    plt.subplot(121)  # Quantity
    labels = []
    plt_quantity = []
    for col in range(5, end_col, 2):
        labels.append(order_history_df.columns[col])
        index = int((col-5)/2)
        plt_quantity.append(order_history_df[labels[index]].sum())
        labels[index] = labels[index][:-9]
    plt.pie(plt_quantity, labels=labels, autopct="%.1f%%")
    plt.title('Quantity')

    plt.subplot(122)  # Price
    labels = []
    plt_price = []
    for col in range(6, end_col, 2):
        labels.append(order_history_df.columns[col])
        index = int((col-5)/2)
        plt_price.append(order_history_df[labels[index]].sum())
        labels[index] = labels[index][:-6]
    plt.pie(plt_price, labels=labels, autopct="%.1f%%")
    plt.title('Price')
    plt.show()

    plt.figure("Analysis", figsize=(10, 6))
    position = range(0, len(labels))
    plt.bar(position, plt_quantity)
    plt.xticks(position, labels)
    plt.tick_params(labelrotation=30)
    for i in range(len(labels)):
        plt.text(i, plt_quantity[i] + 0.02 * (round(sum(plt_quantity) / len(plt_quantity), 2)), plt_quantity[i],
                 ha='center')
    plt.title('Quantity')
    plt.ylabel('Quantity')
    plt.xlabel('Items')
    plt.tight_layout()
    plt.show()

    plt.figure("Analysis", figsize=(10, 6))
    position = range(0, len(labels))
    plt.bar(position, plt_price)
    plt.xticks(position, labels)
    plt.tick_params(labelrotation=30)
    for i in range(len(labels)):
        plt.text(i, plt_price[i] + 0.02 * (round(sum(plt_price) / len(plt_price), 2)), plt_price[i], ha='center')
    plt.title('Price')
    plt.ylabel('Price')
    plt.xlabel('Items')
    plt.tight_layout()
    plt.show()


def str_round(string):
    round_figure = round(float(string), 2)
    if int(round_figure * 10) == (round_figure * 10):
        return str(round_figure) + '0'
    else:
        return str(round_figure)


def scan_item():
    global item_index
    code = capture()
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
    item_number.insert(INSERT, str(int(item_index)) + '.\n')
    item_name.insert(INSERT, name + '\n')
    mrp.insert(INSERT, str_round(price + 0.00) + '\n')
    quantity.insert(INSERT, '1' + '\n')
    rate.insert(INSERT, str_round(price / 1.12) + '\n')
    total.insert(INSERT, str_round(float(rate.get(item_index, "end-1c linestart")) *
                                   float(quantity.get(item_index, "end-1c linestart"))) + '\n')
    disc_amt.insert(INSERT, str_round(float(total.get(item_index, "end-1c linestart")) *
                                      float(discount_percent.get(1.0, END)) / 100) + '\n')
    taxable_amt.insert(INSERT, str_round(float(total.get(item_index, "end-1c linestart")) -
                                         float(disc_amt.get(item_index, "end-1c linestart"))) + '\n')
    c_gst.insert(INSERT, str_round(float(taxable_amt.get(item_index, "end-1c linestart")) * 0.06) + '\n')
    s_gst.insert(INSERT, str_round(float(taxable_amt.get(item_index, "end-1c linestart")) * 0.06) + '\n')
    total_amt.insert(INSERT, str_round(float(mrp.get(item_index, "end-1c linestart")) *
                                       float(quantity.get(item_index, "end-1c linestart")) *
                                       (1 - float(discount_percent.get(1.0, END)) / 100)) + '\n')
    item_index = item_index + 1


def old_item(line):
    current_quantity = int(quantity.get(line, line + 1.0))
    quantity.delete(line, line + 1.0)
    quantity.insert(line, str(current_quantity + 1) + '\n')
    total.delete(line, line + 1.0)
    total.insert(line, str_round(float(rate.get(line, line + 1.0)) * float(quantity.get(line, line + 1.0))) + '\n')
    disc_amt.delete(line, line + 1.0)
    disc_amt.insert(line, str_round(float(total.get(line, line + 1.0)) *
                                    float(discount_percent.get(1.0, END)) / 100) + '\n')
    taxable_amt.delete(line, line + 1.0)
    taxable_amt.insert(line, str_round(float(total.get(line, line + 1.0)) -
                                       float(disc_amt.get(line, line + 1.0))) + '\n')
    c_gst.delete(line, line + 1.0)
    c_gst.insert(line, str_round(float(taxable_amt.get(line, line + 1.0)) * 0.06) + '\n')
    s_gst.delete(line, line + 1.0)
    s_gst.insert(line, str_round(float(taxable_amt.get(line, line + 1.0)) * 0.06) + '\n')
    total_amt.delete(line, line + 1.0)
    total_amt.insert(line, str_round(float(mrp.get(line, line + 1.0)) * float(quantity.get(line, line + 1.0)) *
                                     (1 - float(discount_percent.get(1.0, END)) / 100)) + '\n')


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
    sum_column(total, sum_total)
    sum_column(disc_amt, sum_disc_amt)
    sum_column(taxable_amt, sum_taxable_amt)
    sum_column(c_gst, sum_c_gst)
    sum_column(s_gst, sum_s_gst)
    sum_column(total_amt, sum_total_amt)


def sum_column(data, result):
    count = 0.00
    for counter in range(1, int(item_index)):
        line = float(counter)
        count = count + float(data.get(line, line+1))
    result.delete("1.0", "end")
    result.insert(1.0, str_round(count))


def clear():
    global item_index

    item_index = 1.0

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
    invoice_item_table = [["Sr. No.", "Description of goods", "MRP", "Qty", "Rate", "Total", "Disc Amt", "Taxable Amt",
                           "CGST\n@6%", "SGST\n@6%", "Total Amt\n(inc. Tax)"]]
    for counter in range(1, int(item_index)):
        line = str(float(counter))
        invoice_item_table.append([item_number.get(line, line + ' lineend'), item_name.get(line, line + ' lineend'),
                                   mrp.get(line, line + ' lineend'), quantity.get(line, line + ' lineend'),
                                   rate.get(line, line + ' lineend'), total.get(line, line + ' lineend'),
                                   disc_amt.get(line, line + ' lineend'), taxable_amt.get(line, line + ' lineend'),
                                   c_gst.get(line, line + ' lineend'), s_gst.get(line, line + ' lineend'),
                                   total_amt.get(line, line + ' lineend')])
    invoice_item_table.append(["", "", "", "", "Total", sum_total.get(1.0, 1.99), sum_disc_amt.get(1.0, 1.99),
                               sum_taxable_amt.get(1.0, 1.99), sum_c_gst.get(1.0, 1.99), sum_s_gst.get(1.0, 1.99),
                               sum_total_amt.get(1.0, 1.99)])
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
    customer_details = [["Invoice", invoice_number.cget("text")], ["Date", invoice_date.cget("text")], ["Patient"],
                        ["Name", patient_name.get()], ["Contact", patient_phone_number.get()],
                        ["Address", patient_address.get()], ["Doctor Name", doctor_name.get()]]
    customer = Table(customer_details, style=style)
    table = Table(invoice_item_table, style=style)
    pdf.build([title, customer, table])


def print_bill():
    order_to_csv()
    invoice()
    clear()
    os.startfile(invoice_pdf)


def exit_function():
    exit_window = Tk()
    exit_window.geometry("200x120")
    exit_window.title("Exit")
    Label(exit_window, text="\n Are you Sure? \n").pack()
    Button(exit_window, text="Yes", command=lambda: [window.destroy(), exit_window.destroy()]).pack()
    Button(exit_window, text="No", command=exit_window.destroy).pack()
    exit_window.mainloop()


def about():
    about_window = Tk()
    about_window.geometry("250x180")
    about_window.title("About Us")
    Label(about_window, text="Medical Billing Software \n Build 2022-07-04 02:00:00 PM \n \n Developers: \n Hrishikesh Mahajan \n Aman Narnaware \n Vedant Kulkarni \n Vedant Kulkarni \n").pack()
    Button(about_window, text="Okay", command=about_window.destroy).pack()
    about_window.mainloop()


def time():
    now = datetime.now()
    date_time = now.strftime(date_time_format)
    invoice_date.config(text=date_time)
    invoice_date.after(1000, time)


window.title("Medical Billing Software")

Label(window, text="Invoice No.").grid(row=0, column=0, sticky='e')
Label(window, text="Invoice Date").grid(row=1, column=0, sticky='e')
Label(window, text="Patient Name").grid(row=3, column=0, sticky='e')
Label(window, text="Patient Contact").grid(row=4, column=0, sticky='e')
Label(window, text="Patient Address").grid(row=5, column=0, sticky='e')
Label(window, text="Doctor Name").grid(row=6, column=0, sticky='e')

invoice_number = Label(window)
invoice_number.config(text=(order_history_df.index[-1]+1))
invoice_number.grid(row=0, column=1, sticky='w')


invoice_date = Label(window)
invoice_date.grid(row=1, column=1, sticky='w')

patient_name = Entry(window, width=25)
patient_name.grid(row=3, column=1, sticky='w')

patient_phone_number = Entry(window, width=25)
patient_phone_number.grid(row=4, column=1, sticky='w')

patient_address = Entry(window, width=25)
patient_address.grid(row=5, column=1, sticky='w')

doctor_name = Entry(window, width=25)
doctor_name.grid(row=6, column=1, sticky='w')

scan_button = Button(window, text="Database", command=lambda: os.startfile(database_csv))
scan_button.grid(row=8, column=0)

scan_button = Button(window, text="Scan", command=scan_item)
scan_button.grid(row=8, column=1)

clear_button = Button(window, text="Clear", command=clear)
clear_button.grid(row=8, column=2)

print_button = Button(window, text="Print", command=print_bill)
print_button.grid(row=8, column=3)

history_button = Button(window, text="History", command=lambda: os.startfile(order_history_csv))
history_button.grid(row=8, column=4)

analysis_button = Button(window, text="Analysis", command=graphs)
analysis_button.grid(row=8, column=5)

exit_button = Button(window, text="About", command=about)
exit_button.grid(row=8, column=6)

exit_button = Button(window, text="Exit", command=exit_function)
exit_button.grid(row=8, column=7)

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
item_number.tag_configure("Right", justify='right')
item_number.grid(row=10, column=0)

item_name = Text(window, height=10, width=25)
item_name.grid(row=10, column=1)

mrp = Text(window, height=10, width=6)
mrp.tag_configure("Right", justify='right')
mrp.grid(row=10, column=2)

quantity = Text(window, height=10, width=3)
quantity.tag_configure("Right", justify='right')
quantity.grid(row=10, column=3)

rate = Text(window, height=10, width=6)
rate.tag_configure("Right", justify='right')
rate.grid(row=10, column=4)

total = Text(window, height=10, width=7)
total.tag_configure("Right", justify='right')
total.grid(row=10, column=5)

disc_amt = Text(window, height=10, width=6)
disc_amt.tag_configure("Right", justify='right')
disc_amt.grid(row=10, column=6)

taxable_amt = Text(window, height=10, width=7)
taxable_amt.tag_configure("Right", justify='right')
taxable_amt.grid(row=10, column=7)

c_gst = Text(window, height=10, width=6)
c_gst.tag_configure("Right", justify='right')
c_gst.grid(row=10, column=8)

s_gst = Text(window, height=10, width=6)
s_gst.tag_configure("Right", justify='right')
s_gst.grid(row=10, column=9)

total_amt = Text(window, height=10, width=7)
total_amt.tag_configure("Right", justify='right')
total_amt.grid(row=10, column=10)

Label(window, text="TOTAL").grid(row=11, column=4, sticky='e')

sum_total = Text(window, height=1, width=6)
sum_total.tag_configure("Right", justify='right')
sum_total.grid(row=11, column=5)

sum_disc_amt = Text(window, height=1, width=6)
sum_disc_amt.tag_configure("Right", justify='right')
sum_disc_amt.grid(row=11, column=6)

sum_taxable_amt = Text(window, height=1, width=7)
sum_taxable_amt.tag_configure("Right", justify='right')
sum_taxable_amt.grid(row=11, column=7)

sum_c_gst = Text(window, height=1, width=6)
sum_c_gst.tag_configure("Right", justify='right')
sum_c_gst.grid(row=11, column=8)

sum_s_gst = Text(window, height=1, width=6)
sum_s_gst.tag_configure("Right", justify='right')
sum_s_gst.grid(row=11, column=9)

sum_total_amt = Text(window, height=1, width=7)
sum_total_amt.tag_configure("Right", justify='right')
sum_total_amt.grid(row=11, column=10)


Label(window, text="Discount %").grid(row=11, column=0)
discount_percent = Text(window, height=1, width=6)
discount_percent.grid(row=11, column=1)
discount_percent.insert(1.0, "0.00")

time()

window.mainloop()
