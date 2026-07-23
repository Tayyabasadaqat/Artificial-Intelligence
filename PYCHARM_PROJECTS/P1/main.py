import tools
# AREA CALCULATOR TOOL
print("Welcome to the Area Calculator Tool")
while(True):
    choice=input("To find area of circle press C\n To find area of rectangle press R\n To find area of square press S\n To find area of triangle press T\n To exit press Q\n")
    if choice =='Q' or choice =='q':
        break
    if choice =='C' or choice =='c':
        radius=float(input("Enter the radius of the circle: "))
        tools.calculate_area_circle(radius)
    elif choice =='R' or choice =='r':
        length=float(input("Enter the length of the rectangle: "))
        width =float(input("Enter the width of the rectangle: "))
        tools.calculate_area_rectangle(length,width)
    elif choice =='S' or choice =='s':
        length=float(input("Enter the length of the square: "))
        tools.calculate_area_square(length)
    elif choice =='T' or choice =='t':
        length=float(input("Enter the length of the triangle: "))
        height = float(input("Enter the height of the triangle: "))
        tools.calculate_area_triangle(length,height)
    else:
        print("Please enter a valid option")