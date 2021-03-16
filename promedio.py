import psycopg2 as ps
from datetime import datetime
from math import pi,sqrt,trunc
print("Promedio")
salir = False

def txt_w(resultado):
        try:
            with open('promedio.txt','a',newline='',encoding = 'utf-8') as file:
                file.write(resultado+"\n")
        except Exception as exc0:
            print(str(exc0) + "\n No se puede leer el archivo .txt")

def postgres_insert(nota1,nota2,nota3,promedio,calific):
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO public.promedio(no_transaccion,fecha,nota1,nota2,nota3,promedio,calificacion)
        VALUES(nextval('pk_promedio'),%(fecha)s,%(no1)s,%(no2)s,%(no3)s,%(prom)s,%(calf)s)""",{'fecha':datetime.now(),'no1':nota1,'no2':nota2,'no3':nota3,'prom':promedio,'calf':calific})
        conexion.commit()
        cursor.close()
    except (Exception,ps.DatabaseError) as exc:
        print(exc)
        print("Conexion con base de datos fallida")
    finally:
        if conexion is not None:
            conexion.close()

def postgres_select():
    selectquery="""SELECT * FROM public.promedio ORDER BY no_transaccion ASC"""
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
            print("Nota 1:             ",fila[2])
            print("Nota 2:             ",fila[3])
            print("Nota 3:             ",fila[4])
            print("Promedio:           ",fila[5])
            print("Aprobado/Reprobado: ",fila[6])
            print("")
        cursor.close()
    except (Exception, ps.Error) as error:
        print("Error al obtener datos ", error)
    finally:
        if(conexion is not None):
            conexion.close()

def promedio(not1,not2,not3):
    promedio=(not1+not2+not3)*(1/3)
    calificacion=None
    if(promedio<60 and promedio>=0):
        calificacion="Reprobado"
        return promedio,calificacion
    elif(promedio>=60 and promedio<=100):
        calificacion="Aprobado"
        return promedio,calificacion
    else:
        print("Notas fuera de rango, revisar notas!!!!")
        return None,None

while(salir!=True):
    try:
        opc=str(input("¿Calcular promedio (s/n), mostrar registro (r)?\n ->"))
        if(opc.lower()=="s"):
            prom=0
            calificacion=""
            nota1=float(input("Ingresar nota 1: \n\t->"))
            nota2=float(input("Ingresar nota 2: \n\t->"))
            nota3=float(input("Ingresar nota 3: \n\t->"))
            if(nota2>=0 and nota1>=0 and nota3>=0):
                prom,calificacion=promedio(nota1,nota2,nota3)
                if(type(prom)!=type(None)):
                    print("\t"+str(datetime.now()))
                    print("\t El promedio de las notas es: {0:.2f}".format(prom)+ " ->"+calificacion) 
                    txt_w(str(datetime.now())+"\nEl promedio de las notas es: {0:.2f}".format(prom)+ " ->"+calificacion)
                    prom2=float("{0:.2f}".format(prom))
                    postgres_insert(nota1,nota2,nota3,prom2,calificacion)
        elif(opc.lower()=="r"):
            postgres_select()
        elif(opc.lower()=="n"):
            salir=True
        else:
            print("Opcion invalida elige otra!!!")
    except Exception as exc:
        print(str(exc)+"\n Algo va mal")