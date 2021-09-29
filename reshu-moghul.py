import pandas as pd
from fpdf import FPDF

df = pd.read_csv("test.csv")
series_uniqueOrderID = df["Order ID"].unique() #output: [1004,1005,1006]

# create FPDF object
# Layout ('P', 'L') -- portrait or landscape
# Unit ('mm','cm','in') -- mm or cm or inches
# format ('A3','A4'(default),'A5','Letter','Legal',(100,150))
pdf = FPDF('P')

def concatenateAddress(address1, address2, postalcode):
	if (pd.isna(address2)):
		address1 = str(address1) 
		return address1 + " " + postalcode
	else: 
		address1 = str(address1)
		address2 = str(address2)
		return address1 + " " + address2 + " " + postalcode

for orderID in series_uniqueOrderID:
	name = ""
	contact_number = ""
	shipping_address = ""
	delivery_datetime = ""
	order_items = {}

	df_orderID = df[df["Order ID"] == orderID]

	name = df_orderID["Full Name"].tolist()[0]
	contact_number = df_orderID["Contact"].tolist()[0]
	shipping_address = concatenateAddress(df_orderID["Shipping Address Line 1"].tolist()[0], df_orderID["Shipping Address Line 2"].tolist()[0], str(df_orderID["Postal Code"].tolist()[0]))
	delivery_datetime = df_orderID["Delivery Date"].tolist()[0]

	for i in range(len(df_orderID["SKU"].tolist())):
		order_items[df_orderID["SKU"].tolist()[i]] = df_orderID["Quantity"].tolist()[i]
	
	# Create a PDF page
	pdf.add_page()
	pdf.image(name= 'logo.jpeg',x=10, y=10,w=30,h=30, type='jpeg')
	pdf.set_font("Arial", size = 12) #fonts: 'times', 'arial', 'helvetica', 'courier'
	
	# Output shipping info
	x_position = 42
	pdf.set_xy(x= x_position, y=12)
	pdf.cell(200, 7, txt = "Order ID: " + str(orderID), ln = 1, align = 'L')
	pdf.set_x(x= x_position)
	pdf.cell(200, 7, txt = "Name: " + name + ", Contact: " + contact_number, ln = 1, align = 'L')
	pdf.set_x(x= x_position)
	pdf.cell(200, 7, txt = "Address: " + shipping_address, ln = 1, align = 'L')
	pdf.set_x(x= x_position)
	pdf.cell(200, 7, txt = "Delivery DateTime: " + delivery_datetime, ln = 1, align = 'L')

	# Output item and quantity
	pdf.set_font("Arial", size = 15, style='B')
	width_cell = 95
	height_cell = 10
	pdf.set_xy(x= 10, y = 45)
	
	if len(order_items.items()) > 20:
		pdf.set_font("Arial", size = 15, style='B')
		pdf.set_xy(x=0, y=150)
		pdf.set_text_color(r=255,g=0,b=0)
		pdf.cell(210,10, txt="Number of orders exceeded 20. Proceed to make order slip manually.", align = 'C')
		pdf.set_text_color(r=0,g=0,b=0)
		
	else: 
		pdf.cell(width_cell, height_cell, txt = "ITEM ID", ln = 0, align = 'L', border=1)
		pdf.cell(width_cell, height_cell, txt = "QUANTITY", ln = 1, align = 'R', border=1)
		pdf.set_font("Arial", size = 15) #fonts: 'times', 'arial', 'helvetica', 'courier'
		for sku, qty in order_items.items():
			pdf.cell(width_cell, height_cell, txt = sku, ln = 0, align = 'L', border=1)
			pdf.cell(width_cell, height_cell, txt = str(qty), ln = 1, align = 'R', border=1)
	
	pdf.set_xy(x= 0, y = 260)
	pdf.cell(210, 10, txt = "www.moghulsweets.com", ln = 1, align = 'C')
print("PDF is generated successfully. Total pages: " + str(pdf.page_no()))
pdf.output("output.pdf")