import os
import pyodbc
import platform
from datetime import (
    date
)

from xlsxwriter.workbook import Workbook
import xlsxwriter


import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "premisys.settings")
django.setup()


from django.conf import settings
from django.core.mail import EmailMessage

from empleados.models import (
    Empleado,
)
from datetime import (
    date,
    datetime,
    timedelta,
)
from django.utils import timezone
from django.db.models import (
    Count,
)


def obtener_fecha_tz(fecha):
    zona_horaria = timezone.get_current_timezone()
    fecha = zona_horaria.localize(
        timezone.datetime.strptime(
            '%s' % (
                fecha
            ),
            '%Y-%m-%d %H:%M:%S'
        )
    )
    return fecha


def genera_reporte_top():
    print('----Inicio')
    print('----1 Se conecta a SQL Server')
    
    server = '172.16.100.226' 
    database = 'PremiSys' 
    username = 'empleados_consulta' 
    password = 'Sisamex.#2020'
    puerto = '1433'
    cad_conexion_local = 'DRIVER={ODBC Driver 13 for SQL Server}'
    cad_conexion_prod = 'DRIVER=FreeTDS'
    cad_conexion = cad_conexion_local
    cad_conexion += ';SERVER=' + server
    cad_conexion += ';DATABASE=' + database
    cad_conexion += ';UID=' + username
    cad_conexion += ';PWD=' + password
    cad_conexion += ';PORT=' + puerto
    conn = pyodbc.connect(cad_conexion)  
    
    cursor = conn.cursor()

    myQry = """
        select c.employeenumber, th.CardHolder_Name, COUNT(c.employeenumber) AS frequent from 
        TransactionHeader th left outer join cardholders.dbo.cardholders c on (th.cardholder_id = c.cardholder_id)
        where Trans_Time BETWEEN CAST(CONVERT (date, GETDATE()) AS VARCHAR) + ' 00:00' and GETDATE()
        and th.CardHolder_ID is not null 
        GROUP BY c.employeenumber, th.CardHolder_Name
        HAVING COUNT(c.employeenumber) > 3
        order by frequent desc
    """
    cursor.execute(myQry) 
    rows = cursor.fetchall()
    msg = ""

    print('----2.1 Recorre los datos Premisys y los vacia en un JSON')
    
    lista_datafrequent = []
    for row in rows:
        EMPLOYEENUMBER = row[0]
        CARHOLDERNAME = row[1]
        FREQUENT = row[2]

        datafrequent = {
            'employeeNumber': EMPLOYEENUMBER,
            'cardHolderName': CARHOLDERNAME,
            'frequent': FREQUENT
        }
        lista_datafrequent.append(datafrequent)
    
    cursor.close()
    conn.close()

    if len(datafrequent) >= 1:
        print('----3.1 Vacia el JSON Premisys a un Excel')
    
        sistema_operativo = platform.system()
        if sistema_operativo.upper() == 'WINDOWS':
            archivo = '\Reporte_top_movilidad_aduanas.xlsx'
        else:
            archivo = '/Reporte_top_movilidad_aduanas.xlsx'
        path_archivo = settings.MEDIA_ROOT + archivo

        
        workbook = xlsxwriter.Workbook(path_archivo)
        worksheet = workbook.add_worksheet()
        
        
        format_bold = workbook.add_format({'bold': True})
        format_fontsize = workbook.add_format({'bold': True})
        format_fontsize.set_font_size(15)

        
        fecha_hoy_cad = datetime.strftime(date.today(), '%d-%m-%Y')
        worksheet.write(0, 1, 'Parametros', format_bold)
        worksheet.write(1, 1, 'Fecha:  ' + fecha_hoy_cad)
        
        
        renglon_titulo = 3
        worksheet.write(renglon_titulo, 2, 'REPORTE TOP MOVILIDAD Y ADUANAS', format_fontsize)

        renglon_titulo_columnas = renglon_titulo + 1
        worksheet.write(renglon_titulo_columnas, 0, 'No.', format_bold)
        worksheet.write(renglon_titulo_columnas, 1, 'Nomina', format_bold)
        worksheet.write(renglon_titulo_columnas, 2, 'Nombre', format_bold)
        worksheet.write(renglon_titulo_columnas, 3, 'Lectores', format_bold)

        worksheet.write(renglon_titulo_columnas, 5, 'No.', format_bold)
        worksheet.write(renglon_titulo_columnas, 6, 'Aduana', format_bold)
        worksheet.write(renglon_titulo_columnas, 7, 'Cantidad de transacciones', format_bold)

        worksheet.set_column('A:A', 8)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 40)
        worksheet.set_column('D:D', 15)

        worksheet.set_column('F:F', 10)
        worksheet.set_column('G:G', 10)
        worksheet.set_column('H:H', 25) 

        renglon = renglon_titulo + 2
        renglon_aduana = renglon_titulo + 2
        for registro in lista_datafrequent:
            worksheet.write(renglon, 0, str(renglon-renglon_titulo_columnas))
            if registro['employeeNumber'] is not None:
                worksheet.write(renglon, 1, str(registro['employeeNumber']))
            worksheet.write(renglon, 2, registro['cardHolderName'])
            worksheet.write(renglon, 3, str(registro['frequent']))
            renglon += 1
        

        print('----3.2 Recorre los datos Empleados (Aduanas) y los vacia en un JSON')
        json_aduanas = []
        queryset = Empleado.objects.using('db_meraki').all()
        fecha_hoy = date.today()
        fecha_inicial = obtener_fecha_tz('%s 00:00:01' % fecha_hoy)
        fecha_final = obtener_fecha_tz('%s 23:59:59' % fecha_hoy)
        queryset = queryset.filter(
            fecha_creacion__range=[
                fecha_inicial,
                fecha_final,
            ]
        )
        json_aduanas = queryset.values('aduana').order_by('-aduana__count').annotate(Count('aduana'))
        
        print('----3.3 Vacia el JSON Aduanas a un Excel')
        for registro in json_aduanas:
            worksheet.write(renglon_aduana, 5, str(renglon_aduana-renglon_titulo_columnas))
            worksheet.write(renglon_aduana, 6, str(registro['aduana']))
            worksheet.write(renglon_aduana, 7, str(registro['aduana__count']))
            renglon_aduana += 1
        
        workbook.close()

        print('----4 Envia correo')
        
        subject = 'Reporte Top Movilidad y Aduanas'
        body = 'Se envia reporte solicitado'
        
        lista_destinatarios = [
            'jose-becerra@sisamex.com.mx',
            'enrique-parra@sisamex.com.mx'
        ]
        to = lista_destinatarios
        email = EmailMessage(
            subject=subject, 
            body=body, 
            to=to, 
            cc=[], 
            bcc=[], 
        )
        email.attach_file(path_archivo)
        email.send()

    print('----Fin')

genera_reporte_top()
