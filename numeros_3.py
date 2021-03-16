import psycopg2 as ps

print("Juego de numeros")
salir=False

def in_num():
    try:
        primero=float(input("Ingrese el primer número: "))
        segundo=float(input("Ingrese el segundo número: "))
        tercero=float(input("Ingrese el tercer número: "))
        return primero,segundo,tercero
    except Exception as exc:
        print("%s",exc)
        print("La has cantado carnal")

def txt_w(resultado):
        try:
            with open('numeros_3.txt','a',newline='',encoding = 'utf-8') as file:
                file.write("* "+resultado+"\n")
        except Exception as exc0:
            print(str(exc0) + "\n No se puede leer el archivo .csv")

def postgres_insert(num1,num2,num3,operacion,resultado,resultado_2):
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO public.numeros_3(no_transaccion,numero_1,numero_2,numero_3,operacion,resultado,resultado_2)
        VALUES(nextval('pk_numeros3'),%s,%s,%s,%s,%s,%s)""",(num1,num2,num3,operacion,resultado,resultado_2))
        conexion.commit()
        cursor.close()
    except (Exception,ps.DatabaseError) as exc:
        print(exc)
        print("Conexcion con base de datos fallida")
    finally:
        if conexion is not None:
            conexion.close()

def suma(pri,sec,tri):
    return pri+sec+tri
def multiplicacion(pri,sec,tri):
    return pri*sec*tri
def concatenacion(pri,sec,tri):
    strTotal=str(pri)+str(sec)+str(tri)
    return strTotal
def opc():
    try:
        opc=str(input("Desea seguir jugnado o no? S/N"))
        return opc
    except Exception as ex:
        print(str(ex))
        print("Formato no valido")
    

while(salir!=True):
    print("¿Ingresar numeros s/n?")    
    try:
        in_opc=str(input("-> "))
        if(in_opc.lower()=="s"):
            salir=False
            resultado3operaciones=None
            primero,segundo,tercero=in_num()
            if(primero==segundo==tercero):
                print("-->Todos son iguales")
                txt_w("Todos son iguales")
                postgres_insert(primero,segundo,tercero,'comparacion',str(primero),None)
            elif(primero==segundo):
                print("-->El tercer número es el diferente: "+str(tercero))
                txt_w("El tercer número es el diferente: "+str(tercero))
                postgres_insert(primero,segundo,tercero,'comparacion',str(tercero),None)
            elif(primero==tercero):
                print("-->El segundo número es el diferente: "+str(segundo))
                txt_w("El segundo número es el diferente: "+str(segundo))
                postgres_insert(primero,segundo,tercero,'comparacion',str(segundo),None)
            elif(tercero==segundo):
                print("-->El primer número es el diferente: "+str(primero))
                txt_w("El primer número es el diferente: "+str(primero))
                postgres_insert(primero,segundo,tercero,'comparacion',str(primero),None)
            elif(primero>segundo and primero>tercero):
                resultado3operaciones=suma(primero,segundo,tercero)
                print("-->El primero es el más grande la suma es: "+ str(resultado3operaciones))
                txt_w("El primero es el más grande la suma es: "+ str(resultado3operaciones))
                postgres_insert(primero,segundo,tercero,'suma',str(resultado3operaciones),None)
            elif(segundo>primero and segundo>tercero):
                resultado3operaciones=multiplicacion(primero,segundo,tercero)
                print("-->El segundo es el más grande la multiplicación es: "+ str(resultado3operaciones))
                txt_w("El segundo es el más grande la multiplicación es: "+ str(resultado3operaciones))
                postgres_insert(primero,segundo,tercero,'multiplicacion',str(resultado3operaciones),None)
            elif(tercero>primero and tercero>segundo):
                resultado3operaciones=concatenacion(primero,segundo,tercero)
                print("-->El tercero es el más grande la concatenación es: "+ resultado3operaciones)
                txt_w("El tercero es el más grande la concatenación es: "+ resultado3operaciones)
                postgres_insert(primero,segundo,tercero,'concatenacion',None,resultado3operaciones)                
            else:
                print("Rompiste el universo")
        elif(in_opc.lower()=="n"):
            salir=True
        else:
            print("Opción no valida prueba ingresar otra opción......")
    except Exception as exc:
        print("%s\nAlgo va mal!!!!",exc)