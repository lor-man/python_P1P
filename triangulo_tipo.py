import psycopg2 as ps
from datetime import datetime
salir = False

print("Tipo de triángulo")
def select_triangulo(l1,l2,l3):
    if(l1==l2==l3):
        return "Equilatero"
    elif(l1==l2 or l1==l3 or l3==l2):
        return "Isósceles"
    else:
        return "Escaleno"

def postgres_insert(l1,l2,l3,tipo):
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO public.tipo_triangulo(no_transaccion,lado_1,lado_2,lado_3,tipo,fecha )
        VALUES(nextval('pk_tipo_triangulo'),%(ld1)s,%(ld2)s,%(ld3)s,%(tipo)s,%(date)s);""",{'ld1':l1,'ld2':l2,'ld3':l3,'tipo':tipo,'date':datetime.now()})
        conexion.commit()
        cursor.close()
    except (Exception,ps.DatabaseError) as exc:
        print(exc)
        print("Conexion con base de datos fallida")
    finally:
        if conexion is not None:
            conexion.close()

def postgres_select():
    selectquery="""SELECT * FROM public.tipo_triangulo ORDER BY no_transaccion ASC """
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute(selectquery)
        datos=cursor.fetchall()
        print("Registro de datos del programa:")
        for fila in datos:
            print("No_transacción: ",fila[0])
            print("Lado 1= ",fila[1])
            print("Lado 2= ",fila[2])
            print("Lado 3= ",fila[3])
            print("Tipo: ",fila[4])
            print("Fecha :",fila[5])
        cursor.close()
    except (Exception, ps.Error) as error:
        print("Error al obtener datos ", error)
    finally:
        if(conexion is not None):
            conexion.close()

def lados():
    try:
        l1=float(input("\tIngresar lado 1\n\t-> "))
        l2=float(input("\tIngresar lado 2\n\t-> "))
        l3=float(input("\tIngresar lado 3\n\t-> "))
        return l1,l2,l3
    except Exception as exc:
        print(str(exc))

def txt_w(resultado):
        try:
            with open('triangulo_tipo.txt','a',newline='',encoding = 'utf-8') as file:
                file.write(resultado+"\n")
        except Exception as exc0:
            print(str(exc0) + "\n No se puede leer el archivo .txt")

while(salir!=True):
    try:
        opc=str(input("¿Ingresar lados de triángulo(s/n), mostrar registro (r)?\n ->"))
        if(opc.lower()=="s"):
            l1,l2,l3=lados()
            if(l1>0 and l2>0 and l3>0):
                triangulo=select_triangulo(l1,l2,l3)
                print("\t"+str(datetime.now()))
                print("\tEl triángulo con lados: l1="+str(l1)+" l2="+str(l2)+" l3="+str(l3)+"\n\tEs un triángulo: "+triangulo)
                txt_w("\t"+str(datetime.now())+"\n\tEl triángulo con lados: l1="+str(l1)+" l2="+str(l2)+" l3="+str(l3)+"\n\tEs un triángulo: "+triangulo)
                postgres_insert(l1,l2,l3,triangulo)
            else:
                print("Ingresar numeros positivos unicamente!!!!")
        elif(opc.lower()=="r"):
            postgres_select()
        elif(opc.lower()=="n"):
            salir=True
        else:
            print("Opcion invalida elige otra!!!")
    except Exception as exc:
        print(str(exc)+"\n Algo va mal")