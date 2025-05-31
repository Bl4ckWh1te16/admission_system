from django.db import models
from django.urls import reverse

class EducationProgram(models.Model):
    STUDY_LEVELS = [
        ('bachelor', 'Бакалавриат'),
        ('master', 'Магистратура'),
        ('specialist', 'Специалитет'),
        ('phd', 'Аспирантура'),
    ]
    
    name = models.CharField(
        "Название программы", 
        max_length=255,
        help_text="Полное название программы, например: 'Компьютерные науки'"
    )
    code = models.CharField(
        "Код программы", 
        max_length=20,
        help_text="Код по ФГОС, например: 09.03.01"
    )
    level = models.CharField(
        "Уровень образования",
        max_length=20,
        choices=STUDY_LEVELS,
        default='bachelor'
    )
    description = models.TextField(
        "Описание программы",
        help_text="Подробное описание программы обучения"
    )
    duration = models.PositiveSmallIntegerField(
        "Срок обучения (лет)",
        default=4
    )
    budget_places = models.PositiveIntegerField(
        "Количество бюджетных мест",
        default=0
    )
    paid_places = models.PositiveIntegerField(
        "Количество платных мест", 
        default=0
    )
    tuition_fee = models.DecimalField(
        "Стоимость обучения (в год)", 
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        "Дата создания", 
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Дата обновления", 
        auto_now=True
    )

    def __str__(self):
        return f"{self.code} - {self.name} ({self.get_level_display()})"

    class Meta:
        verbose_name = "Образовательная программа"
        verbose_name_plural = "Образовательные программы"
        ordering = ['code', 'name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        verbose_name = "Образовательная программа"
        verbose_name_plural = "Образовательные программы"

class Applicant(models.Model):
    GENDER_CHOICES = [('M', 'Мужской'), ('F', 'Женский')]
    
    full_name = models.CharField("ФИО", max_length=255)
    birth_date = models.DateField("Дата рождения")
    gender = models.CharField("Пол", max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email")
    address = models.TextField("Адрес")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Абитуриент"
        verbose_name_plural = "Абитуриенты"
        ordering = ['-created_at']

class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_review', 'На рассмотрении'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
    ]
    
    applicant = models.ForeignKey(
        Applicant, 
        on_delete=models.CASCADE, 
        verbose_name="Абитуриент"
    )
    program = models.ForeignKey(
        EducationProgram, 
        on_delete=models.CASCADE, 
        verbose_name="Программа"
    )
    status = models.CharField(
        "Статус", 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='new'
    )
    application_date = models.DateTimeField(
        "Дата подачи", 
        auto_now_add=True
    )
    exam_results = models.JSONField(
        "Результаты экзаменов", 
        default=dict,
        blank=True
    )
    
    def __str__(self):
        return f"Заявление #{self.id} - {self.applicant}"
    
    def get_absolute_url(self):
        return reverse('application_detail', args=[str(self.id)])
    
    class Meta:
        verbose_name = "Заявление"
        verbose_name_plural = "Заявления"
        ordering = ['-application_date']