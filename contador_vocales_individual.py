import psycopg2 as ps
print("Vocales 0.2")
salir = False

def txt_w(resultado):
        try:
            with open('contador_vocales_02.txt','a',newline='',encoding = 'utf-8') as file:
                file.write(resultado+"\n")
        except Exception as exc0:
            print(str(exc0) + "\n No se puede leer el archivo .txt")

def postgres_insert(palabra,a,e,i,o,u):
    conexion=None
    try:
        conexion=ps.connect(database="python",user="postgres",password="123456",host="172.30.128.1",port="5432")
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO public.contador_vocales_02(no_transaccion, palabra,a,e,i,o,u)
        VALUES(nextval('pk_cnt_vocal_02'),%s,%s,%s,%s,%s,%s)""",(palabra,a,e,i,o,u))
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
        opc=str(input("¿Contar vocales 0.2 s/n?\n ->"))
        if(opc.lower()=="s"):
            palabra_0=str(input("Ingresar palabra\n ->"))
            palabra_1=palabra_0.lower()
            cnta=cnte=cnti=cnto=cntu=0
            for voc in palabra_1:
                if(voc=="a"or voc=="á"):
                    cnta+=1
                elif(voc=="e"or voc=="é"):
                    cnte+=1                    
                elif(voc=="i"or voc=="í"):
                    cnti+=1
                elif(voc=="o"or voc=="ó"):
                    cnto+=1
                elif(voc=="u"or voc=="ú" or voc=="ü"):
                    cntu+=1
            print("La palabra "+palabra_0+" tiene cada vocal la siguiente cantidad de veces:\n\ta="+str(cnta)+"\n\te="+str(cnte)+"\n\ti="+str(cnti)+"\n\to="+str(cnto)+"\n\tu="+str(cntu))
            txt_w("*La palabra "+palabra_0+" tiene cada vocal la siguiente cantidad de veces:\n\ta="+str(cnta)+"\n\te="+str(cnte)+"\n\ti="+str(cnti)+"\n\to="+str(cnto)+"\n\tu="+str(cntu))
            postgres_insert(palabra_0,cnta,cnte,cnti,cnto,cntu)
        elif(opc.lower()=="n"):
            salir=True
        else:
            print("Opcion invalida elige otra!!!")
    except Exception as exc:
        print(str(exc)+"\n Algo va mal")
    