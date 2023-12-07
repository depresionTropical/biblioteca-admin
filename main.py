from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from model import handle_db as db
from fastapi.middleware.cors import CORSMiddleware

# instance fastpi class
app= FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# HTML template
template = Jinja2Templates(directory='./view')

@app.get('/', response_class=HTMLResponse)
def root(req : Request):
    return template.TemplateResponse('index.html',{'request':req})

@app.post('/', response_class=HTMLResponse)
def root(req : Request):
    return template.TemplateResponse('index.html',{'request':req})

@app.get('/autor_registro',response_class=HTMLResponse)
def signup(req: Request):
    return template.TemplateResponse('autor_registro.html',{'request':req})
@app.post('/autor_registro',response_class=HTMLResponse)
def signup(req: Request):
    return template.TemplateResponse('autor_registro.html',{'request':req})

@app.get('/libro_registro',response_class=HTMLResponse)
def signup(req: Request):
    return template.TemplateResponse('libro_registro.html',{'request':req})
@app.post('/libro_registro',response_class=HTMLResponse)
def signup(req: Request):
    return template.TemplateResponse('libro_registro.html',{'request':req})

@app.get('/cliente_registro',response_class=HTMLResponse)
def signup(req: Request):
    return template.TemplateResponse('cliente_registro.html',{'request':req})
@app.post('/cliente_registro',response_class=HTMLResponse)
def signup(req: Request):
    return template.TemplateResponse('cliente_registro.html',{'request':req})

@app.get('/prestamo_registro',response_class=HTMLResponse)
def signup(req: Request):
    return template.TemplateResponse('prestamo_registro.html',{'request':req})
@app.post('/prestamo_registro',response_class=HTMLResponse)
def signup(req: Request):
    return template.TemplateResponse('prestamo_registro.html',{'request':req})

@app.get('/devolucion_registro',response_class=HTMLResponse)
def signup(req: Request):
    return template.TemplateResponse('devolucion_registro.html',{'request':req})
@app.post('/devolucion_registro',response_class=HTMLResponse)
def signup(req: Request):
    return template.TemplateResponse('devolucion_registro.html',{'request':req})

@app.get('/user',response_class=HTMLResponse)
def signup(req: Request):
    return template.TemplateResponse('user.html',{'request':req})


# post

@app.post('/insert-author')
def insert_author(
    nombre:str=Form(),
    apellido:str=Form(),
    nacionalidad:str=Form()
):
    data_author={
    'nombre':nombre,
    'apellido':apellido,
    'nacionalidad':nacionalidad
    }
    database = db.Autor().insert(data_author)
    print(nombre,apellido,nacionalidad)
    return RedirectResponse('/')

@app.post('/insert-client')
def insert_author(
    nombre:str=Form(),
    apellido:str=Form(),
    fecha_alta:str=Form()
):
    data_client={
    'nombre':nombre,
    'apellido':apellido,
    'fecha_alta':fecha_alta
    }
    database = db.Cliente().insert(data_client)
    print(type(data_client['fecha_alta']))
    return RedirectResponse('/cliente_registro')

@app.post('/insert-book')
def insert_author(
    titulo:str=Form(),
    autor:int=Form(),
    fecha_publicacion:str=Form()
):
    data_book={
    'titulo':titulo,
    'idAutor':autor,
    'fecha_publicacion':fecha_publicacion
    }
    database = db.Libro().insert(data_book)
    #print(type(data_client['fecha_alta']))
    #print(data_book['fecha_publicacion'])
    return RedirectResponse('/libro_registro')

@app.post('/insert-press')
def insert_press(
    libro:int=Form(),
    cliente:int=Form(),
    fecha_prestamo:str=Form()
):
    data_press={
    'libro':libro,
    'cliente':cliente,
    'fecha_prestamo':fecha_prestamo
    }
    database = db.Prestamo().insert(data_press)
    #print(type(data_client['fecha_alta']))
    #print(data_press['fecha_prestamo'])
    return RedirectResponse('/prestamo_registro')

# get autor

@app.get('/get-author')
def get_author():
    database = db.Autor().get_all()
    #print(type(database))
    return database

@app.get('/get-client')
def get_client():
    database = db.Cliente().get_all()
    #print(type(database))
    return database

@app.get('/get-book')
def get_book():
    database = db.Libro().get_all()
    #print(type(database))
    return database


@app.get('/get-press-table')
def get_book():
    #database = db.Prestamo().get_all()
    #print(type(database))
    # return database
    prestamos = db.Prestamo().get_all()
    formatted_prestamos = [
        {
            'Libro': prestamo[1],
            'Cliente': prestamo[0],
            'Fecha de Préstamo': prestamo[2]
        }
        for prestamo in prestamos
    ]
    print(prestamos)
    return formatted_prestamos


@app.get('/get-client-not-devolved')
def get_client():
    database = db.Cliente().get_all()
    #print(type(database))
    return database

@app.get('/get-client-not-devolved')
def get_book():
    database = db.Libro().get_all()
    #print(type(database))
    return database


@app.put("/return")
def update_return(libro:str,cliente:str,fecha_devolucion:str, req:Request):
    # Aquí debes tener la lógica para actualizar la devolución en tu base de datos
    # return_id es el ID del préstamo que se va a actualizar
    # return_data contiene los datos actualizados de la devolución

    # Código para actualizar la devolución en la base de datos
    database = db.Prestamo().update_status(libro,cliente,fecha_devolucion)
    print(f"libro { libro}  cliente {cliente} fecha {fecha_devolucion}")
    
    return {"message": f"Devolución con ID {libro} actualizada"}

# Controlador para manejar solicitudes POST a /insert-return
@app.get('/return',response_class=HTMLResponse)
def signup(req: Request):
    print("-----------------------------")
    print(f"libro { req.query_params['libro']}  cliente {req.query_params['cliente']} fecha {req.query_params['fecha_devolucion']}")
    db.Prestamo().update_status(req.query_params['libro'],req.query_params['cliente'],req.query_params['fecha_devolucion'])
    return template.TemplateResponse('/devolucion_registro.html',{'request':req})

    

