import qrcode

data = "Bond Global Energy Projects Limited\n\n" \
      "Phone number: 01-2931149\n" \
      "Address: 93b Ilupeju Street, Dolphin Estate, Ikoyi, Lagos\n" \
      "Mail: lubricants@bondenergyltd.com\n" \
      "Website: www.bondenergyltd.com\n" \

img = qrcode.make(data)
img.save("dynamic_qr.png")