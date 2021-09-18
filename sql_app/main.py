# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:25:17 2020

@author: Marcelo
"""

from typing import List, Union

from fastapi import Depends, FastAPI, HTTPException, status, Response, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from datetime import timedelta, date, datetime
from typing import Optional
from jose import JWTError
from . import crud, models, schemas, app_utils, secrets, GCP_functions
#from . import GCP_functions
from .database import SessionLocal, engine
import pandas as pd
import io
import os
import json
from google.oauth2 import service_account
from google.cloud import storage
import asyncio
from twilio.twiml.messaging_response import MessagingResponse
#import zipfile
#import StringIO

##################################  security ############################################
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
with open('GCP_secrets/data-science-proj-280908-e7130591b0d5.json') as source:
    info = json.load(source)
    project_id = 'data-science-proj-280908'
storage_credentials = service_account.Credentials.from_service_account_info(info)
storage_client = storage.Client(project=project_id, credentials=storage_credentials)

#########################################################################################


################################# SQL engine ############################################
models.Base.metadata.create_all(bind=engine)

####################################  DOCS TAGS and DESCRIPTION #######################################################
tags_metadata = [
    {
         "name": "Users",
         "description":"Operations with Users. Also login logic",
    },
    {
         "name": "Clients",
         "description":"Operations with Clients.",
     },
    {
         "name": "Operarios",
         "description":"Operations with Operators.",
     },
    {
         "name": "Fincas",
         "description":"Operations with Farms/Fincas.",
     },
    {
         "name": "Lotes",
         "description":"Operations with Terrains/Lotes.",
     },
    {
         "name": "Actividades-Lotes",
         "description":"Operations related to works on Farms/Fincas Terrains/Lotes.",
     },
    {
         "name": "Hatos",
         "description":"Operations with Herds / Hatos.",
     },
    {
         "name": "Vacas",
         "description":"Operations with Cows/Vacas.",
     },
    {
         "name": "Actividades-Vacas",
         "description":"Operations related to works on Cows/Vacas.",
     },
    {
         "name": "Leche",
         "description":"Operations with Milk/Leche.",
     },
    {
         "name": "Otras Fuentes Lotes",
         "description":"Operations related to terrain properties and characteristics.",
     },
        {
         "name": "Monitoreo Descargas satelitales",
         "description":"Operations related to satellite image download monitoring.",
     },
    {
         "name": "Estacion Meteorologica",
         "description":"Operations with Meteo-station / IoT.",
     },
    {
         "name": "Stream Images",
         "description":"Streaming de imagenes satelitales / Remote Sensing.",
     },
    
    ]

# APP
app = FastAPI(
    title="My Kau API project",
    description= "This is the API for connecting MySQL 8.0 DB to the APP, Dashboard and other front ends",
    version="0.0.2",
    openapi_tags=tags_metadata
    )
################################  CORS   ######################################################
app.add_middleware(
    CORSMiddleware,
    #allow_origins=secrets.origins,
    allow_origin_regex='https?://.*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

##############################################################################################


############################## Functions   #####################################################
### Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### OATH
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = app_utils.decode_access_token(data=token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(user=username)
    except JWTError:  # PyJWTError:
        raise credentials_exception
    tk_user = crud.get_user(db, username=token_data.user)
    if tk_user is None:
        raise credentials_exception
    return tk_user

### Current user active status
async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.active_status != 1:  # 0=inactive, 1=active
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

######################################################################################


#######################     USERS   ###################################################
@app.post("/user", response_model=schemas.UserInfo, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user=user.user)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    #send email to cliente mail
    return crud.create_user(db=db, user_t=user)

@app.post("/token", response_model=schemas.Token, tags=["Users"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=app_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = app_utils.create_access_token(
        data={"sub": user.user}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.patch("/User_upd/{USERNAME}", response_model=schemas.UserInfo2, tags=["Users"])
def update_user_status(USERNAME: str, user_t: schemas.User, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.update_user(db=db, user_t=user_t, username=USERNAME)
    db_user_id = crud.get_user_by_username(db, user=USERNAME)
    if db_user_id is None:
        raise HTTPException(status_code=404, detail="Username not found")
    return db_user_id

#missing to update password

@app.get("/Users_all/", response_model=List[schemas.UserInfo2], tags=["Users"]) 
def read_users(db: Session = Depends(get_db), full_name: Optional[str]=None, email: Optional[str]=None, active_status: Optional[int]=None,  user_rol: Optional[int]=None, operario: Optional[int]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    usuarios = crud.get_all_users(db, full_name=full_name, email=email, active_status=active_status,  user_rol=user_rol, operario=operario, id_cliente= current_user.ID_CLIENTE)
    return usuarios
#deberia haber una forma de mostrar todos asi no sean del cliente, para asignar


@app.get("/User_priv/", response_model=List[schemas.API_Users_PrivT], tags=["Users"])
def read_users_priv(db: Session = Depends(get_db), name: Optional[str]=None, description: Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    privilegios = crud.get_all_privs(db, name=name, description=description)
    return privilegios

### Permisions
@app.get("/Permisos/", response_model=List[schemas.PermisosT], tags=["Users"])
def read_permisos(db: Session = Depends(get_db), name: Optional[str]=None, user: Optional[int]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    permisos = crud.get_permisos(db, name=name, user=user, id_cliente = current_user.ID_CLIENTE)
    return permisos

@app.patch("/Permisos/{User_ID}", response_model=List[schemas.PermisosT], tags=["Users"])
def update_permisos(User_ID: int, permiso: schemas.PermisosU, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.update_permiso(db=db, permiso=permiso, user_id=User_ID)
    db_permiso_id = crud.get_permisos(db, user=User_ID, id_cliente = current_user.ID_CLIENTE)
    if db_permiso_id is None:
        raise HTTPException(status_code=404, detail="User_ID not found")
    return db_permiso_id

###################################################################################################


############################       CLIENTS      ###############################################
@app.get("/clientes/", response_model=List[schemas.ClientesT], tags=["Clients"])  
def read_clientes(db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user), ciudad:Optional[str]=None, departamento:Optional[str]=None, nombre:Optional[str]=None, date1: Optional[str]=None, id_cliente: Optional[str]=None):
    clientes = crud.get_clientes(db, ciudad=ciudad, departamento=departamento, nombre=nombre, date1= date1, id_cliente=id_cliente)
    return clientes

@app.post("/Cliente/", status_code=201, tags=["Clients"])
async def write_cliente(cliente: schemas.ClientesCreate, db: Session = Depends(get_db)): #, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_cliente(db=db, cliente=cliente)
    #esto seria bueno asociarlo con enviar un email, con formulario y que el ID de cliente se guarde
    #para asignarlo al usuario creado

#editar cliente
@app.patch("/Cliente/{ID_CLIENTE}", response_model=List[schemas.ClientesT], tags=["Clients"])
def update_cliente(Cliente_ID: int, cliente: schemas.ClientesU, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.update_cliente(db=db, cliente=cliente, cliente_id=Cliente_ID)
    db_cliente_id = crud.get_clientes(db, id_cliente = Cliente_ID)
    if db_cliente_id is None:
        raise HTTPException(status_code=404, detail="ID_CLIENTE not found")
    return db_cliente_id
#falta otra tabla sobre estado clientes, pagos y vencimientos, separada de tabla cliente
#[tambien agregar fecha inicial contrato, fecha_vencimiento, estado
####################################################################################################


##################################      OPERARIOS    #################################################
@app.get("/Operario", response_model=List[schemas.OperarioT], tags=["Operarios"])  # List[
def read_operarios(db: Session = Depends(get_db), finca:Optional[str]=None, id_operario:Optional[str]=None, rol:Optional[str]=None, nombre:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    operarios = crud.get_operarios(db, finca=finca, id_operario=id_operario, rol=rol, nombre=nombre, id_cliente = current_user.ID_CLIENTE)
    return operarios

@app.post("/create_operario/", status_code=201, tags=["Operarios"])
def write_operario(operario: schemas.OperarioN, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_operario(db=db, operario=operario)
'''
@app.delete("/Operario_del/{ID_OPERARIO}", tags=["Operarios"])
def erase_operario(ID_OPERARIO: int, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.delete_operario(db, id_operario=ID_OPERARIO)  # operario = operario,
    db_operario_id = crud.get_oper_by_id(db, id_operario=ID_OPERARIO)
    if db_operario_id is not None:
        raise HTTPException(status_code=404, detail="Operario_ID not deleted")
    return {
        "status": True,
        "message": "User deleted"
    }
'''
@app.get("/Operario_sin_user", response_model=List[schemas.Operario_Sin_UserT], tags=["Operarios"])  # List[
def read_oper_sin_user(db: Session = Depends(get_db), nombre:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    operarios = crud.get_oper_sin_user(db, nombre=nombre, id_cliente = current_user.ID_CLIENTE)
    return operarios

#patch operario
@app.patch("/Operario/{ID_OPERARIO}", response_model=List[schemas.OperarioT], tags=["Operarios"])
def update_operario(Operario_ID: int, operario: schemas.OperarioN, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.update_operario(db=db, operario=operario, id_operario=Operario_ID)
    db_operario_id = crud.get_operarios(db, id_operario=Operario_ID, id_cliente = current_user.ID_CLIENTE)
    if db_operario_id is None:
        raise HTTPException(status_code=404, detail="ID_OPERARIO not found")
    return db_operario_id

##########################################################################################################


#################################     FINCAS     #########################################################
@app.get("/Fincas/", response_model=List[schemas.FincaT], tags=["Fincas"])
def read_fincas(db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user), finca:Optional[int]=None, nombre:Optional[str]=None):
    fincas = crud.get_fincas(db, finca=finca, id_cliente = current_user.ID_CLIENTE, nombre=nombre)
    return fincas

@app.get("/Fincas_small/", response_model=List[schemas.FincaR], tags=["Fincas"])
def read_fincass(db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user), finca:Optional[int]=None, nombre:Optional[str]=None):
    fincas = crud.get_fincas(db, finca=finca, id_cliente = current_user.ID_CLIENTE, nombre=nombre)
    return fincas

@app.post("/create_finca/", status_code=201, tags=["Fincas"]) #response_model=schemas.Leche_Hatosi)
def wr_finca(finca: schemas.FincaP, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_finca(db=db, finca=finca, id_cliente= current_user.ID_CLIENTE)
#solo funciona si tabla lotes tiene finca_id creada ... cambiar SQL, sino se puede, APP debera crear finca y lote al tiempo
#obteniendo max finca_id, asignando en tabla lotes y despues en tabla fincas

#patch finca
@app.patch("/Fincas/{ID_FINCA}", response_model=List[schemas.FincaT], tags=["Fincas"])
def update_finca(Finca_ID: int, finca: schemas.FincaU, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.update_finca(db=db, finca=finca, id_finca=Finca_ID)
    db_finca_id = crud.get_fincas(db, finca=Finca_ID, id_cliente = current_user.ID_CLIENTE)
    if db_finca_id is None:
        raise HTTPException(status_code=404, detail="ID_FINCA not found")
    return db_finca_id
###########################################################################################################


###########################################    LOTES    ###################################################
@app.post("/Fincas/{finca_id}/Lotes/", status_code=201, tags=["Lotes"])
def write_lote_for_finca(finca_id: int, lote: schemas.LotesN, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_finca_lote(db=db, lote=lote, finca_id=finca_id) #, id_cliente= current_user.ID_CLIENTE)

@app.get("/Lotes/", response_model=List[schemas.LotesT], tags=["Lotes"])
def read_lotes(db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user), id_finca:Optional[int]=None, id_lote:Optional[int]=None, nombre:Optional[str]=None):
    lotes = crud.get_lotes(db, id_finca=id_finca, id_lote=id_lote, nombre=nombre, id_cliente = current_user.ID_CLIENTE)
    return lotes
'''
@app.delete("/Lotes_del/{ID_LOTE}", tags=["Lotes"])
def erase_lote(ID_LOTE: int, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.delete_lote(db, id_lote=ID_LOTE)  # operario = operario,
    db_lote_id = crud.get_lotes(db, id_lote=ID_LOTE, id_cliente = current_user.ID_CLIENTE)
    if db_lote_id is not None:
        raise HTTPException(status_code=404, detail="Lote_ID not deleted")
    return {
        "status": True,
        "message": "Lote deleted"
    }
'''
@app.patch("/Lotes_upd/{ID_LOTE}", response_model=List[schemas.LotesT], tags=["Lotes"])
def update_lotes_id(ID_LOTE: int, lote: schemas.LotesN, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    #primero ver si el lote si pertenece al cliente, luego cambiar
    crud.update_lote(db=db, lote=lote, id_lote=ID_LOTE)
    db_lote_id = crud.get_lotes(db, id_lote=ID_LOTE, id_cliente = current_user.ID_CLIENTE)
    if db_lote_id is None:
        raise HTTPException(status_code=404, detail="Lote_ID not found")
    return db_lote_id

###########################################################################################################


#########################################  ACTIVIDADES LOTES  ############################################
@app.get("/Acti_Lotes/", response_model=List[schemas.Actividades_LotesT], tags=["Actividades-Lotes"])
def read_acti_lotes(db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user), id_finca:Optional[int]=None, id_lote:Optional[int]=None, nombre_lote:Optional[str]=None, nombre_oper:Optional[str]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d")):
    acti_lotes = crud.get_acti_lotes(db, id_finca=id_finca, id_lote=id_lote, nombre_lote=nombre_lote, nombre_oper=nombre_oper, date1=date1, date2=date2, id_cliente = current_user.ID_CLIENTE)
    return acti_lotes

@app.post("/Wr_Acti_Lotes/", status_code=201, tags=["Actividades-Lotes"]) #response_model=schemas.Leche_Hatosi)
def wr_acti_lotes(ac_lo: schemas.Acti_lotes_post, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_acti_lotes(db=db, ac_lo=ac_lo)

@app.post("/Wr_Acti_Aforo/", status_code=201, tags=["Actividades-Lotes"]) #response_model=schemas.Leche_Hatosi)
def wr_acti_aforo(ac_fo: schemas.Aforo_Requi, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    id_to_use = crud.create_acti_lotes2(db=db, ac_fo=ac_fo)
    id_to_use
    id_to_use = id_to_use.ID_ACT_LOTE
    return crud.create_acti_aforo(db=db, ac_fo=ac_fo, id_to_use=id_to_use)

@app.get("/Tipo_Acti_Lotes/", response_model=List[schemas.Tipo_Actividades_LotesT], tags=["Actividades-Lotes"])
def read_tip_acti_lotes(db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    tipo_acti_lotes = crud.get_tipo_acti_lotes(db)
    return tipo_acti_lotes

###########################################################################################################


########################################    HATOS     ####################################################
@app.get("/Hatos/", response_model=List[schemas.HatosT], tags=["Hatos"])
def read_hatos(db: Session = Depends(get_db), id_finca:Optional[int]=None, id_hato:Optional[int]=None, nombre:Optional[str]=None, tipo:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    hatos = crud.get_hatos(db, id_finca=id_finca, id_hato=id_hato, nombre=nombre, tipo=tipo, id_cliente = current_user.ID_CLIENTE)
    return hatos

@app.get("/Hatos_small/", response_model=List[schemas.HatosR], tags=["Hatos"])
def read_hatoss(db: Session = Depends(get_db), id_finca:Optional[int]=None, id_hato:Optional[int]=None, nombre:Optional[str]=None, tipo:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    hatos = crud.get_hatos(db, id_finca=id_finca, id_hato=id_hato, nombre=nombre, id_cliente = current_user.ID_CLIENTE)
    return hatos

@app.post("/create_hato/", status_code=201, tags=["Hatos"]) #response_model=schemas.Leche_Hatosi)
def wr_hato(hato: schemas.HatosP, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_hato(db=db, hato=hato, id_cliente= current_user.ID_CLIENTE)
#funciona, pero duplica ID_hato, sino se puede corregir SQL, entonces hacer get max ID y crear con +1

#Patch Hato
@app.patch("/Hatos/{ID_HATO}", response_model=List[schemas.HatosT], tags=["Hatos"])
def update_hato(Hato_ID: int, hato: schemas.HatosP, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.update_hato(db=db, hato=hato, id_hato=Hato_ID)
    db_hato_id = crud.get_hatos(db, id_hato=Hato_ID, id_cliente = current_user.ID_CLIENTE)
    if db_hato_id is None:
        raise HTTPException(status_code=404, detail="ID_HATO not found")
    return db_hato_id


@app.get("/TrasHatos/", response_model=List[schemas.Traslado_HatosT], tags=["Hatos"])
async def read_hist_trashatos(db: Session = Depends(get_db), id_hato:Optional[str]=None, id_lote:Optional[str]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"),current_user: schemas.UserInfo = Depends(get_current_active_user)): #skip: int = 0, limit: int = 100,
    hist_trashatos = crud.get_trashato(db, id_hato=id_hato, id_lote=id_lote, date1=date1, date2=date2, id_cliente = current_user.ID_CLIENTE)# skip=skip, limit=limit)
    return hist_trashatos

@app.post("/Traslado_hato/", status_code=201, tags=["Hatos"])
async def tras_ubica_hatos(sch_ubi: schemas.Ubicacion_VacasBasic, db: Session = Depends(get_db), Fecha_Traslado : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    #actualizar datos de ubicacion
    updated = crud.update_ubica_hato(db=db, sch_ubi=sch_ubi, id_cliente= current_user.ID_CLIENTE)
    if updated == 'ok':
        #si la ubicacion ya existia y se actualizo, entonces escribir nuevo traslado id
        db_tras_hato = crud.write_trashato(db=db, sch_ubi=sch_ubi, Fecha_Traslado=Fecha_Traslado, id_cliente = current_user.ID_CLIENTE)
        if db_tras_hato is None: #si el traslado de vaca no se registro, mostrar error
            raise HTTPException(status_code=404, detail="Traslado no registrado")
            ## si funciono, crear loop para trasladar todas las vacas de un lote al otro
    
    #si la ubicacion no existia, entonces escribir nueva ubicacion y nuevo traslado
    else: #toca restringir vacas, lotes y hatos desde la APP con seleccion, no texto
        #falta ajustar write de ubicacion con varias vacas
        crud.write_ubi_vaca(db=db, sch_ubi=sch_ubi, id_cliente=current_user.ID_CLIENTE)
        db_tras_hato = crud.write_trashato(db=db, sch_ubi=sch_ubi, Fecha_Traslado=Fecha_Traslado, id_cliente = current_user.ID_CLIENTE)
        if db_tras_hato is None: #si el traslado de vaca no se registro, mostrar error
            raise HTTPException(status_code=404, detail="Traslado no registrado")
    return db_tras_hato

#patch traslado hatos

###########################################################################################################


#############################################   VACAS    #################################################
@app.get("/Vacas/", response_model=List[schemas.VacasT], tags=["Vacas"])
async def read_vacas(db: Session = Depends(get_db), id_vaca:Optional[int]=None, nombre:Optional[str]=None, sexo:Optional[int]=None, raza:Optional[int]=None, activa:int=1, current_user: schemas.UserInfo = Depends(get_current_active_user)): #id_finca:Optional[int]=None
    vacas = crud.get_vacas(db, id_vaca=id_vaca, nombre=nombre, sexo=sexo, raza=raza, activa=activa, id_cliente = current_user.ID_CLIENTE) #id_finca=id_finca
    return vacas

@app.get("/Vacas_small/", response_model=List[schemas.VacasR], tags=["Vacas"])
async def read_vacass(db: Session = Depends(get_db), id_vaca:Optional[int]=None, nombre:Optional[str]=None, sexo:Optional[int]=None, raza:Optional[int]=None, activa:int=1, current_user: schemas.UserInfo = Depends(get_current_active_user)):  #id_finca:Optional[int]=None
    vacas = crud.get_vacas(db,  id_vaca=id_vaca, nombre=nombre, sexo=sexo, raza=raza, activa=activa, id_cliente = current_user.ID_CLIENTE) #id_finca=id_finca
    return vacas

@app.post("/Wr_Vaca/", status_code=201, tags=["Vacas"])
def create_vaca(wr_va: schemas.VacaN, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_vaca(db=db, wr_va=wr_va, id_cliente = current_user.ID_CLIENTE)

@app.patch("/Vacas_upd/{ID_VACA}", response_model=List[schemas.VacasT], tags=["Vacas"])
def update_vacas_id(ID_VACA: int, vaca: schemas.VacaN, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.update_vaca(db=db, vaca=vaca, id_vaca=ID_VACA)
    db_vaca_id = crud.get_vacas(db, id_vaca=ID_VACA, id_cliente = current_user.ID_CLIENTE)
    if db_vaca_id is None:
        raise HTTPException(status_code=404, detail="Vaca_ID not found")       
    return db_vaca_id

@app.get("/Raza/", response_model=List[schemas.razaT], tags=["Vacas"])
async def read_raza(db: Session = Depends(get_db), id_raza:Optional[int]=None, nombre:Optional[str]=None, codigo:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    raza = crud.get_razas(db, id_raza=id_raza, nombre=nombre, codigo=codigo) #, id_cliente = current_user.ID_CLIENTE
    return raza

@app.get("/Raza_small/", response_model=List[schemas.razaR], tags=["Vacas"])
async def read_razas(db: Session = Depends(get_db), id_raza:Optional[int]=None, nombre:Optional[str]=None, codigo:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)): 
    raza = crud.get_razas(db, id_raza=id_raza, nombre=nombre, codigo=codigo) #id_cliente = current_user.ID_CLIENTE
    return raza

@app.get("/Sexo/", response_model=List[schemas.sexoT], tags=["Vacas"])
async def read_sexo(db: Session = Depends(get_db), id_sexo:Optional[int]=None, nombre:Optional[str]=None, codigo:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)): 
    sexo = crud.get_sexo(db, id_sexo=id_sexo, nombre=nombre, codigo=codigo) #, id_cliente = current_user.ID_CLIENTE
    return sexo

@app.get("/Tip_Dest/", response_model=List[schemas.tipo_destinoT], tags=["Vacas"])
async def read_dest(db: Session = Depends(get_db), id_destino:Optional[int]=None, nombre:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    tip_dest = crud.get_t_destino(db, id_destino=id_destino, nombre=nombre) #, id_cliente = current_user.ID_CLIENTE
    return tip_dest

@app.get("/Sires/", response_model=List[schemas.siresT], tags=["Vacas"])
async def read_sires(db: Session = Depends(get_db), id_sire:Optional[int]=None, id_oficial:Optional[str]=None, nombre_largo:Optional[str]=None, registro:Optional[str]=None, raza:Optional[int]=None, activa:Optional[int]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)): #id_finca:Optional[int]=None
    sires = crud.get_sires(db, id_sire=id_sire, id_oficial=id_oficial, nombre_largo=nombre_largo, registro=registro, raza=raza, activa=activa, id_cliente = current_user.ID_CLIENTE) #id_finca=id_finca
    return sires

#post sire

#patch sire

#########################################################################################################


###########################################   ACTIVIDADES VACAS   #########################################
@app.get("/Tip_Oper/", response_model=List[schemas.tipo_operacionesT], tags=["Actividades-Vacas"])
async def read_tip_oper(db: Session = Depends(get_db), id_tipo:Optional[int]=None, nombre:Optional[str]=None, codigo:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    tip_oper = crud.get_t_operacion(db, id_tipo=id_tipo, nombre=nombre, codigo=codigo) #, id_cliente = current_user.ID_CLIENTE
    return tip_oper


@app.get("/AV_categ/", response_model=List[schemas.Actividades_vacas_categoriaT], tags=["Actividades-Vacas"])
async def read_av_categ(db: Session = Depends(get_db), id_cat:Optional[int]=None, nombre:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    av_categ = crud.get_av_categoria(db, id_cat=id_cat, nombre=nombre) #, id_cliente = current_user.ID_CLIENTE
    return av_categ

@app.get("/AV_result/", response_model=List[schemas.Actividades_vacas_resultadoT], tags=["Actividades-Vacas"])
async def read_av_result(db: Session = Depends(get_db), id_res:Optional[int]=None, nombre:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    av_res = crud.get_av_resultado(db, id_res=id_res, nombre=nombre) #, id_cliente = current_user.ID_CLIENTE
    return av_res

'''
@app.post("/Mastitis/", response_model=Union[schemas.MastitisT, schemas.ActInfo])
async def write_mastitis(mastitis: schemas.MastitisT, av:schemas.ActInfo, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    id_to_use = crud.reg_actividades_vacas(db=db, av=av)
    id_to_use
    id_to_use = id_to_use.ID_Actividad 
    return crud.registrar_mastitis(db=db, mastitis=mastitis, id_to_use=id_to_use)
'''

@app.post("/Masti_2/", status_code=201, tags=["Actividades-Vacas"])
async def write_masti_2(data: schemas.Mast_Requi, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    id_to_use = crud.reg_acti_2(db=db, data=data)
    id_to_use
    id_to_use = id_to_use.ID_Actividad 
    return crud.registrar_masti_2(db=db, data=data, id_to_use=id_to_use)

@app.get("/ActiVacas/", response_model=List[schemas.ActInfo], tags=["Actividades-Vacas"])
async def read_act_vacas(date1: str='2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), vaca:Optional[str]=None, operacion:Optional[int]=None, operario:Optional[int]=None,db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): #skip: int = 0, limit: int = 100,
    act_vacas = crud.get_act_vacas(db, date1=date1, date2=date2, vaca=vaca, operacion=operacion, operario=operario, id_cliente = current_user.ID_CLIENTE)# skip=skip, limit=limit)
    return act_vacas

'''
@app.get("/Mastit_get/", response_model=List[Union[schemas.MastitisT,schemas.ActInfo]])
async def read_mastitis(date1: str='2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), vaca:Optional[str]=None, operacion:Optional[int]=None, operario:Optional[int]=None,db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): #skip: int = 0, limit: int = 100,
    act_mast = crud.get_act_mastitis(db, date1=date1, date2=date2, vaca=vaca, operacion=operacion, operario=operario, id_cliente = current_user.ID_CLIENTE)
    return act_mast
'''

@app.get("/Mastit_get/", status_code=201, tags=["Actividades-Vacas"])#, response_model=List[schemas.Mast_2])
async def read_mastitis(date1: Optional[str]='2020-01-01', date2: Optional[str] = datetime.now().strftime("%Y-%m-%d"), vaca:Optional[str]=None, operacion:Optional[int]=None, operario:Optional[int]=None, id_mastitis:Optional[int]=None,   db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): #skip: int = 0, limit: int = 100,
    act_mast = crud.get_act_mastitis(db, date1=date1, date2=date2, vaca=vaca, operacion=operacion, operario=operario, id_mastitis=id_mastitis, id_cliente = current_user.ID_CLIENTE)
    return act_mast

#DB View
@app.get("/Last_Mastit/", status_code=201, tags=["Actividades-Vacas"])#, response_model=List[schemas.Mast_2])
async def read_masti_las(vaca:Optional[str]=None, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): #skip: int = 0, limit: int = 100, operario:Optional[int]=None
    act_mast2 = crud.get_last_mastitis(db, vaca=vaca, id_cliente = current_user.ID_CLIENTE) #operario=operario, 
    return act_mast2

#patch mastitis
@app.patch("/Mastitis/{ID_mastitis}", status_code=201, tags=["Actividades-Vacas"])
def update_mastitis(ID_mastitis: int, mastitis: schemas.MastitisU, acts:schemas.ActividadesU, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.update_mastitis(db=db, mastitis=mastitis, acts=acts, id_mastitis=ID_mastitis)
    db_mastitis = crud.get_act_mastitis(db, id_mastitis=ID_mastitis, id_cliente = current_user.ID_CLIENTE)
    if db_mastitis is None:
        raise HTTPException(status_code=404, detail="Mastitis_ID not found")
    return db_mastitis


@app.get("/Partos_act_get/", status_code=201, tags=["Actividades-Vacas"])#, response_model=List[schemas.Mast_2])
async def read_partos(date1: Optional[str]='2020-01-01', date2: Optional[str] = datetime.now().strftime("%Y-%m-%d"), vaca:Optional[str]=None, categoria:Optional[int]=None, operario:Optional[int]=None, comentario:Optional[str]=None,  db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): #skip: int = 0, limit: int = 100,
    act_partos = crud.get_act_partos(db, date1=date1, date2=date2, vaca=vaca, categoria=categoria, operario=operario, comentario=comentario, id_cliente = current_user.ID_CLIENTE)
    return act_partos

@app.get("/solo_partos_get/", response_model=List[schemas.PartosT], tags=["Actividades-Vacas"])#, response_model=List[schemas.Mast_2])
async def read_parto(date1: Optional[str]='2020-01-01', date2: Optional[str] = datetime.now().strftime("%Y-%m-%d"), vaca:Optional[str]=None, idparto:Optional[int]=None, idactividad:Optional[int]=None, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): #skip: int = 0, limit: int = 100,
    partos = crud.get_solo_partos(db, vaca=vaca, idparto=idparto, idactividad=idactividad, id_cliente = current_user.ID_CLIENTE)
    return partos

@app.get("/Max_partos_get/", status_code=201, tags=["Actividades-Vacas"])#, response_model=List[schemas.Mast_2])
async def read_max_parto(vaca:Optional[str]=None, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): #skip: int = 0, limit: int = 100,
    max_partos = crud.get_max_partos(db, vaca=vaca, id_cliente = current_user.ID_CLIENTE)
    return max_partos

@app.post("/Parto_crear/", status_code=201, tags=["Actividades-Vacas"])
async def write_parto(data: schemas.Parto_Requi, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    id_to_use = crud.reg_acti_2(db=db, data=data) #reg_acti_P
    id_to_use
    id_to_use = id_to_use.ID_Actividad 
    numero_parto = crud.get_max_partos(db, vaca=data.ID_VACA, id_cliente = current_user.ID_CLIENTE)
    try:
        numero = int(numero_parto[0]['max_partos'])+1
    except:
        numero = 1
    id_parto = crud.registrar_parto(db=db, data=data, id_to_use=id_to_use, numero=numero)
    id_parto_new = id_parto.IDparto
    return id_parto_new

#patch partos

@app.get("/UbicacionVacas/", response_model=List[schemas.Ubicacion_VacasT], tags=["Actividades-Vacas"])
def read_ubva(db: Session = Depends(get_db), id_vaca:Optional[str]=None, id_hato:Optional[str]=None, id_lote:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    ub_va = crud.get_ubva(db, id_vaca=id_vaca, id_hato=id_hato, id_lote=id_lote, id_cliente= current_user.ID_CLIENTE)
    return ub_va

# DB View
@app.get("/UbicacionVacas_view/", response_model=List[schemas.Ubicacion_Vacas_FullT], tags=["Actividades-Vacas"])
def read_ubvaf(db: Session = Depends(get_db), id_vaca:Optional[str]=None, id_hato:Optional[str]=None, id_lote:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    ub_vaf = crud.get_ubvaf(db, id_vaca=id_vaca, id_hato=id_hato, id_lote=id_lote, id_cliente= current_user.ID_CLIENTE)
    return ub_vaf

#patch ubicacion vacas

@app.get("/TrasVacas/", response_model=List[schemas.Traslado_VacasT], tags=["Actividades-Vacas"])
async def read_hist_trasvacas(db: Session = Depends(get_db), id_hato:Optional[str]=None, id_vaca:Optional[str]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"),current_user: schemas.UserInfo = Depends(get_current_active_user)): #skip: int = 0, limit: int = 100,
    hist_trasvacas = crud.get_trasvaca(db, id_hato=id_hato, id_vaca=id_vaca, date1=date1, date2=date2, id_cliente = current_user.ID_CLIENTE)# skip=skip, limit=limit)
    return hist_trasvacas

@app.post("/Traslado_vaca/", status_code=201, tags=["Actividades-Vacas"])
async def tras_ubica_vacas(sch_ubi: schemas.Ubicacion_VacasT, db: Session = Depends(get_db), Fecha_Traslado : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    #obtener lote_id del hato al que se mueve la vaca
    id_lote = crud.get_ubha(db, id_hato=sch_ubi.ID_HATO, id_cliente= current_user.ID_CLIENTE)
    #print(id_lote)
    #transformar JSON a dataframe y extraer unico lote en INT
    #if id_lote is not None:
    id_lote2 = pd.DataFrame.from_records([s.__dict__ for s in id_lote])
    id_lote2.reset_index(drop=True, inplace=True)
    id_lote = id_lote2.ID_LOTE.mode()
    #actualizar diccionario incluyendo datos del lote
    sch_ubi.ID_LOTE=int(id_lote)
    #actualizar datos de ubicacion
    updated = crud.update_ubica_vaca(db=db, sch_ubi=sch_ubi, id_cliente= current_user.ID_CLIENTE)#, id_lote=id_lote)
    if updated == 'ok':
        print('ok')
        #si la ubicacion ya existia y se actualizo, entonces escribir nuevo traslado id
        db_tras_vaca = crud.write_trasvaca(db=db, sch_ubi=sch_ubi, Fecha_Traslado=Fecha_Traslado, id_cliente = current_user.ID_CLIENTE)
        if db_tras_vaca is None: #si el traslado de vaca no se registro, mostrar error
            raise HTTPException(status_code=404, detail="Traslado no registrado")
    #si la ubicacion no existia, entonces escribir nueva ubicacion y nuevo traslado
    else:
    #else: #toca restringir vacas, lotes y hatos desde la APP con seleccion, no texto
        print('Vaca es nueva')
        #primero comprobrar que el cliente tenga esa vaca, lote y hato
        #data_histo = crud.get_ubva(db=db, id_vaca=sch_ubi.ID_VACA, id_cliente= current_user.ID_CLIENTE) #id_hato=sch_ubi.ID_HATO, id_lote=sch_ubi.ID_LOTE,
        #if len(data_histo) == 0 :
        #    #si el cliente no tiene alguno de esos, mostrar error para que ingrese nuevos datos
        #    raise HTTPException(status_code=400, detail="Vaca, o Lote, o Hato no son de cliente")
        #elif len(data_histo) == 1:
        crud.write_ubi_vaca(db=db, sch_ubi=sch_ubi, id_cliente=current_user.ID_CLIENTE)#, id_lote = id_lote)
        db_tras_vaca = crud.write_trasvaca(db=db, sch_ubi=sch_ubi, Fecha_Traslado=Fecha_Traslado, id_cliente = current_user.ID_CLIENTE)
        if db_tras_vaca is None: #si el traslado de vaca no se registro, mostrar error
            raise HTTPException(status_code=404, detail="Traslado no registrado")   
    return db_tras_vaca

#patch traslado vacas


##########################################################################################################


#########################################    LECHE    #####################################################
@app.get("/Leche_Hatos/", response_model=List[schemas.Leche_Hatosi], tags=["Leche"]) 
def read_leche_hatos(db: Session = Depends(get_db), id_hato:Optional[int]=None, id_operario:Optional[int]=None, id_leche_ha:Optional[int]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d") ,current_user: schemas.UserInfo = Depends(get_current_active_user)): #date1: str='2020-01-01'
    leche_hatos = crud.get_leche_hatos(db, id_hato=id_hato, id_operario=id_operario, id_leche_ha=id_leche_ha, date1=date1, date2=date2, id_cliente = current_user.ID_CLIENTE) #, date1=date1
    return leche_hatos

@app.post("/Wr_Leche_Hatos/", status_code=201, tags=["Leche"]) #response_model=schemas.Leche_Hatosi)
def wr_leche_hatos(le_ha: schemas.Leche_HatosT, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_leche_hatos(db=db, le_ha=le_ha)

#patch leche hatos
@app.patch("/Leche_Hatos/{ID_Leche}", response_model=List[schemas.Leche_Hatosi], tags=["Leche"])
def update_leche_ha(ID_leche: int, leche: schemas.Leche_HatosU, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.update_leche_ha(db=db, leche=leche, id_leche=ID_leche)
    db_leche_ha = crud.get_leche_hatos(db, id_leche_ha=ID_leche, id_cliente = current_user.ID_CLIENTE)
    if db_leche_ha is None:
        raise HTTPException(status_code=404, detail="Lote_ID not found")
    return db_leche_ha

### Leche Vacas
@app.get("/Leche_Vacas/", response_model=List[schemas.Leche_Vacai], tags=["Leche"])
def read_leche_vaca(db: Session = Depends(get_db), id_vaca:Optional[int]=None, id_operario:Optional[int]=None, id_leche_va:Optional[int]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), current_user: schemas.UserInfo = Depends(get_current_active_user)): #date1: date = '2020-01-01'
    leche_vaca = crud.get_leche_vacas(db, id_vaca=id_vaca, id_operario=id_operario, id_leche_va=id_leche_va, date1=date1, date2=date2, id_cliente = current_user.ID_CLIENTE) #, date1=date
    return leche_vaca

@app.post("/Wr_Leche_vacas/", status_code=201, tags=["Leche"]) #, response_model=schemas.Leche_Vacai)
def wr_leche_vacas(le_va: schemas.Leche_VacaT, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_leche_vacas(db=db, le_va=le_va)

@app.post("/Wr_Leche_vaca_list/", status_code=201, tags=["Leche"]) #, response_model=schemas.Leche_Vacai)
def wr_leche_vaca_l(le_va: List[schemas.Leche_VacaT], db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_leche_vaca_list(db=db, le_va=le_va)

#patch leche vacas
@app.patch("/Leche_Vacas/{ID_Leche}", response_model=List[schemas.Leche_Vacai], tags=["Leche"])
def update_leche_va(ID_leche: int, leche: schemas.Leche_VacaU, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.update_leche_va(db=db, leche=leche, id_leche=ID_leche)
    db_leche_va = crud.get_leche_vacas(db, id_leche_va=ID_leche, id_cliente = current_user.ID_CLIENTE)
    if db_leche_va is None:
        raise HTTPException(status_code=404, detail="Lote_ID not found")
    return db_leche_va
##########################################################################################################

######################################### OTRAS FUENTES LOTES   #########################################
@app.post("/Wr_lotes_variables/", status_code=201, tags=["Otras Fuentes Lotes"]) #, response_model=schemas.Leche_Vacai)
def wr_lotes_var(lo_va: List[schemas.Lotes_variablesT], db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_lotes_var(db=db, lo_va=lo_va)

#get

#patch

@app.post("/Wr_lotes_quimicos/", status_code=201, tags=["Otras Fuentes Lotes"]) #, response_model=schemas.Leche_Vacai)
def wr_lotes_qui(lo_qu: List[schemas.Lotes_quimicosT], db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_lotes_qui(db=db, lo_qu=lo_qu)


#get

#patch

###########################################################################################################

##########################################  Monitoreo procesamiento imagenes satel   ######################
@app.post("/Wr_monitoreo_descargas/", status_code=201, tags=["Monitoreo Descargas satelitales"]) #, response_model=schemas.Leche_Vacai)
def wr_moni_des(mo_des: schemas.monitoreo_descargas_sentinelT, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_moni_des(db=db, mo_des=mo_des)

@app.get("/Rd_monitoreo_descargas/", response_model=List[schemas.monitoreo_descargas_sentinelT], tags=["Monitoreo Descargas satelitales"])
async def read_meteo(date1: str='2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), finca:Optional[str]=None, zona:Optional[str]=None, id_cliente:Optional[str]=None, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): 
    descarga_data = crud.get_moni_des(db, date1=date1, date2=date2, finca=finca, zona=zona, id_cliente = id_cliente) #current_user.ID_CLIENTE)# skip=skip, limit=limit)
    return descarga_data

###########################################################################################################

########################################   ESTACION METEOROLOGICA   #######################################
# API module only for Google Cloud Functions
@app.post("/Meteo/", response_model=schemas.MeteorologiaT, tags=["Estacion Meteorologica"])
def write_meteo(meteo: schemas.MeteorologiaT, db: Session = Depends(get_db)): #, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.registrar_meteo(db=db, meteo=meteo)

@app.get("/Meteo_get/", response_model=List[schemas.MeteorologiaT], tags=["Estacion Meteorologica"])
async def read_meteo_sta(date1: str='2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), estacion:Optional[str]=None, finca:Optional[str]=None, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): 
    meteo_data = crud.get_meteo(db, date1=date1, date2=date2, estacion=estacion, finca=finca, id_cliente = current_user.ID_CLIENTE)# skip=skip, limit=limit)
    return meteo_data

@app.get("/Meteo_csv/", response_model=List[schemas.MeteorologiaT], tags=["Estacion Meteorologica"])
async def meteo_csv(date1: str='2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), finca:Optional[str]=None, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): 
    meteo_data = crud.get_meteo(db, date1=date1, date2=date2, finca=finca, id_cliente = current_user.ID_CLIENTE)# skip=skip, limit=limit)    
    df = pd.DataFrame.from_records([s.__dict__ for s in meteo_data])
    df.reset_index(drop=True, inplace=True)
    cols = ["ID_FINCA", "ID_CLIENTE", "FECHA_HORA", "activacion", "DHT_Humidity_mean", "DHT_Humidity_max", "DHT_Humidity_min", "DHT_Humidity_std", "DHT_Temp_mean",
            "DHT_Temp_max", "DHT_Temp_min", "Hum_Gnd_mean", "Rain_mm_sum", "Thermo_Couple_mean", "Thermo_Couple_max", "Thermo_Couple_min", "Wind_Dir_Moda", "Wind_Speed_mean", "Wind_Speed_max", 
            "DS18b20_cap_mean", "DS18b20_cap_max", "DS18b20_cap_min", "Solar_Volt_mean", "Solar_Volt_max", "Solar_Volt_min", "Solar_Volt_std", "Sunlight_mean", "Sunlight_max", "Sunlight_min", "Sunlight_std"]
    df= df[cols]
    stream = io.StringIO()
    df.to_csv(stream, index = False)
    #response = StreamingResponse(io.StringIO(df.to_csv(index=False)), media_type="text/csv")
    response = StreamingResponse(iter([stream.getvalue()]),
                            media_type="text/csv"
       )
    response.headers["Content-Disposition"] = "attachment; filename=meteo_data.csv"   
    return response
#https://stackoverflow.com/questions/61140398/fastapi-return-a-file-response-with-the-output-of-a-sql-query

###########################################################################################################

####################################      STREAMING IMAGES   ################################################
@app.get("/Image_lote/", tags=["Stream Images"]) #response_model=List[schemas.MeteorologiaT]
async def imagen_lote(date1: str='2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), lote:Optional[str]=None, prop:Optional[str]=None, numero:Optional[int] = 0, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): 
    images_route = 'Data/PNG_Images/ID_CLIENTE-'
    id_cliente = current_user.ID_CLIENTE
    buck= 'satellite_storage'
    mindate = int(''.join(date1.split('-')))
    maxdate = int(''.join(date2.split('-')))
    print(mindate,maxdate)
    datos = GCP_functions.list_all_blobs(storage_client,buck,images_route+str(id_cliente)+'/','/', lote=lote, prop=prop, mindate=mindate, maxdate=maxdate)
    open_file = GCP_functions.open_blob(storage_client,buck, datos[numero]) #, "../"+os.path.basename(datos[0].split('/')[-1]))
    return StreamingResponse(io.BytesIO(open_file), media_type="image/png")


# https://stackoverflow.com/questions/61163024/return-multiple-files-from-fastapi
@app.get("/Multi_Image_lote/", tags=["Stream Images"]) #response_model=List[schemas.MeteorologiaT]
async def imagen_lotes(date1: str='2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), lote:Optional[str]=None, prop:Optional[str]=None, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): 
    images_route = 'Data/PNG_Images/ID_CLIENTE-'
    id_cliente = current_user.ID_CLIENTE
    buck= 'satellite_storage'
    mindate = int(''.join(date1.split('-')))
    maxdate = int(''.join(date2.split('-')))
    print(mindate,maxdate)
    datos = GCP_functions.list_all_blobs(storage_client,buck,images_route+str(id_cliente)+'/','/', lote=lote, prop=prop, mindate=mindate, maxdate=maxdate)
    results ={}
    for dato in datos:
        open_file = GCP_functions.open_blob(storage_client,buck, dato)
        #results[str(dato.split('/')[-1])]: (StreamingResponse(io.BytesIO(open_file), media_type="image/png"))
        results[str(dato.split('/')[-1])]: io.BytesIO(open_file)
    return results
        
    
    #return StreamingResponse(io.BytesIO(GCP_functions.open_multi_blob(storage_client,buck, datos)), media_type="image/png")
    '''async def stream_imagenes(datos):
        yield [io.BytesIO(GCP_functions.open_blob(storage_client,buck, dato)) for dato in datos]
        yield b""
    return stream_imagenes(datos)
    '''
    '''
    def get_bytes_value(image):
        img_byte_arr = io.BytesIO(GCP_functions.open_blob(storage_client,buck, image))
        image.save(img_byte_arr, format='PNG') #img.save
        return img_byte_arr.getvalue()   
    return [get_bytes_value(image) for image in datos] if datos else None
    '''
             
'''
    for dato in datos:
        open_file = GCP_functions.download_blob(storage_client,buck, dato, "../"+os.path.basename(dato.split('/')[-1]))
        StreamingResponse(io.BytesIO(open_file))
  
    def zipfile(datos):
        zip_io = io.BytesIO()
        with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as temp_zip:
            for fpath in datos:
                # Calculate path for file in zip
                fdir, fname = os.path.split(fpath)
                zip_path = os.path.join(fdir, fname)
                # Add file, at correct path
                temp_zip.write((fpath, zip_path))
        return StreamingResponse(
            iter([zip_io.getvalue()]), 
            media_type="application/x-zip-compressed", 
            headers = { "Content-Disposition": f"attachment; filename=images.zip"}
            )
'''
import shutil
@app.post("/Image_load/{clase_id}", tags=["Stream Images"]) #response_model=List[schemas.MeteorologiaT]
async def imagen_load(clase_id:str, image: UploadFile = File(...) , db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user) ): 
    id_cliente = current_user.ID_CLIENTE
    Tipo_clase=clase_id
    buck= 'api-images-user'
    destination_name = "ID_CLIENTE-" + str(id_cliente) +"/"+ Tipo_clase + "/" + image.filename #"test.jpg" #+ image.filename
    blob = GCP_functions.upload_blob_file(storage_client, buck, destination_name)
    blob.create_resumable_upload_session()
    blob.upload_from_file(image.file)  #.file) #buffer)
    return {"file_name":image.filename}


@app.post("/Multi_Image/{clase_id}", tags=["Stream Images"]) #response_model=List[schemas.MeteorologiaT]
async def imagen_multid(clase_id:str, files: List[UploadFile] = File(...) , db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): #, current_user: schemas.UserInfo = Depends(get_current_active_user)): 
    for img in files:
        id_cliente = current_user.ID_CLIENTE
        Tipo_clase=clase_id
        buck= 'api-images-user'
        destination_name = "ID_CLIENTE-" + str(id_cliente) +"/"+ Tipo_clase + "/" + img.filename 
        #with open(f'{img.filename}', 'wb') as buffer:
        #    shutil.copyfileobj(img.file, buffer)
        blob = GCP_functions.upload_blob_file(storage_client, buck, destination_name)
        blob.create_resumable_upload_session()
        blob.upload_from_file(img.file)
        
    return {"file_name":"Good"}
    
    #images_route = 'Data/Upload_Images/'#'ID_CLIENTE-'
    #id_cliente = current_user.ID_CLIENTE
    #buck= 'satellite_storage'
    #datos = GCP_functions.list_all_blobs(storage_client,buck,images_route+str(id_cliente)+'/','/', lote=lote, prop=prop, mindate=mindate, maxdate=maxdate)
    #open_file = GCP_functions.open_blob(storage_client,buck, datos[numero]) #, "../"+os.path.basename(datos[0].split('/')[-1]))
    
    #return StreamingResponse(io.BytesIO(open_file), media_type="image/png")


#id_cliente = str(1) #id_cliente
#prop = 'ndvi'
#lote = str(100)

#########################################################################################################################

################################################## CELOTRON   ###########################################################
@app.post("/Heat_Detection/", status_code=200, tags=["Deteccion Celo"]) #response_model=List[schemas.MeteorologiaT]
async def celo_detect(db: Session = Depends(get_db)): # sch_celo: schemas.celoT,, current_user: schemas.UserInfo = Depends(get_current_active_user)): 
    #write to DB
    #id_celo = crud.write_celo(db=db, sch_celo=sch_celo)
    id_celo = crud.write_celo(db)
    # Start our TwiML response
    resp = MessagingResponse()
    resp.message("Mensaje de Celo recibido!, consecutivo: " + str(id_celo))
    
    ### reenviar SMS
    crud.sms_celo()
    return str(resp)

#invalid content type application-json