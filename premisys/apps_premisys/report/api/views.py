from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import pyodbc
import json

class employeeTourniquets(APIView):

    def get_employee_tourniquets(self, fini, ffin, codeEmp, sourceName, cardHolderName):
        #conn = pyodbc.connect('DRIVER={SQL Server};SERVER=SAM_SQL03;DATABASE=PremiSys;UID=empleados_consulta;PWD=Sisamex.#2020')
        conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=172.16.100.226;PORT=1433;DATABASE=PremiSys;UID=empleados_consulta;PWD=Sisamex.#2020')
        #cnn = pyodbc.connect('DRIVER=FreeTDS;SERVER=<ServidorSQLServer o IP>;PORT=1433;DATABASE=<basededatos>;UID=<usuariobd>;PWD=<passwdbd>')
        #conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=SAM_SQL03;DATABASE=PremiSys;UID=empleados_consulta;PWD=Sisamex.#2020')
        cursor = conn.cursor()
        filNameNumber = ""
        if  not codeEmp == "":
            filNameNumber =  """and c.employeenumber in ("""+ str(codeEmp) +""")"""
        elif not cardHolderName == "":
            filNameNumber = """and th.CardHolder_Name like '"""+ str(cardHolderName) +"""%'"""
        elif not sourceName == "":
            filNameNumber = """and th.Source_Name = '"""+ str(sourceName) +"""'"""
        print(filNameNumber)
                    
        QUERY = ("""
                    select c.employeenumber, th.CardHolder_Name, th.Trans_Time, th.Source_Name 
                        from TransactionHeader th 
                        left outer join cardholders.dbo.cardholders c on (th.cardholder_id = c.cardholder_id)
                    where Trans_Time between '"""+str(fini)+"""' and '""" + str(ffin)+ """'
                    """+ str(filNameNumber)+ """
                    and th.CardHolder_ID is not null order by Trans_Time
                """)

        print(QUERY)
        cursor.execute(QUERY)
        EMPLOYEE = []
        
        for row in cursor:
            EMPLOYEENUMBER          = row[0]
            CARHOLDERNAME           = row[1]
            TRANSTIME               = row[2]
            SOURCENAME              = row[3] 

            employee ={'employeeNumber':EMPLOYEENUMBER,
                        'cardHolderName':CARHOLDERNAME,
                        'transTime': TRANSTIME,
                        'sourceName': SOURCENAME
                        }
            EMPLOYEE.append(employee)
        if len(EMPLOYEE):
            result ={
                "success": True,
                "result": EMPLOYEE
            }
        else :
            result ={
                "success": False,
                "result": []
            }

        conn.close()
        return result

    #def get(self, request, format=None):
    def post(self, request):
        #print("entre")
        data = request.data
        #fecha = data['fecha']
        fi = data['fechaIni']
        ff = data['fechaFin']
        codeEmp = data['codeEmp']
        #print(codeEmp)
        sourceName = data['sourceName']
        cardHolderName = data['cardHolderName']
        print(cardHolderName)
        serializers = self.get_employee_tourniquets(fi, ff, codeEmp,sourceName, cardHolderName)
        #print(serializers)
        return Response(serializers, status.HTTP_200_OK)

class employeeSuspected(APIView):
    
    def get_employee_suspected(self, fecha, sourceName):
        #conn = pyodbc.connect('DRIVER={SQL Server};SERVER=SAM_SQL03;DATABASE=PremiSys;UID=empleados_consulta;PWD=Sisamex.#2020')
        conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=172.16.100.226;PORT=1433;DATABASE=PremiSys;UID=empleados_consulta;PWD=Sisamex.#2020')
        cursor = conn.cursor()

        QUERY = ("""                        
            select c.employeenumber, th.CardHolder_Name, th.Trans_Time, th.Source_Name from 
            TransactionHeader th left outer join cardholders.dbo.cardholders c on (th.cardholder_id = c.cardholder_id)
            where Trans_Time BETWEEN '"""+str(fecha)+""" 00:00' and '"""+str(fecha)+""" 23:59:59.999'
            and Source_Name like '%"""+str(sourceName)+"""' 
            and th.CardHolder_ID is not null order by Trans_Time
            """)

        #print(QUERY)
        cursor.execute(QUERY)
        SUSPECTED = []

        for row in cursor:
            EMPLOYEENUMBER          = row[0]
            CARHOLDERNAME           = row[1]
            TRANSTIME               = row[2]
            SOURCENAME              = row[3] 

            suspected ={'employeeNumber':EMPLOYEENUMBER,
                        'cardHolderName':CARHOLDERNAME,
                        'transTime': TRANSTIME,
                        'sourceName': SOURCENAME
                        }
            SUSPECTED.append(suspected)
        if len(SUSPECTED):
            result ={
                "success": True,
                "result": SUSPECTED
            }
        else :
            result ={
                "success": False,
                "result": []
            }

        conn.close()
        return result
    

    def post(self, request):
        #print(request.POST.get('fecha'))
        data = request.data
        #print(data['fecha'])
        #print(data['sourceName'])

        fecha = data['fecha']
        sourceName = data['sourceName']
        
        serializers = self.get_employee_suspected(fecha ,sourceName)
        #print(serializers)
        return Response(serializers, status.HTTP_200_OK)
        #return Response('test', status.HTTP_200_OK)
       
