# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:25:17 2020

@author: Marcelo
"""

from typing import List, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from datetime import timedelta, date, datetime
from typing import Optional
from jose import JWTError
from . import crud, models, schemas, app_utils, secrets
from .database import SessionLocal, engine
import pandas as pd
import io


# security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# app engine
models.Base.metadata.create_all(bind=engine)
# APP
app = FastAPI()

### CORS
app.add_middleware(
    CORSMiddleware,
    #allow_origins=secrets.origins,
    allow_origin_regex='https?://.*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# OATH
#################################
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


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.active_status != 1:  # 0=inactive, 1=active
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/user", response_model=schemas.UserInfo)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user=user.user)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user_t=user)


@app.post("/token", response_model=schemas.Token)
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

@app.patch("/User_upd/{USERNAME}", response_model=schemas.UserInfo2)
def update_user_status(USERNAME: str, user_t: schemas.User, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.update_user(db=db, user_t=user_t, username=USERNAME)
    db_user_id = crud.get_user_by_username(db, user=USERNAME)
    if db_user_id is None:
        raise HTTPException(status_code=404, detail="Username not found")
    return db_user_id

@app.get("/Users_all/", response_model=List[schemas.UserInfo2])  # sT
def read_users(db: Session = Depends(get_db), full_name: Optional[str]=None, email: Optional[str]=None, active_status: Optional[int]=None,  user_rol: Optional[int]=None, operario: Optional[int]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    usuarios = crud.get_all_users(db, full_name=full_name, email=email, active_status=active_status,  user_rol=user_rol, operario=operario, id_cliente= current_user.ID_CLIENTE)
    return usuarios


@app.get("/clientes/", response_model=List[schemas.ClientesT])  # sT
def read_clientes(db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user), ciudad:Optional[str]=None, departamento:Optional[str]=None, nombre:Optional[str]=None, date1: Optional[str]=None, id_cliente:Optional[str]=None):
    clientes = crud.get_clientes(db, ciudad=ciudad, departamento=departamento, nombre=nombre, date1= date1, id_cliente=id_cliente)
    return clientes

@app.post("/Cliente/", status_code=201)
def write_cliente(cliente: schemas.ClientesCreate, db: Session = Depends(get_db)): #, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_cliente(db=db, cliente=cliente)
    #esto seria bueno asociarlo con enviar un email, con formulario y que el ID de cliente se guarde
    #para asignarlo al usuario creado


@app.get("/Operario", response_model=List[schemas.OperarioT])  # List[
def read_operarios(db: Session = Depends(get_db), finca:Optional[str]=None, rol:Optional[str]=None, nombre:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    operarios = crud.get_operarios(db, finca=finca, rol=rol, nombre=nombre, id_cliente = current_user.ID_CLIENTE)
    return operarios


@app.post("/create_operario/", response_model=schemas.OperarioT)
def write_operario(operario: schemas.OperarioT, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_operario(db=db, operario=operario)


@app.delete("/Operario_del/{ID_OPERARIO}", )
def erase_operario(ID_OPERARIO: int, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.delete_operario(db, id_operario=ID_OPERARIO)  # operario = operario,
    db_operario_id = crud.get_oper_by_id(db, id_operario=ID_OPERARIO)
    if db_operario_id is not None:
        raise HTTPException(status_code=404, detail="Operario_ID not deleted")
    return {
        "status": True,
        "message": "User deleted"
    }

### Fincas
@app.get("/Fincas/", response_model=List[schemas.FincaT])
def read_fincas(db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user), finca:Optional[int]=None, nombre:Optional[str]=None):
    fincas = crud.get_fincas(db, finca=finca, id_cliente = current_user.ID_CLIENTE, nombre=nombre)
    return fincas

@app.get("/Fincas_small/", response_model=List[schemas.FincaR])
def read_fincas(db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user), finca:Optional[int]=None, nombre:Optional[str]=None):
    fincas = crud.get_fincas(db, finca=finca, id_cliente = current_user.ID_CLIENTE, nombre=nombre)
    return fincas


@app.post("/create_finca/", status_code=201) #response_model=schemas.Leche_Hatosi)
def wr_finca(finca: schemas.FincaP, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_finca(db=db, finca=finca, id_cliente= current_user.ID_CLIENTE)
#solo funciona si tabla lotes tiene finca_id creada ... cambiar SQL, sino se puede, APP debera crear finca y lote al tiempo
#obteniendo max finca_id, asignando en tabla lotes y despues en tabla fincas


@app.post("/Fincas/{finca_id}/Lotes/", response_model=schemas.LotesT)
def write_lote_for_finca(finca_id: int, lote: schemas.LotesT, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_finca_lote(db=db, lote=lote, finca_id=finca_id, id_cliente= current_user.ID_CLIENTE)


@app.get("/Lotes/", response_model=List[schemas.LotesT])
def read_lotes(db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user), id_finca:Optional[int]=None, id_lote:Optional[int]=None, nombre:Optional[str]=None):
    lotes = crud.get_lotes(db, id_finca=id_finca, id_lote=id_lote, nombre=nombre, id_cliente = current_user.ID_CLIENTE)
    return lotes

@app.get("/UbicacionVacas/", response_model=List[schemas.Ubicacion_VacasT])
def read_ubva(db: Session = Depends(get_db), id_vaca:Optional[str]=None, id_hato:Optional[str]=None, id_lote:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    ub_va = crud.get_ubva(db, id_vaca=id_vaca, id_hato=id_hato, id_lote=id_lote, id_cliente= current_user.ID_CLIENTE)
    return ub_va



@app.delete("/Lotes_del/{ID_LOTE}", )
def erase_lote(ID_LOTE: int, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.delete_lote(db, id_lote=ID_LOTE)  # operario = operario,
    db_lote_id = crud.get_lote_by_id(db, id_lote=ID_LOTE)
    if db_lote_id is not None:
        raise HTTPException(status_code=404, detail="Lote_ID not deleted")
    return {
        "status": True,
        "message": "Lote deleted"
    }


@app.patch("/Lotes_upd/{ID_LOTE}", response_model=schemas.LotesT)
def update_lotes_id(ID_LOTE: int, lote: schemas.LotesT, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    crud.update_lote(db=db, lote=lote, id_lote=ID_LOTE)
    db_lote_id = crud.get_lote_by_id(db, id_lote=ID_LOTE)
    if db_lote_id is None:
        raise HTTPException(status_code=404, detail="Lote_ID not found")
    return db_lote_id


@app.get("/Acti_Lotes/", response_model=List[schemas.Actividades_LotesT])
def read_acti_lotes(db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user), id_finca:Optional[int]=None, id_lote:Optional[int]=None, nombre_lote:Optional[str]=None, nombre_oper:Optional[str]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d")):
    acti_lotes = crud.get_acti_lotes(db, id_finca=id_finca, id_lote=id_lote, nombre_lote=nombre_lote, nombre_oper=nombre_oper, date1=date1, date2=date2, id_cliente = current_user.ID_CLIENTE)
    return acti_lotes

@app.post("/Wr_Acti_Lotes/", status_code=201) #response_model=schemas.Leche_Hatosi)
def wr_acti_lotes(ac_lo: schemas.Actividades_LotesT, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_acti_lotes(db=db, ac_lo=ac_lo)
#funciona, pero duplica ID_acti_lote, sino se puede corregir SQL, entonces hacer get max ID y crear con +1


@app.get("/Hatos/", response_model=List[schemas.HatosT])
def read_hatos(db: Session = Depends(get_db), id_finca:Optional[int]=None, id_hato:Optional[int]=None, nombre:Optional[str]=None, tipo:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    hatos = crud.get_hatos(db, id_finca=id_finca, id_hato=id_hato, nombre=nombre, tipo=tipo, id_cliente = current_user.ID_CLIENTE)
    return hatos

@app.get("/Hatos_small/", response_model=List[schemas.HatosR])
def read_hatos(db: Session = Depends(get_db), id_finca:Optional[int]=None, id_hato:Optional[int]=None, nombre:Optional[str]=None, tipo:Optional[str]=None, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    hatos = crud.get_hatos(db, id_finca=id_finca, id_hato=id_hato, nombre=nombre, id_cliente = current_user.ID_CLIENTE)
    return hatos

@app.post("/create_hato/", status_code=201) #response_model=schemas.Leche_Hatosi)
def wr_hato(hato: schemas.HatosP, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_hato(db=db, hato=hato, id_cliente= current_user.ID_CLIENTE)
#funciona, pero duplica ID_hato, sino se puede corregir SQL, entonces hacer get max ID y crear con +1


@app.get("/Leche_Hatos/", response_model=List[schemas.Leche_Hatosi]) 
def read_leche_hatos(db: Session = Depends(get_db), id_hato:Optional[int]=None, id_operario:Optional[int]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d") ,current_user: schemas.UserInfo = Depends(get_current_active_user)): #date1: str='2020-01-01'
    leche_hatos = crud.get_leche_hatos(db, id_hato=id_hato, id_operario=id_operario, date1=date1, date2=date2, id_cliente = current_user.ID_CLIENTE) #, date1=date1
    return leche_hatos

@app.post("/Wr_Leche_Hatos/", status_code=201) #response_model=schemas.Leche_Hatosi)
def wr_leche_hatos(le_ha: schemas.Leche_Hatosi, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_leche_hatos(db=db, le_ha=le_ha)



@app.get("/Vacas/", response_model=List[schemas.VacasT])
async def read_vacas(db: Session = Depends(get_db), id_finca:Optional[int]=None, id_vaca:Optional[int]=None, nombre:Optional[str]=None, sexo:Optional[int]=None, raza:Optional[int]=None, activa:int=1, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    vacas = crud.get_vacas(db, id_finca=id_finca, id_vaca=id_vaca, nombre=nombre, sexo=sexo, raza=raza, activa=activa, id_cliente = current_user.ID_CLIENTE)
    return vacas

@app.get("/Vacas_small/", response_model=List[schemas.VacasR])
async def read_vacas(db: Session = Depends(get_db), id_finca:Optional[int]=None, id_vaca:Optional[int]=None, nombre:Optional[str]=None, sexo:Optional[int]=None, raza:Optional[int]=None, activa:int=1, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    vacas = crud.get_vacas(db, id_finca=id_finca, id_vaca=id_vaca, nombre=nombre, sexo=sexo, raza=raza, activa=activa, id_cliente = current_user.ID_CLIENTE)
    return vacas

@app.get("/Leche_Vacas/", response_model=List[schemas.Leche_Vacai])
def read_leche_vaca(db: Session = Depends(get_db), id_vaca:Optional[int]=None, id_operario:Optional[int]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), current_user: schemas.UserInfo = Depends(get_current_active_user)): #date1: date = '2020-01-01'
    leche_vaca = crud.get_leche_vacas(db, id_vaca=id_vaca, id_operario=id_operario, date1=date1, date2=date2, id_cliente = current_user.ID_CLIENTE) #, date1=date
    return leche_vaca

@app.post("/Wr_Leche_vacas/", status_code=201) #, response_model=schemas.Leche_Vacai)
def wr_leche_vacas(le_va: schemas.Leche_Vacai, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_leche_vacas(db=db, le_va=le_va)

'''
@app.post("/Mastitis/", response_model=Union[schemas.MastitisT, schemas.ActInfo])
async def write_mastitis(mastitis: schemas.MastitisT, av:schemas.ActInfo, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    id_to_use = crud.reg_actividades_vacas(db=db, av=av)
    id_to_use
    id_to_use = id_to_use.ID_Actividad 
    return crud.registrar_mastitis(db=db, mastitis=mastitis, id_to_use=id_to_use)
'''

@app.post("/Masti_2/", status_code=201)
async def write_masti_2(data: schemas.Mast_Requi, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    id_to_use = crud.reg_acti_2(db=db, data=data)
    id_to_use
    id_to_use = id_to_use.ID_Actividad 
    return crud.registrar_masti_2(db=db, data=data, id_to_use=id_to_use)


@app.get("/ActiVacas/", response_model=List[schemas.ActInfo])
async def read_act_vacas(date1: str='2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), vaca:Optional[str]=None, operacion:Optional[int]=None, operario:Optional[int]=None,db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): #skip: int = 0, limit: int = 100,
    act_vacas = crud.get_act_vacas(db, date1=date1, date2=date2, vaca=vaca, operacion=operacion, operario=operario, id_cliente = current_user.ID_CLIENTE)# skip=skip, limit=limit)
    return act_vacas


@app.get("/Mastit_get/", response_model=List[Union[schemas.MastitisT,schemas.ActInfo]])
async def read_mastitis(date1: str='2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), vaca:Optional[str]=None, operacion:Optional[int]=None, operario:Optional[int]=None,db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): #skip: int = 0, limit: int = 100,
    act_mast = crud.get_act_mastitis(db, date1=date1, date2=date2, vaca=vaca, operacion=operacion, operario=operario, id_cliente = current_user.ID_CLIENTE)
    return act_mast

@app.get("/TrasVacas/", response_model=List[schemas.Traslado_VacasT])
async def read_hist_trasvacas(db: Session = Depends(get_db), id_hato:Optional[str]=None, id_vaca:Optional[str]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"),current_user: schemas.UserInfo = Depends(get_current_active_user)): #skip: int = 0, limit: int = 100,
    hist_trasvacas = crud.get_trasvaca(db, id_hato=id_hato, id_vaca=id_vaca, date1=date1, date2=date2, id_cliente = current_user.ID_CLIENTE)# skip=skip, limit=limit)
    return hist_trasvacas

@app.post("/Traslado_vaca/", status_code=201)
async def tras_ubica_vacas(sch_ubi: schemas.Ubicacion_VacasT, db: Session = Depends(get_db), Fecha_Traslado : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    #actualizar datos de ubicacion
    updated = crud.update_ubica_vaca(db=db, sch_ubi=sch_ubi, id_cliente= current_user.ID_CLIENTE)
    if updated == 'ok':
        #si la ubicacion ya existia y se actualizo, entonces escribir nuevo traslado id
        db_tras_vaca = crud.write_trasvaca(db=db, sch_ubi=sch_ubi, Fecha_Traslado=Fecha_Traslado, id_cliente = current_user.ID_CLIENTE)
        if db_tras_vaca is None: #si el traslado de vaca no se registro, mostrar error
            raise HTTPException(status_code=404, detail="Traslado no registrado")
    
    #si la ubicacion no existia, entonces escribir nueva ubicacion y nuevo traslado
    else: #toca restringir vacas, lotes y hatos desde la APP con seleccion, no texto
        #primero comprobrar que el cliente tenga esa vaca, lote y hato
        #data_histo = crud.get_ubva(db=db, id_vaca=sch_ubi.ID_VACA, id_cliente= current_user.ID_CLIENTE) #id_hato=sch_ubi.ID_HATO, id_lote=sch_ubi.ID_LOTE,
        #if len(data_histo) == 0 :
        #    #si el cliente no tiene alguno de esos, mostrar error para que ingrese nuevos datos
        #    raise HTTPException(status_code=400, detail="Vaca, o Lote, o Hato no son de cliente")
        #elif len(data_histo) == 1:
        crud.write_ubi_vaca(db=db, sch_ubi=sch_ubi, id_cliente=current_user.ID_CLIENTE)
        db_tras_vaca = crud.write_trasvaca(db=db, sch_ubi=sch_ubi, Fecha_Traslado=Fecha_Traslado, id_cliente = current_user.ID_CLIENTE)
        if db_tras_vaca is None: #si el traslado de vaca no se registro, mostrar error
            raise HTTPException(status_code=404, detail="Traslado no registrado")
    return db_tras_vaca

@app.get("/TrasHatos/", response_model=List[schemas.Traslado_HatosT])
async def read_hist_trashatos(db: Session = Depends(get_db), id_hato:Optional[str]=None, id_lote:Optional[str]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"),current_user: schemas.UserInfo = Depends(get_current_active_user)): #skip: int = 0, limit: int = 100,
    hist_trashatos = crud.get_trashato(db, id_hato=id_hato, id_lote=id_lote, date1=date1, date2=date2, id_cliente = current_user.ID_CLIENTE)# skip=skip, limit=limit)
    return hist_trashatos

@app.post("/Traslado_hato/", status_code=201)
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


@app.post("/Wr_lotes_variables/", status_code=201) #, response_model=schemas.Leche_Vacai)
def wr_lotes_var(lo_va: List[schemas.Lotes_variablesT], db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_lotes_var(db=db, lo_va=lo_va)

@app.post("/Wr_lotes_quimicos/", status_code=201) #, response_model=schemas.Leche_Vacai)
def wr_lotes_qui(lo_qu: schemas.Lotes_quimicosT, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_lotes_qui(db=db, lo_qu=lo_qu)

@app.post("/Wr_monitoreo_descargas/", status_code=201) #, response_model=schemas.Leche_Vacai)
def wr_moni_des(mo_des: schemas.monitoreo_descargas_sentinelT, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_moni_des(db=db, mo_des=mo_des)


#################################################
# API module only for Google Cloud Functions
@app.post("/Meteo/", response_model=schemas.MeteorologiaT)
def write_meteo(meteo: schemas.MeteorologiaT, db: Session = Depends(get_db)): #, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.registrar_meteo(db=db, meteo=meteo)

@app.get("/Meteo_get/", response_model=List[schemas.MeteorologiaT])
async def read_meteo(date1: str='2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), finca:Optional[str]=None, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): 
    meteo_data = crud.get_meteo(db, date1=date1, date2=date2, finca=finca, id_cliente = current_user.ID_CLIENTE)# skip=skip, limit=limit)
    return meteo_data

@app.get("/Meteo_csv/", response_model=List[schemas.MeteorologiaT])
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
    


##################################################