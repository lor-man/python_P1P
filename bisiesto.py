import psycopg2 as ps
from datetime import datetime
from calendar import isleap
print("Bisiesto")
salir = False

def txt_w(resultado):
        try:
            with open('bisiesto.txt','a',newline='',encoding = 'utf-8') as file:
                file.write(resultado+"\n")
        except Exception as exc0:
            print(str(exc0) + "\n No se puede leer el archivo .txt")

def postgres_insert(yr,tipo):
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO public.bisiesto(no_transaccion,fecha,"año",tipo)
        VALUES(nextval('pk_bisiesto'),%(fecha)s,%(yr1)s,%(tip)s)""",{'fecha':datetime.now(),'yr1':yr,'tip':tipo})
        conexion.commit()
        cursor.close()
    except (Exception,ps.DatabaseError) as exc:
        print(exc)
        print("Conexion con base de datos fallida")
    finally:
        if conexion is not None:
            conexion.close()

def postgres_select():
    selectquery="""SELECT * FROM public.bisiesto ORDER BY no_transaccion ASC"""
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute(selectquery)
        datos=cursor.fetchall()
        print("Registro de datos del programa")
        for fila in datos:
            print("No_transacción:     ",fila[0])
            print("Fecha y hora:       ",fila[1])
            print("Año:             ",fila[2])
            print("Tipo:             ",fila[3])
            print("")
        cursor.close()
    except (Exception, ps.Error) as error:
        print("Error al obtener datos ", error)
    finally:
        if(conexion is not None):
            conexion.close()

while(salir!=True):
    try:
        opc=str(input("¿Ver año (s/n), mostrar registro (r)?\n ->"))
        if(opc.lower()=="s"):
            yr=int(input("\tIngresa el año de nacimiento\n\t->"))
            print("\t"+str(datetime.now()))
            if(isleap(yr)):
                print("\tEl año de nacimiento "+str(yr)+" fue bisiesto")
                txt_w(str(datetime.now())+"\nEl año de nacimiento "+str(yr)+" fue bisiesto")
                postgres_insert(yr,"Bisiesto")
            elif(isleap(yr)==False):
                print("\tEl año de nacimiento "+str(yr)+" no fue bisiesto")
                txt_w(str(datetime.now())+"\nEl año de nacimiento "+str(yr)+" no fue bisiesto")   
                postgres_insert(yr,"No bisiesto")       
        elif(opc.lower()=="r"):
            postgres_select()
        elif(opc.lower()=="n"):
            salir=True
        else:
            print("Opcion invalida elige otra!!!")
    except Exception as exc:
        print(str(exc)+"\n Algo va mal")