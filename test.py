import ocr

ingredient_list = ocr.read_label("Images/HoneyNutCheerios.jpg")
print(ingredient_list)