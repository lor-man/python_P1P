import psycopg2 as ps
from datetime import datetime
salir = False

def txt_w(resultado):
        try:
            with open('100_pares.txt','a',newline='',encoding = 'utf-8') as file:
                file.write(resultado+"\n")
        except Exception as exc0:
            print(str(exc0) + "\n No se puede leer el archivo .txt")

def postgres_select():
    selectquery="""SELECT * FROM public."100_pares"ORDER BY no_transaccion ASC"""
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute(selectquery)
        datos=cursor.fetchall()
        print("Registro de datos del programa")
        for fila in datos:
            print("No_transacción: ",fila[0])
            print("Fecha y hora: ",fila[1])
        cursor.close()
    except (Exception, ps.Error) as error:
        print("Error al obtener datos ", error)
    finally:
        if(conexion is not None):
            conexion.close()
            
def postgres_insert():
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO public."100_pares"(no_transaccion, fecha)
        VALUES(nextval('pk_100_pares'),%(date)s);""",{'date':datetime.now()})
        conexion.commit()
        cursor.close()
    except (Exception,ps.DatabaseError) as exc:
        print(exc)
        print("Conexion con base de datos fallida")
    finally:
        if conexion is not None:
            conexion.close()

while(salir!=True):
    try:
        opc=str(input("¿Mostrar numeros pares (s/n), mostrar registro (r)?\n ->"))
        if(opc.lower()=="s"):
            a=[]
            cnt=0
            #a.append(cnt)
            while(cnt<100):
                cnt+=2
                a.append(cnt)
            print("\t"+str(datetime.now()))
            print("\tExisten "+str(len(a))+" numeros pares del 1 al 100 son:\n\t"+str(a))
            txt_w("\t"+str(datetime.now())+"\n\tExisten "+str(len(a))+" numeros pares del 1 al 100\n\tNúmeros pares:\n\t"+str(a))
            postgres_insert()
        elif(opc.lower()=="r"):
            postgres_select()
        elif(opc.lower()=="n"):
            salir=True
        else:
            print("Opcion invalida elige otra!!!")
    except Exception as exc:
        print(str(exc)+"\n Algo va mal")