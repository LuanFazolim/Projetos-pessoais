from fasthtml.common import Div, H1, P, Form, Input, Button, Ul, Li, A

def gerar_titulo(titulo, subtitulo):
    return Div(
        H1(titulo),
        P(subtitulo),
        P("Foi gerado")
    )

def gerar_formulario():
    fomulario = Form(
        Input(type= 'text', name='tarefa', placeholder = 'insira a tarefa'),
        Button('Enviar'),
        method = 'post',
        action='/add_tarefa',
        hx_post = '/add_tarefa',
        hx_target='#lista-tarefas',
        hx_swap='outerHTML'
    )
    return fomulario

def gerar_lista_tarefas(lista_tarefas):

    itens_lista = [Li(tarefa, '-', A('Excluir',hx_get=f'/deletar/{i}',
                                     hx_target='#lista-tarefas',
                                     hx_swap='outerHTML')) for i,tarefa in enumerate (lista_tarefas)]

    lista = Ul(
        *itens_lista, id= 'lista-tarefas'
    )
    return lista


