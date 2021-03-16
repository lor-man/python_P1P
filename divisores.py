import psycopg2 as ps
print("Divisores")
salir = False

def txt_w(resultado):
        try:
            with open('divisores.txt','a',newline='',encoding = 'utf-8') as file:
                file.write("\n "+resultado+"\n")
        except Exception as exc0:
            print(str(exc0) + "\n No se puede leer el archivo .txt")

def postgres_insert(num,divisores):
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO public.divisores(no_transaccion,"numero(+/-)", "divisores(+/-)")
        VALUES(nextval('pk_divisores'),%s,%s)""",(num,divisores))
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
        opc=str(input("¿Obtener divisores s/n?\n ->"))
        if(opc.lower()=="s"):
            div=abs(int(input("Ingresar numero:\n ->")))
            divisores = []
            for i in range(1,div+1):
                if(div%i==0):
                    divisores.append(i)
            print("\tLos divisores de (+/-)"+ str(div)+ " son (+/-): \n\t"+str(divisores))
            txt_w("\tLos divisores de (+/-)"+ str(div)+ " son (+/-): \n\t"+str(divisores))
            postgres_insert(div,divisores)
        elif(opc.lower()=="n"):
            salir=True
        else:
            print("Opcion invalida elige otra!!!")
    except Exception as exc:
        print(str(exc)+"\n Algo va mal")    