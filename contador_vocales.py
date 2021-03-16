import psycopg2 as ps
print("Vocales")
salir = False

def txt_w(resultado):
        try:
            with open('contador_vocales.txt','a',newline='',encoding = 'utf-8') as file:
                file.write(resultado+"\n")
        except Exception as exc0:
            print(str(exc0) + "\n No se puede leer el archivo .txt")

def postgres_insert(palabra,cant_vocales):
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO public.contador_vocales("no_transacción", palabra, cantidad_vocales)
        VALUES(nextval('pk_cnt_vocal'),%s,%s)""",(palabra,cant_vocales))
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
        opc=str(input("¿Contar vocales s/n?\n ->"))
        if(opc.lower()=="s"):
            palabra_0=str(input("Ingresar palabra\n ->"))
            palabra_1=palabra_0.lower()
            cntv=0
            for voc in palabra_1:
                if(voc=="a" or voc=="e" or voc=="i" or voc=="o" or voc=="u" or voc=="á" or voc=="é" or voc=="í" or voc=="ó" or voc=="ú" or voc=="ü"):
                    cntv+=1
            print("\tLa palabra "+palabra_0+ " tiene "+ str(cntv)+" vocales")
            txt_w("*\tLa palabra "+palabra_0+ " tiene "+ str(cntv)+" vocales") 
            postgres_insert(palabra_0,cntv) 
        elif(opc.lower()=="n"):
            salir=True
        else:
            print("Opcion invalida elige otra!!!")
    except Exception as exc:
        print(str(exc)+"\n Algo va mal")
    