import psycopg2 as ps
from math import factorial
from datetime import datetime
salir = False

def txt_w(resultado):
        try:
            with open('factorial_7.txt','a',newline='',encoding = 'utf-8') as file:
                file.write(resultado+"\n")
        except Exception as exc0:
            print(str(exc0) + "\n No se puede leer el archivo .txt")

def postgres_insert(num1,factorial):
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO public.factorial7(no_transaccion,fecha,numero,fact)
        VALUES(nextval('pk_factorial7'),%(date)s,%(numero)s,%(fact)s);""",{'date':datetime.now(),'numero':num1,'fact':factorial})
        conexion.commit()
        cursor.close()
    except (Exception,ps.DatabaseError) as exc:
        print(exc)
        print("Conexion con base de datos fallida")
    finally:
        if conexion is not None:
            conexion.close()

def postgres_select():
    selectquery="""SELECT * FROM public.factorial7 ORDER BY no_transaccion ASC """
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute(selectquery)
        datos=cursor.fetchall()
        print("Registro de datos del programa:\n")
        for fila in datos:
            print("No_transacción: ",fila[0])
            print("Fecha: ",fila[1])
            print("Número= ",fila[2])
            print("Factorial= ",fila[3])
            print(" ")
        cursor.close()
    except (Exception, ps.Error) as error:
        print("Error al obtener datos ", error)
    finally:
        if(conexion is not None):
            conexion.close()

while(salir!=True):
    try:
        opc=str(input("¿Factorial (s/n), mostrar registro (r)?\n ->"))
        if(opc.lower()=="s"):
            numfact7=int(input("\tIngresa el número.\n\t->"))
            if(numfact7>0 and numfact7%7==0):
                print("\t"+str(datetime.now()))
                print("\tEl factorial del número "+str(numfact7)+" es:" +str(factorial(numfact7)))
                txt_w("\t"+str(datetime.now())+"\n\tEl factorial del número "+str(numfact7)+" es:" +str(factorial(numfact7)))
                postgres_insert(numfact7,factorial(numfact7))
            else:
                print("El número no es divisible dentro de 7 o es negativo ingresa otro número!!!!")
        elif(opc.lower()=="r"):
            postgres_select()
        elif(opc.lower()=="n"):
            salir=True
        else:
            print("Opcion invalida elige otra!!!")
    except Exception as exc:
        print(str(exc)+"\n Algo va mal")