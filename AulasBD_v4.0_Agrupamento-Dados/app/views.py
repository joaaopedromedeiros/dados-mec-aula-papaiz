from django.shortcuts import render
import pyodbc
from .util_conexao import *

def home(request):
    template = 'home.html'
    return render(request, template)

def campi_por_uf(request):
    template = 'Campi_por_UF.html'
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        sql = """
        SELECT Municipio.uf, COUNT(Campus.id_campus) AS total_campi
        FROM Municipio
        INNER JOIN Campus ON Municipio.id_municipio = Campus.id_municipio
        GROUP BY Municipio.uf
        ORDER BY Municipio.uf;
        """
        cursor.execute(sql)
        dados_campi = cursor.fetchall()  # Lista de tuplas: [(uf, total_campi), ...]

        return render(request, template, context={'dados_campi': dados_campi})

    except Exception as err:
        return render(request, template, context={'ERRO': err})

def curso_por_area(request):
    template = 'Curso_por_area.html'
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        sql = """
        SELECT area.descricao AS area,
               COUNT(curso.id_curso) AS quantidade_cursos
        FROM Cursos_Oferecidos_por_Campus as cursos_oferecidos
        INNER JOIN Area as area 
               ON cursos_oferecidos.id_area = area.id_area
        INNER JOIN Curso curso 
               ON cursos_oferecidos.id_curso = curso.id_curso
        GROUP BY area.descricao
        ORDER BY area.descricao;
        """
        cursor.execute(sql)
        dados_area = cursor.fetchall()  # [(area, quantidade_cursos), ...]

        # Transformando em lista de dicionários
        dados_area_dict = [{'area': area, 'quantidade_cursos': quantidade} for area, quantidade in dados_area]

        return render(request, template, context={'dados_area': dados_area_dict})

    except Exception as err:
        return render(request, template, context={'ERRO': err})


def ranking_dos_cursos_por_uf(request):
    template = 'Ranking_dos_cursos_por_UF.html'
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        sql = """
        WITH CursosPorUF AS (
            SELECT  
                Curso.nome, 
                Municipio.uf AS estado,
                COUNT(*) AS ofertas,
                MIN(Cursos_Oferecidos_por_Campus.enade) AS enade_min,
                MAX(Cursos_Oferecidos_por_Campus.enade) AS enade_max,
                CAST(AVG(Cursos_Oferecidos_por_Campus.enade) AS DECIMAL(5,2)) AS enade_media,
                ROW_NUMBER() OVER(PARTITION BY Municipio.uf ORDER BY COUNT(*) DESC) AS rn
            FROM Cursos_Oferecidos_por_Campus
            INNER JOIN Curso ON Cursos_Oferecidos_por_Campus.id_curso = Curso.id_curso
            INNER JOIN Campus ON Cursos_Oferecidos_por_Campus.id_campus = Campus.id_campus
            INNER JOIN Municipio ON Campus.id_municipio = Municipio.id_municipio 
            GROUP BY Curso.nome, Municipio.uf
            HAVING AVG(Cursos_Oferecidos_por_Campus.enade) > 2.5
        )
        SELECT *
        FROM CursosPorUF
        WHERE rn <= 10
        ORDER BY estado ASC, ofertas DESC;
        """
        cursor.execute(sql)
        ranking_uf = cursor.fetchall()  # [(nome, estado, ofertas, enade_min, enade_max, enade_media, rn), ...]

        return render(request, template, context={'ranking_uf': ranking_uf})

    except Exception as err:
        return render(request, template, context={'ERRO': err})

def ranking_por_municipio(request):
    template = 'Ranking_por_Municipio.html'
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        sql = """
        SELECT TOP(15) 
            Municipio.nome, 
            Municipio.uf, 
            COUNT(Campus.id_campus) AS total_campus
        FROM Municipio
        INNER JOIN Campus ON Municipio.id_municipio = Campus.id_municipio
        GROUP BY Municipio.nome, Municipio.uf
        ORDER BY total_campus DESC;
        """
        cursor.execute(sql)
        ranking_municipio = cursor.fetchall()  # Lista de tuplas: [(nome, uf, total_campus), ...]

        return render(request, template, context={'ranking_municipio': ranking_municipio})

    except Exception as err:
        return render(request, template, context={'ERRO': err})


def dados_gerais(request):
    template = 'dados_gerais.html'
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        count_ies = cursor.execute('SELECT count(*) FROM IES').fetchval()
        count_campus = cursor.execute('SELECT count(*) FROM campus').fetchval()
        count_cursos = cursor.execute('SELECT count(*) FROM curso').fetchval()
        count_ofertas = cursor.execute('SELECT count(*) FROM cursos_oferecidos_por_campus').fetchval()
        count_areas = cursor.execute('SELECT count(*) FROM area').fetchval()

        return render(request, template, context={
            'count_ies': count_ies,
            'count_campus': count_campus,
            'count_cursos': count_cursos,
            'count_ofertas': count_ofertas,
            'count_areas': count_areas,
        })

    except Exception as err:
        return render(request, template, context={'ERRO': err})
