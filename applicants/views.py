from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Applicant, Application
from .forms import ApplicantForm, ApplicationForm
from django.http import HttpResponse
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os
from django.conf import settings

class ApplicantListView(ListView):
    model = Applicant
    template_name = 'applicants/applicant_list.html'
    context_object_name = 'applicants'
    paginate_by = 20

class ApplicantDetailView(DetailView):
    model = Applicant
    template_name = 'applicants/applicant_detail.html'
    context_object_name = 'applicant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = self.object.application_set.all()
        return context

class ApplicantCreateView(CreateView):
    model = Applicant
    form_class = ApplicantForm
    template_name = 'applicants/applicant_form.html'
    success_url = reverse_lazy('applicants:applicant_list')

class ApplicationListView(ListView):
    model = Application
    template_name = 'applicants/application_list.html'
    context_object_name = 'applications'  # Исправлено с 'applications' на 'applications'
    paginate_by = 20
    
class ApplicationUpdateView(UpdateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'applicants/application_form.html'
    success_url = reverse_lazy('applicants:application_list')

class ApplicationCreateView(CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'applicants/application_form.html'
    success_url = reverse_lazy('applicants:application_list')

class ApplicantUpdateView(UpdateView):
    model = Applicant
    form_class = ApplicantForm
    template_name = 'applicants/applicant_form.html'
    success_url = reverse_lazy('applicants:applicant_list')
    
class ApplicationDetailView(DetailView):
    model = Application
    template_name = 'applicants/application_detail.html'
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context

def generate_pdf_document(request, applicant_id, application_id):
    # Регистрируем шрифт для поддержки кириллицы
    try:
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'arial.ttf')
        pdfmetrics.registerFont(TTFont('Arial', font_path))
        pdfmetrics.registerFont(TTFont('Arial-Bold', 
            os.path.join(settings.BASE_DIR, 'static', 'fonts', 'arialbd.ttf')))
    except:
        # Если шрифты не найдены, попробуем использовать стандартные
        try:
            pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
            pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
        except:
            pass

    # Получаем данные
    applicant = Applicant.objects.get(pk=applicant_id)
    application = Application.objects.get(pk=application_id)
    
    # Создаем буфер для PDF
    buffer = BytesIO()
    
    # Создаем PDF-документ
    doc = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Устанавливаем шрифты
    try:
        doc.setFont("Arial-Bold", 14)
    except:
        doc.setFont("Helvetica-Bold", 14)
    
    # Название организации (обновлено)
    org_name = 'АВТОНОМНАЯ НЕКОММЕРЧЕСКАЯ ОРГАНИЗАЦИЯ ПРОФЕССИОНАЛЬНОГО ОБРАЗОВАНИЯ'
    org_name2 = '"КОЛЛЕДЖ МИРОВОЙ ЭКОНОМИКИ И ПЕРЕДОВЫХ ТЕХНОЛОГИЙ"'
    
    # Шапка документа
    doc.drawCentredString(width/2, height-2*cm, org_name)
    doc.drawCentredString(width/2, height-2.5*cm, org_name2)
    
    # Название документа
    doc.setFont("Arial-Bold", 16) if 'Arial-Bold' in pdfmetrics.getRegisteredFontNames() else doc.setFont("Helvetica-Bold", 16)
    doc.drawCentredString(width/2, height-4*cm, "СПРАВКА")
    doc.setFont("Arial", 12) if 'Arial' in pdfmetrics.getRegisteredFontNames() else doc.setFont("Helvetica", 12)
    
    # Основной текст
    text_lines = [
        f"Дана {applicant.full_name}, {applicant.birth_date.strftime('%d.%m.%Y')} г.р., в том, что",
        f"он(а) подал(а) заявление на поступление в Колледж по программе:",
        f"«{application.program.name}» (код: {application.program.code}).",
        "",
        f"Статус заявления: {application.get_status_display()}.",
        ""
    ]
    
    if application.status == 'approved':
        text_lines.extend([
            f"Рекомендован(а) к зачислению на {'бюджетную' if application.program.budget_places > 0 else 'платную'}",
            "основу обучения."
        ])
    
    # Позиция для текста
    y_position = height - 6*cm
    
    # Выводим текст
    for line in text_lines:
        doc.drawString(2*cm, y_position, line)
        y_position -= 0.7*cm
    
    # Подпись
    doc.line(2*cm, y_position-1.5*cm, 7*cm, y_position-1.5*cm)
    doc.drawString(2*cm, y_position-2*cm, "Директор приемной комиссии")
    
    # Печать и дата
    doc.drawRightString(width-2*cm, y_position-2*cm, "М.П.")
    doc.drawRightString(width-2*cm, y_position-2.5*cm, datetime.now().strftime("%d.%m.%Y"))
    
    # Футер
    doc.setFont("Arial-Oblique", 8) if 'Arial-Oblique' in pdfmetrics.getRegisteredFontNames() else doc.setFont("Helvetica-Oblique", 8)
    doc.drawCentredString(width/2, 1*cm, 
        f"Документ сгенерирован автоматически {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    
    # Сохраняем PDF
    doc.showPage()
    doc.save()
    
    # Возвращаем PDF как ответ
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f"Справка_{applicant.full_name}_{datetime.now().strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response