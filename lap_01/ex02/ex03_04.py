def truycapphantu(tuple_data):
    first_elemant = tuple_data[0]
    last_elemant = tuple_data[-1]
    return first_elemant, last_elemant
input_tuple = eval(input("Nhap tuple, vi du(1,2,3):"))
first , last = truycapphantu(input_tuple)
print("Phan tu dau tien:", first)
print("Phan tu cuoi cung:", last)