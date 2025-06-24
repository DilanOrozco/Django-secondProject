from django.http import HttpResponse
from django.shortcuts import render, redirect 
from django.contrib import messages
from .models import Estudiante, Reporte
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook


# Create your views here.
def index(request):
    return render(request, 'index.html')



def registrar_estudiante(request):
    if request.method == 'POST':
        Estudiante.objects.create(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            tipo_documento=request.POST['tipo_documento'],
            numero_documento=request.POST['numero_documento'],
            telefono=request.POST['telefono'],
            correo=request.POST['correo'],
            ficha=request.POST['ficha'],
            programa=request.POST['programa'],
            horario=request.POST['horario']
        )
        return redirect('registrar')
    return render(request, 'registrar_estudiante.html')

def reporte_academico(request):
    estudiantes = Estudiante.objects.all()
    if request.method == 'POST':
        estudiante_id = request.POST['estudiante']
        estudiante = Estudiante.objects.get(id=estudiante_id)
        Reporte.objects.create(
            estudiante=estudiante,
            tipo=request.POST['tipo'],
            detalle=request.POST['detalle'],
            instructor=request.POST['instructor']
        )
        return redirect('reporte')
    return render(request, 'reporte_academico.html', {'estudiantes': estudiantes})

def listado_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request, 'listado_estudiantes.html', {'estudiantes' : estudiantes})

def listado_reportes(request):
    reportes = Reporte.objects.all()
    return render(request, 'listado_reportes.html', {'reportes' : reportes})
    

def eliminar_estudiante(request, estudiante_id):
    estudiante = Estudiante.objects.get(id = estudiante_id)
    # preguntar confirmacion de eliminacion
    if request.method == 'POST':
        # si confirma eliminar estudiante
        if 'confirmar' in request.POST:
            estudiante.delete()
            messages.success(request, 'Estudiante eliminado exitosamente')
            return redirect('listado_estudiantes')
        else:
            return redirect('listado_estudiantes')
    return render(request, 'confirmar_eliminacion.html', {'estudiante': estudiante})

def eliminar_reporte(request, reporte_id):
    reporte = Reporte.objects.get(id = reporte_id)
    # preguntar confirmacion de eliminacion
    if request.method == 'POST':
        # si confirma eliminar estudiante
        if 'confirmar' in request.POST:
            reporte.delete()
            messages.success(request, 'Reporte eliminado exitosamente')
            return redirect('listado_reportes')
        else:
            return redirect('listado_estudiantes')
    return render(request, 'confirmar_eliminacion_reporte.html', {'reporte': reporte})

def editar_estudiante(request, estudiante_id):
    estudiante = Estudiante.objects.get(id=estudiante_id)
    if request.method == 'POST':
        try:
            estudiante.nombre = request.POST['nombre']
            estudiante.apellido = request.POST['apellido']
            estudiante.tipo_documento = request.POST['tipo_documento']
            estudiante.numero_documento = request.POST['numero_documento']
            estudiante.telefono = request.POST['telefono']
            estudiante.correo = request.POST['correo']
            estudiante.ficha = request.POST['ficha']
            estudiante.programa = request.POST['programa']
            estudiante.horario = request.POST['horario']
            estudiante.save()
            messages.success(request, 'Actualización exitosa')
        except Exception as e :
            messages.error(e, 'Error al actualizar')
        return redirect('listado_estudiantes')
    return render(request, 'editar_estudiante.html', {'estudiante' : estudiante})

