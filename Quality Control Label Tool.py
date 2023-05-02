import os
import datetime
from datetime import datetime
import time
import sys
from PIL import Image
import zpl
from zebra import Zebra
# Import writer class from csv module
from csv import writer

# Create File
try:
    if not os.path.exists(fr'QC_Data.csv'):
        print("No File found...attempting to create 'QC_Data.csv'\n")
        header = ['Barcode', 'Date', 'Time', 'Location']
        with open(fr'QC_Data.csv', 'w', newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(header)
            f_object.close()
except Exception as ex:
    print(ex)
    print("\n FATAL ERROR: Please Notify Your Nearest Shift Manager")
    for i in range(10,0,-1):
        sys.stdout.write(str('.')+' ')
        sys.stdout.flush()
        time.sleep(1)
    quit()

print("""
     -----------------------------------------------------
    |           QUALITY CONTROL LABELLING                 |      
    |                                                     |
    |           AND INVENTORY TRACKING TOOL               |
     -----------------------------------------------------
""")
location = input("\nEnter your location: ")
#location = ('Midlands Super Hub')
check = []
rule = True
while True:
    barcode = input("\n Scan a Product Barcode: ")
    check.append(barcode)
    if len(check) == 2:
        if check[0] == check[1]:
            rule = False
            check.clear()
    
    
    print("\n Printing Label...")
    print("\n Uploading to CSV File...")
    
    now = datetime.now()

    t = now.strftime("%H:%M:%S")
 
    d = now.strftime("%d/%m/%Y")
  
    # List that we want to add as a new row
    Header = ['barcode', 'Date', 'Time' ,'Location']
    List = [barcode, d, t, location]
 
    # Open our existing CSV file in append mode
    # Create a file object for this file
    if rule == True:
        try:
            with open(fr'QC_Data.csv', 'a', newline='') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(List)
                f_object.close()
            
        except Exception as ex:
            print(ex)
            print("\n FATAL ERROR: Please Notify Your Nearest Shift Manager")
            for i in range(10,0,-1):
                sys.stdout.write(str('.')+' ')
                sys.stdout.flush()
                time.sleep(1)
            quit()
    else:
        print("Barcode already scanned!")
        rule = True

    z = Zebra()
    Q = z.getqueues()
    z.setqueue(Q[0])
    z.setup()
    z.output(f"""^XA
^FX Top section with logo, name and address.
^CF0,60

^FO120,50^FDQuality Checked^FS
^CF0,40
^FO40,115^FDDate: {d}^FS
^FO40,155^FDLocation: {location}^FS

^FX Third section with bar code.
^BY3,2,140
^FO40,210^BC^FD{barcode}^FS
^XZ""")
    