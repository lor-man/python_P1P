import psycopg2 as ps
print("\t\tSumatoria")
print("\t    k=N\n\t   ------\n\t   \\        |    /\n\t    \\       |   /\n\t     |      | || \n\t    /       |   \\ \n\t   /        |    \\ \n\t   ------\n\t    k=1")

salir = False

def txt_w(resultado):
        try:
            with open('sumatoria.txt','a',newline='',encoding = 'utf-8') as file:
                file.write(resultado+"\n")
        except Exception as exc0:
            print(str(exc0) + "\n No se puede leer el archivo .txt")

def postgres_insert(numero, sumatoria):
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO public.sumatoria(no_transaccion, numero, sumatoria)
        VALUES(nextval('pk_sumatoria'),%s,%s)""",(numero,sumatoria))
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
        opc=str(input("¿Realizar sumatoria s/n?\n ->"))
        if(opc.lower()=="s"):
            numero=int(input("\t Ingresar numero de sumatoria: \n\t ->")) 
            vect=range(1,numero+1)
            sumatoria=sum(vect)
            print("\t   La sumatoria desde 1 hasta "+str(numero)+" es: "+ str(sumatoria))   
            txt_w("* La sumatoria desde 1 hasta "+str(numero)+" es: "+ str(sumatoria))
            postgres_insert(numero,sumatoria)
        elif(opc.lower()=="n"):
            salir=True
        else:
            print("Opcion invalida elige otra!!!")
    except Exception as exc:
        print(str(exc)+"\n Algo va mal")