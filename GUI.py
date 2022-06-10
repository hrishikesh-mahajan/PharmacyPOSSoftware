from tkinter import END, Button, Entry, Label, Text, Tk

import Barcode
import Dictionary

window = Tk()

item_index = "1.0"


def reset():
    invoice_number.delete(0, END)
    invoice_date.delete(0, END)
    patient_id.delete(0, END)
    patient_name.delete(0, END)
    patient_phone_number.delete(0, END)
    patient_address.delete(0, END)
    doctor_name.delete(0, END)


def scan_item():
    global item_index
    code = Barcode.capture()
    name = Dictionary.Barcode_Dictionary[code][0]
    price = Dictionary.Barcode_Dictionary[code][1]
    if code in Dictionary.Barcode_Dictionary.keys():
        item_number.insert(END, str(item_index)[:-1] + "\n")
        item_name.insert(END, name + "\n")
        mrp.insert(END, str(price) + "\n")
        quantity.insert(END, "1" + "\n")
        rate.insert(END, str(round(price / 1.12, 2)) + "\n")
        total.insert(END, str(float(rate.get(END)) * float(quantity.get(END))) + "\n")
        disc_amt.insert(END, str(round(float(total.get(END)) / 1.12, 2)) + "\n")
        taxable_amt.insert(
            END, str(round(price / 1.12, 2) * float(quantity.get(END))) + "\n"
        )
        c_gst.insert(END, str(round(float(taxable_amt.get(END)) * 0.06, 2)) + "\n")
        s_gst.insert(END, str(round(float(taxable_amt.get(END)) * 0.06, 2)) + "\n")
        total_amt.insert(
            END,
            str(
                round(
                    float(taxable_amt.get(END))
                    + float(taxable_amt.get(END))
                    + float(taxable_amt.get(END)),
                    2,
                )
            )
            + "\n",
        )
        item_index = str(float(item_index) + 1)


def exit_function():
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


window.geometry("1000x400")
window.title("Medical Billing Software")

label_invoice_number = Label(window, text="Invoice No. :")
label_invoice_number.grid(row=0, column=0, sticky="e")

invoice_number = Entry(window, width=25)
invoice_number.grid(row=0, column=1, padx=20, sticky="e")

label_invoice_date = Label(window, text="Invoice Date :")
label_invoice_date.grid(row=1, column=0, sticky="e")

invoice_date = Entry(window, width=25)
invoice_date.grid(row=1, column=1, padx=20, sticky="e")

label_patient_id = Label(window, text="Patient ID :")
label_patient_id.grid(row=2, column=0, sticky="e")

patient_id = Entry(window, width=25)
patient_id.grid(row=2, column=1, padx=20, sticky="e")

label_patient_name = Label(window, text="Patient Name :")
label_patient_name.grid(row=3, column=0, sticky="e")

patient_name = Entry(window, width=25)
patient_name.grid(row=3, column=1, padx=20, sticky="e")

label_patient_phone_number = Label(window, text="Patient Contact :")
label_patient_phone_number.grid(row=4, column=0, sticky="e")

patient_phone_number = Entry(window, width=25)
patient_phone_number.grid(row=4, column=1, padx=20, sticky="e")

label_patient_address = Label(window, text="Patient Address :")
label_patient_address.grid(row=5, column=0, sticky="e")

patient_address = Entry(window, width=25)
patient_address.grid(row=5, column=1, padx=20, sticky="e")

label_doctor_name = Label(window, text="Doctor Name :")
label_doctor_name.grid(row=6, column=0, sticky="e")

doctor_name = Entry(window, width=25)
doctor_name.grid(row=6, column=1, padx=20, sticky="e")

reset_button = Button(window, text="Reset", command=reset)
reset_button.grid(row=8, column=0, pady=10)

scan_button = Button(window, text="Scan", command=scan_item)
scan_button.grid(row=8, column=1, pady=10)

exit_button = Button(window, text="Exit", command=exit_function)
exit_button.grid(row=8, column=2, pady=10)

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
item_number.grid(row=10, column=0, padx=10)

item_name = Text(window, height=10, width=25)
item_name.grid(row=10, column=1, padx=10)

mrp = Text(window, height=10, width=6)
mrp.grid(row=10, column=2, padx=10)

quantity = Text(window, height=10, width=3)
quantity.grid(row=10, column=3, padx=10)

rate = Text(window, height=10, width=6)
rate.grid(row=10, column=4, padx=10)

total = Text(window, height=10, width=6)
total.grid(row=10, column=5, padx=10)

disc_amt = Text(window, height=10, width=6)
disc_amt.grid(row=10, column=6, padx=10)

taxable_amt = Text(window, height=10, width=7)
taxable_amt.grid(row=10, column=7, padx=10)

c_gst = Text(window, height=10, width=6)
c_gst.grid(row=10, column=8, padx=10)

s_gst = Text(window, height=10, width=6)
s_gst.grid(row=10, column=9, padx=10)

total_amt = Text(window, height=10, width=7)
total_amt.grid(row=10, column=10, padx=10)

window.mainloop()