def editar_reporte(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    
    if request.method == 'POST':
        try:
            # Obtener el objeto Estudiante usando el ID enviado desde el formulario
            estudiante_id = request.POST['estudiante']
            estudiante = Estudiante.objects.get(id=estudiante_id)
            
            # Asignar los valores correctamente
            reporte.tipo = request.POST['tipo']
            reporte.estudiante = estudiante  # Asignar el objeto, no el string
            reporte.detalle = request.POST['detalle']
            reporte.instructor = request.POST['instructor']
            reporte.save()
            
            messages.success(request, 'Actualización exitosa')
            
        except Estudiante.DoesNotExist:
            messages.error(request, 'El estudiante seleccionado no existe')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')  # Corregir el primer parámetro
            
        return redirect('listado_reportes')
    
    # Para el GET request, necesitas pasar los estudiantes para el formulario
    estudiantes = Estudiante.objects.all()
    return render(request, 'editar_reporte.html', {
        'reporte': reporte,
        'estudiantes': estudiantes  # Agregar esto para el formulario
    })
        
# Exportar clientes a PDF
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from .models import Estudiante

def exportar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listado_de_estudiantes.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Título centrado
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.darkblue)
    p.drawCentredString(width / 2, 760, "Listado de Estudiantes")
    
    # Línea debajo del título
    p.setStrokeColor(colors.black)
    p.line(50, 755, width - 50, 755)

    # Encabezados
    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(colors.black)
    y = 730
    p.drawString(50, y, "Nombre")
    p.drawString(140, y, "Documento")
    p.drawString(210, y, "Teléfono")
    p.drawString(260, y, "Correo")
    p.drawString(370, y, "Ficha")
    p.drawString(430, y, "Programa")
    p.drawString(510, y, "Horario")

    y -= 15
    p.line(50, y, width - 50, y)
    y -= 15

    # Contenido
    p.setFont("Helvetica", 8)
    estudiantes = Estudiante.objects.all()

    for est in estudiantes:
        if y < 60:
            p.showPage()
            y = 760
            p.setFont("Helvetica-Bold", 10)
            p.drawString(50, y, "Nombre")
            p.drawString(140, y, "Documento")
            p.drawString(210, y, "Teléfono")
            p.drawString(260, y, "Correo")
            p.drawString(370, y, "Ficha")
            p.drawString(430, y, "Programa")
            p.drawString(510, y, "Horario")
            y -= 15
            p.line(50, y, width - 50, y)
            y -= 15
            p.setFont("Helvetica", 9)

        # Filas con alineación básica
        p.drawString(50, y, f"{est.nombre} {est.apellido}")
        p.drawString(140, y, f"{est.tipo_documento} {est.numero_documento}")
        p.drawString(210, y, est.telefono)
        p.drawString(260, y, est.correo)
        p.drawString(370, y, str(est.ficha))
        p.drawString(430, y, est.programa)
        p.drawString(510, y, est.horario)
        y -= 18

    p.showPage()
    p.save()
    return response


# Exportar clientes a Excel
def exportar_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Estudiantes.xlsx"'
    wb = Workbook()
    ws = wb.active
    ws.append(['Documento', 'Nombres', 'Apellidos', 'Teléfono', 'Correo'])
    estudiantes = Estudiante.objects.all()
    for estudiante in estudiantes:
        ws.append([estudiante.numero_documento, estudiante.nombre, estudiante.apellido, estudiante.telefono, estudiante.correo])
    wb.save(response)
    return response

def exportar_reportes_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listado_de_reportes.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Título centrado
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.darkblue)
    p.drawCentredString(width / 2, 760, "Listado de Reportes")
    
    # Línea debajo del título
    p.setStrokeColor(colors.black)
    p.line(50, 755, width - 50, 755)
    
    # Encabezados
    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(colors.black)
    y = 730
    p.drawString(50, y, "Estudiante")
    p.drawString(150, y, "Tipo")
    p.drawString(220, y, "Instructor")
    p.drawString(320, y, "Fecha")
    p.drawString(420, y, "Detalle")
    
    y -= 15
    p.line(50, y, width - 50, y)
    y -= 15
    
    # Contenido
    p.setFont("Helvetica", 8)
    reportes = Reporte.objects.all().order_by('-fecha')
    
    for reporte in reportes:
        if y < 60:
            p.showPage()
            y = 760
            p.setFont("Helvetica-Bold", 10)
            p.drawString(50, y, "Estudiante")
            p.drawString(150, y, "Tipo")
            p.drawString(220, y, "Instructor")
            p.drawString(320, y, "Fecha")
            p.drawString(420, y, "Detalle")
            y -= 15
            p.line(50, y, width - 50, y)
            y -= 15
            p.setFont("Helvetica", 8)
        
        # Filas con datos del reporte
        estudiante_nombre = f"{reporte.estudiante.nombre} {reporte.estudiante.apellido}"
        fecha_formateada = reporte.fecha.strftime("%d/%m/%Y")
        detalle_corto = reporte.detalle[:30] + "..." if len(reporte.detalle) > 30 else reporte.detalle
        
        p.drawString(50, y, estudiante_nombre)
        p.drawString(150, y, reporte.tipo)
        p.drawString(220, y, reporte.instructor)
        p.drawString(320, y, fecha_formateada)
        p.drawString(420, y, detalle_corto)
        y -= 18
    
    p.showPage()
    p.save()
    return response


def exportar_reportes_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Reportes.xlsx"'
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Reportes"
    
    # Encabezados
    ws.append(['Estudiante', 'Documento', 'Tipo Reporte', 'Instructor', 'Fecha', 'Detalle'])
    
    reportes = Reporte.objects.all().order_by('-fecha')
    
    for reporte in reportes:
        estudiante_nombre = f"{reporte.estudiante.nombre} {reporte.estudiante.apellido}"
        fecha_formateada = reporte.fecha.strftime("%d/%m/%Y %H:%M")
        
        ws.append([
            estudiante_nombre,
            reporte.estudiante.numero_documento,
            reporte.tipo,
            reporte.instructor,
            fecha_formateada,
            reporte.detalle
        ])
    
    wb.save(response)
    return response