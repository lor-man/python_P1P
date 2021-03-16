import psycopg2 as ps
print("Orden descendente")
salir = False

def txt_w(resultado):
        try:
            with open('orden_descendente.txt','a',newline='',encoding = 'utf-8') as file:
                file.write(resultado+"\n")
        except Exception as exc0:
            print(str(exc0) + "\n No se puede leer el archivo .txt")

def postgres_insert(num1,num2,nums):
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO public.orden_descendente(no_transaccion, numero_menor, numero_mayor, descendente)
        VALUES(nextval('pk_orden_descendente'),%s,%s,%s)""",(num1,num2,nums))
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
        opc=str(input("¿Mostrar números descendentes s/n?\n ->"))
        if(opc.lower()=="s"):
            num_1=int(input("\tIngrese el primer número:\n\t ->"))
            num_2=int(input("\tIngrese el segundo número:\n\t ->"))
            serie_desc=[]
            if(num_1>num_2):
                for i in range(num_1,num_2-1,-1):
                    serie_desc.append(i)
                print("\tLos numeros desde "+str(num_1)+" hasta "+str(num_2)+" son:\n\t"+str(serie_desc))
                txt_w("*Los numeros desde "+str(num_1)+" hasta "+str(num_2)+" son:\n\t"+str(serie_desc))
                postgres_insert(num_2,num_1,serie_desc)
            elif(num_1<num_2):
                for i in range(num_2,num_1-1,-1):
                    serie_desc.append(i)
                print("\tLos numeros desde "+str(num_2)+" hasta "+str(num_1)+" son:\n\t"+str(serie_desc))
                txt_w("*Los numeros desde "+str(num_2)+" hasta "+str(num_1)+" son:\n\t"+str(serie_desc))
                postgres_insert(num_1,num_2,serie_desc)
            else:
                print("Has roto el universo")
        elif(opc.lower()=="n"):
            salir=True
        else:
            print("Opcion invalida elige otra!!!")
    except Exception as exc:
        print(str(exc)+"\n Algo va mal")