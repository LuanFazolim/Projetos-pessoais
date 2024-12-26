


from fasthtml.common import fast_app, serve, Titled, RedirectResponse
from componentes import gerar_formulario,gerar_lista_tarefas


app, routes = fast_app()
lista_tarefas = []

@routes("/")
def homepage():
    formulario = gerar_formulario()
    print(lista_tarefas)
    elemento_lista_tarefas =  gerar_lista_tarefas(lista_tarefas)
    return Titled("Lista", formulario, elemento_lista_tarefas)

@routes ('/add_tarefa', methods= ['post'])
def adicionar_tarefas(tarefa: str):
    if tarefa:
        lista_tarefas.append(tarefa)
    return gerar_lista_tarefas(lista_tarefas)



@routes('/deletar/{poc}')
def deletar(poc:int):
    if len(lista_tarefas)> poc:
        lista_tarefas.pop(poc)
    return gerar_lista_tarefas(lista_tarefas)

serve()