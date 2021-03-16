import psycopg2 as ps
print("Numeros de 2 en 2")
salir = False

def txt_w(resultado):
        try:
            with open('numeros_inicio_fin.txt','a',newline='',encoding = 'utf-8') as file:
                file.write(resultado+"\n")
        except Exception as exc0:
            print(str(exc0) + "\n No se puede leer el archivo .txt")

def postgres_insert(num1,num2,nums):
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO public.numeros_inicio_fin(no_transaccion, numero_inicio, numero_final, serie_2_2)
        VALUES(nextval('pk_numeros_2_2'),%s,%s,%s)""",(num1,num2,nums))
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
        opc=str(input("¿Desplegar números s/n?\n ->"))
        if(opc.lower()=="s"):
            numero_menor=int(input("\tIngresar el numero inicial: \n\t ->"))
            numero_mayor=int(input("\tIngresar el numero final:   \n\t ->"))
            if(numero_mayor>numero_menor):
                serie_2=[]
                aux=numero_menor
                serie_2.append(numero_menor)
                while(aux<numero_mayor-1):
                    aux+=2
                    serie_2.append(aux)
                print("\tNumeros de 2 en 2 desde "+str(numero_menor)+" hasta "+str(numero_mayor)+":\n\t"+str(serie_2))
                txt_w("* Numeros de 2 en 2 desde "+str(numero_menor)+" hasta "+str(numero_mayor)+":\n\t"+str(serie_2))
                postgres_insert(numero_menor,numero_mayor,serie_2)
            else:
                print("Cambie el orden de los números de entrada")
        elif(opc.lower()=="n"):
            salir=True
        else:
            print("Opcion invalida elige otra!!!")
    except Exception as exc:
        print(str(exc)+"\n Algo va mal")