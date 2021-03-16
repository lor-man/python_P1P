import psycopg2 as ps
from datetime import datetime
from math import pi,sqrt
print("Área de figuras")
salir = False

def txt_w(resultado):
        try:
            with open('area.txt','a',newline='',encoding = 'utf-8') as file:
                file.write(resultado+"\n")
        except Exception as exc0:
            print(str(exc0) + "\n No se puede leer el archivo .txt")

def postgres_insert(figura,area):
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO public.area(no_transaccion,fecha,figura,area)
        VALUES(nextval('pk_area'),%(fecha)s,%(fig)s,%(ar)s)""",{'fecha':datetime.now(),'fig':figura,'ar':area})
        conexion.commit()
        cursor.close()
    except (Exception,ps.DatabaseError) as exc:
        print(exc)
        print("Conexion con base de datos fallida")
    finally:
        if conexion is not None:
            conexion.close()

def postgres_select():
    selectquery="""SELECT * FROM public.area ORDER BY no_transaccion ASC"""
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
            print("Figura: ",fila[2])
            print("Área: ",fila[3])
            print("")
        cursor.close()
    except (Exception, ps.Error) as error:
        print("Error al obtener datos ", error)
    finally:
        if(conexion is not None):
            conexion.close()

def circulo(radio):
    return pi*radio**2
def cuadrado(lado):
    return lado**2
def rectangulo(ld1,ld2):
    return ld1*ld2
def triangulo1(base,altura):
    return base*altura*0.5
def triangulo2(ld1,ld2,ld3):
    s=(ld1+ld2+ld3)/2
    area=sqrt(s*(s-ld1)*(s-ld2)*(s-ld3))
    return area

def calc_area(figura):
    area=None
    if(figura=='c'):
        rad=float(input("\tIngrese el radio\n\t->"))
        area=circulo(rad)
        return area,"Círculo" 
    elif(figura=='s'):
        lad=float(input("\tIngrese el lado\n\t->"))
        area=cuadrado(lad)
        return area,"Cuadrado" 
    elif(figura=='r'):
        lad1=float(input("\tIngrese el lado 1\n\t->"))
        lad2=float(input("\tIngrese el lado 2\n\t->"))
        area=rectangulo(lad1,lad2)
        return area,"Rectangulo"
    elif(figura=='t'):
        print("¿Se cuenta con los lados(l) o con base y altura(bh)?")
        opct=str(input("-> ")).lower()
        if(opct=="l"):
            lad1t=float(input("\tIngrese el lado 1\n\t->"))
            lad2t=float(input("\tIngrese el lado 2\n\t->"))
            lad3t=float(input("\tIngrese el lado 3\n\t->"))
            area=triangulo2(lad1t,lad2t,lad3t)
            return area,"Triángulo"
        elif(opct=="bh"):
            bas=float(input("\tIngrese la base\n\t->"))
            alt=float(input("\tIngrese la altura\n\t->"))
            area=triangulo1(bas,alt)
            return area,"Triángulo"
    else:
        print("Opción incorrecta!!!")
        return None,None

while(salir!=True):
    try:
        opc=str(input("¿Calcular area (s/n), registro de programa (r)?\n ->"))
        if(opc.lower()=="s"):
            print("¿De que figura desea calcular el área circulo(c),cuadrado(s),rectangulo(r) o triángulo(t)?")
            fig=str(input("->")).lower()
            areaFig,Fig=calc_area(fig)
            if(type(areaFig)!=type(None)and type(Fig)!=type(None)):
                print("\t"+str(datetime.now()))
                print("\t El área de "+Fig+" es: "+str(areaFig))
                txt_w(""+str(datetime.now())+"\n\t El área de "+Fig+" es: "+str(areaFig))
                postgres_insert(Fig,areaFig)
        elif(opc.lower()=="r"):
            postgres_select()
        elif(opc.lower()=="n"):
            salir=True
        else:
            print("Opcion invalida elige otra!!!")
    except Exception as exc:
        print(str(exc)+"\n Algo va mal")