class employeeFrecuent(APIView):

    def get_employee_frecuent(self):
        #conn = pyodbc.connect('DRIVER={SQL Server};SERVER=SAM_SQL03;DATABASE=PremiSys;UID=empleados_consulta;PWD=Sisamex.#2020')
        conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=172.16.100.226;PORT=1433;DATABASE=PremiSys;UID=empleados_consulta;PWD=Sisamex.#2020')
        cursor = conn.cursor()
        
        QUERY = ("""                                    
            select c.employeenumber, th.CardHolder_Name, COUNT(c.employeenumber) AS frequent from 
            TransactionHeader th left outer join cardholders.dbo.cardholders c on (th.cardholder_id = c.cardholder_id)
            where Trans_Time BETWEEN CAST(CONVERT (date, GETDATE()) AS VARCHAR) + ' 00:00' and GETDATE()
            and th.CardHolder_ID is not null 
            GROUP BY c.employeenumber, th.CardHolder_Name
            HAVING COUNT(c.employeenumber) > 3
            order by frequent desc
        """)

        #print(QUERY)
        cursor.execute(QUERY)
        DATAFREQUENT = []

        for row in cursor:
            EMPLOYEENUMBER          = row[0]
            CARHOLDERNAME           = row[1]
            FREQUENT               = row[2]
       
            datafrequent ={'employeeNumber':EMPLOYEENUMBER,
                        'cardHolderName':CARHOLDERNAME,
                        'frequent': FREQUENT
                        }
            DATAFREQUENT.append(datafrequent)
        if len(DATAFREQUENT):
            result ={
                "success": True,
                "result": DATAFREQUENT
            }
        else :
            result ={
                "success": False,
                "result": []
            }

        conn.close()
        return result

    def get(self, request, format=None):
        serializers = self.get_employee_frecuent()
        return Response(serializers, status.HTTP_200_OK)

class employeeNumber(APIView):

    def get_employee_number(self):
        
        #conn = pyodbc.connect('DRIVER={SQL Server};SERVER=SAM_SQL03;DATABASE=PremiSys;UID=empleados_consulta;PWD=Sisamex.#2020')
        conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=172.16.100.226;PORT=1433;DATABASE=PremiSys;UID=empleados_consulta;PWD=Sisamex.#2020')
        cursor = conn.cursor()
        
        QUERY = ("""                                                
            select employeenumber from cardholders.dbo.cardholders
            group by  employeenumber 
            having employeenumber is not null
            order by employeenumber
        """)
        
        #print(QUERY)
        cursor.execute(QUERY)
        GROUPNOMINA = []

        for row in cursor:
            EMPLOYEENUMBER          = row[0]
       
            groupnomina ={
                            'employeeNumber':EMPLOYEENUMBER,
                        }
            GROUPNOMINA.append(groupnomina)
        conn.close()
        return GROUPNOMINA
    
    def get(self, request, format=None):
        serializers = self.get_employee_number()
        return Response(serializers, status.HTTP_200_OK)

# api para optener de Letores
class readTourniquets(APIView):
    def get_read_torniquets(self):
        
            #conn = pyodbc.connect('DRIVER={SQL Server};SERVER=SAM_SQL03;DATABASE=PremiSys;UID=empleados_consulta;PWD=Sisamex.#2020')
            conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=172.16.100.226;PORT=1433;DATABASE=PremiSys;UID=empleados_consulta;PWD=Sisamex.#2020')
            cursor = conn.cursor()
            QUERY = ("""
                select DISTINCT Source_Name
	            from TransactionHeader where Source_Name <> '' and Source_Name IS NOT NULL
            """)

            print(QUERY)
            cursor.execute(QUERY)
            READTOURNIQUETS = []
            
            for row in cursor:
                KEY      = row[0]
            
                readObject ={
                    'key':KEY,
                    'value': KEY,
                }

                READTOURNIQUETS.append(readObject)
            if len(READTOURNIQUETS):
                result ={
                    "success": True,
                    "result": READTOURNIQUETS
                }
            else :
                result ={
                    "success": False,
                    "result": []
                }

            conn.close()
            return result
       
            
           

    def get(self, request, format=None):
        try:
            serializers = self.get_read_torniquets()
            return Response(serializers, status.HTTP_200_OK)
        except:
            return Response("Ocurrio un error", status.HTTP_302_FOUND)