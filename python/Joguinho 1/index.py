
from PIL import Image

# Carrega a imagem
image_path = "D:\python\Joguinho 1\pinto.png"
img = Image.open(image_path)



a = 1




while a != (000):
    
    a = int(input("Escreva um numero par: "))
  
        


    if a%2 == 0 :
    
        print("Isso e um par!!!!!")
    
    else:

    
        print("lixo")
        img.show()



    