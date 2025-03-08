def taotupletulist(lst):
    return tuple(lst)
input_list = input("Nhap danh sach cac so, cach nhau bang dau phay:")
numbers = list(map(int, input_list.split(',')))
mytuple = taotupletulist(numbers)
print("List:", numbers)
print("Tuple tu List:", mytuple) 