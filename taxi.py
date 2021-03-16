import psycopg2 as ps
from datetime import datetime
from calendar import isleap
print("Flota de taxis")
salir = False

def txt_w(resultado):
        try:
            with open('taxis.txt','a',newline='',encoding = 'utf-8') as file:
                file.write(resultado+"\n")
        except Exception as exc0:
            print(str(exc0) + "\n No se puede leer el archivo .txt")

def postgres_insert(yr,kilometraje,con):
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO public.taxi(no_transaccion,fecha,yr,kilometraje,condicion)
        VALUES(nextval('pk_taxi'),%(fecha)s,%(yr1)s,%(kilo)s,%(cond)s)""",{'fecha':datetime.now(),'yr1':yr,'kilo':kilometraje,'cond':con})
        conexion.commit()
        cursor.close()
    except (Exception,ps.DatabaseError) as exc:
        print(exc)
        print("Conexion con base de datos fallida")
    finally:
        if conexion is not None:
            conexion.close()

def postgres_select():
    selectquery="""SELECT * FROM public.taxi ORDER BY no_transaccion ASC"""
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute(selectquery)
        datos=cursor.fetchall()
        print("Registro de datos del programa")
        for fila in datos:
            print("No_transacción:",fila[0])
            print("Fecha y hora:  ",fila[1])
            print("Año:           ",fila[2])
            print("Kilometraje:   ",fila[3])
            print("Condición:     ",fila[4])
            print("")
        cursor.close()
    except (Exception, ps.Error) as error:
        print("Error al obtener datos ", error)
    finally:
        if(conexion is not None):
            conexion.close()

while(salir!=True):
    try:
        opc=str(input("¿Categorizar vehiculo (s/n), mostrar registro (r)?\n ->"))
        if(opc.lower()=="s"):
            year=int(input("Ingresar año del vehiculo\n-> "))
            klt=int(input("Ingresar el kilometraje del vehiculo\n-> "))
            print("\t"+str(datetime.now()))
            if(year<2007 and klt>20000):
                print("\tEl vehiculo del año "+str(year)+" y kilometraje "+str(klt)+"km necesita ser renovado")
                txt_w(str(datetime.now())+"\nEl vehiculo del año "+str(year)+" y kilometraje "+str(klt)+" necesita ser renovado")
                postgres_insert(year,klt,'Renovar')
            elif(2007<=year<=2013 and 10000<klt<20000):
                print("\tEl vehiculo del año "+str(year)+" y kilometraje "+str(klt)+"km necesita mantenimiento")
                txt_w(str(datetime.now())+"\nEl vehiculo del año "+str(year)+" y kilometraje "+str(klt)+" necesita mantenimiento")
                postgres_insert(year,klt,'Mantenimiento')
            elif(year>=2013 and klt<=10000):
                print("\tEl vehiculo del año "+str(year)+" y kilometraje "+str(klt)+"km se encuentra en optimas condiciones")
                txt_w(str(datetime.now())+"\nEl vehiculo del año "+str(year)+" y kilometraje "+str(klt)+" se encuentra en optimas condiciones")
                postgres_insert(year,klt,'Optimo')
            else:
                print("\tEl vehiculo del año "+str(year)+" y kilometraje "+str(klt)+"km estado Mecanico")
                txt_w(str(datetime.now())+"\nEl vehiculo del año "+str(year)+" y kilometraje "+str(klt)+" estado Mecanico")
                postgres_insert(year,klt,'Mecanico')
        elif(opc.lower()=="r"):
            postgres_select()
        elif(opc.lower()=="n"):
            salir=True
        else:
            print("Opcion invalida elige otra!!!")
    except Exception as exc:
        print(str(exc)+"\n Algo va mal")