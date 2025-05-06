from django.db import models

# Create your models here.

class Matricula(models.Model):
    estado = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    ies = models.CharField(max_length=255, blank=True, null=True)
    sigla = models.CharField(max_length=50, blank=True, null=True)
    organizacao = models.CharField(max_length=100, blank=True, null=True)
    categoria_administrativa = models.CharField(max_length=100, blank=True, null=True)
    nome_curso = models.CharField(max_length=255, blank=True, null=True)
    nome_detalhado_curso = models.CharField(max_length=255, blank=True, null=True)
    modalidade = models.CharField(max_length=50, blank=True, null=True)
    grau = models.CharField(max_length=100, blank=True, null=True)
    matriculas_2014 = models.IntegerField(blank=True, null=True)
    matriculas_2015 = models.IntegerField(blank=True, null=True)
    matriculas_2016 = models.IntegerField(blank=True, null=True)
    matriculas_2017 = models.IntegerField(blank=True, null=True)
    matriculas_2018 = models.IntegerField(blank=True, null=True)
    matriculas_2019 = models.IntegerField(blank=True, null=True)
    matriculas_2020 = models.IntegerField(blank=True, null=True)
    matriculas_2021 = models.IntegerField(blank=True, null=True)
    matriculas_2022 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False 
        db_table = 'matriculas'
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        
    def __str__(self):
        return f"{self.nome_curso or 'Sem nome'} - {self.ies or 'Sem IES'} ({self.cidade or 'Sem cidade'}/{self.estado or 'Sem estado'})"
