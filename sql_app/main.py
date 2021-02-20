# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:25:17 2020

@author: Marcelo
"""

from typing import List, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, date, datetime
from typing import Optional
from jose import JWTError
from . import crud, models, schemas, app_utils
from .database import SessionLocal, engine


# security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# app engine
models.Base.metadata.create_all(bind=engine)
# APP
app = FastAPI()


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

@app.get("/clientes/", response_model=List[schemas.ClientesT])  # sT
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    clientes = crud.get_clientes(db, skip=skip, limit=limit)
    return clientes


@app.get("/clientes/{ID_CLIENTE}", response_model=schemas.ClientesT)  # sT
def read_client(ID_CLIENTE: int, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    db_client = crud.get_client(db, cliente_id=ID_CLIENTE)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client


@app.get("/Operario", response_model=List[schemas.OperarioT])  # List[
def read_operarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    operarios = crud.get_operarios(db, skip=skip, limit=limit)
    return operarios


@app.get("/Operario/{ID_OPERARIO}", response_model=schemas.OperarioT)  # sT
def read_oper_id(ID_OPERARIO: int, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    db_operario_id = crud.get_oper_by_id(db, id_operario=ID_OPERARIO)
    if db_operario_id is None:
        raise HTTPException(status_code=404, detail="Operario_ID not found")
    return db_operario_id

@app.get("/Operario_name/{NombreOperario}", response_model=schemas.OperarioT)
def read_operario(NombreOperario: str, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    name_oper = crud.get_oper_by_name(db, NombreOperario=NombreOperario)
    if name_oper is None:
        raise HTTPException(status_code=404, detail="Operario not found")
    return name_oper


@app.get("/Operario_rol/{RolOperario}", response_model=schemas.OperarioT)  # sT
def read_operario_rol(RolOperario: str, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    rol_oper = crud.get_oper_by_rol(db, rol_operario=RolOperario)
    if rol_oper is None:
        raise HTTPException(status_code=404, detail="Rol Operario not found")
    return rol_oper


@app.post("/Operario/", response_model=schemas.OperarioCreate)
def write_operario(operario: schemas.OperarioCreate, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
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


@app.get("/Fincas/", response_model=List[schemas.FincaT])
def read_fincas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    fincas = crud.get_fincas(db, skip=skip, limit=limit)
    return fincas


@app.post("/Fincas/{finca_id}/Lotes/", response_model=schemas.LotesT)
def write_lote_for_finca(finca_id: int, lote: schemas.LotesT, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_finca_lote(db=db, lote=lote, finca_id=finca_id)


@app.get("/Lotes/", response_model=List[schemas.LotesT])
def read_lotes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    lotes = crud.get_lotes(db, skip=skip, limit=limit)
    return lotes

@app.get("/UbicacionVacas/", response_model=List[schemas.Ubicacion_VacasT])
def read_ubva(db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    ub_va = crud.get_ubva(db)
    return ub_va

@app.get("/Lotes/{ID_LOTE}", response_model=schemas.LotesT)  # sT
def read_lotes_id(ID_LOTE: int, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    db_lote_id = crud.get_lote_by_id(db, id_lote=ID_LOTE)
    if db_lote_id is None:
        raise HTTPException(status_code=404, detail="Lote_ID not found")
    return db_lote_id


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


@app.get("/Hatos/", response_model=List[schemas.HatosT])
def read_hatos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    hatos = crud.get_hatos(db, skip=skip, limit=limit)
    return hatos

@app.get("/Leche_Hatos/", response_model=List[schemas.Leche_Hatosi]) 
def read_leche_hatos(db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): #date1: str='2020-01-01'
    leche_hatos = crud.get_leche_hatos(db) #, date1=date1
    return leche_hatos

@app.post("/Wr_Leche_Hatos/", status_code=201) #response_model=schemas.Leche_Hatosi)
def wr_leche_hatos(le_ha: schemas.Leche_Hatosi, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_leche_hatos(db=db, le_ha=le_ha)

@app.get("/Hatos/{ID_HATO}", response_model=schemas.HatosT)  # sT
def read_hatos_id(ID_HATO: int, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    db_hato_id = crud.get_hato_by_id(db, id_hato=ID_HATO)
    if db_hato_id is None:
        raise HTTPException(status_code=404, detail="HATO_ID not found")
    return db_hato_id


@app.get("/Vacas/", response_model=List[schemas.VacasT])
def read_vacas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    vacas = crud.get_vacas(db, skip=skip, limit=limit)
    return vacas

@app.get("/Leche_Vacas/", response_model=List[schemas.Leche_Vacai])
def read_leche_vaca(db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)): #date1: date = '2020-01-01'
    leche_vaca = crud.get_leche_vacas(db) #, date1=date
    return leche_vaca

@app.post("/Wr_Leche_vacas/", status_code=201) #, response_model=schemas.Leche_Vacai)
def wr_leche_vacas(le_va: schemas.Leche_Vacai, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.create_leche_vacas(db=db, le_va=le_va)

@app.get("/Vacas/{ID_VACA}", response_model=schemas.VacasT)  # sT
def read_vacas_id(ID_VACA: int, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    db_vaca_id = crud.get_vaca_by_id(db, id_vaca=ID_VACA)
    if db_vaca_id is None:
        raise HTTPException(status_code=404, detail="VACA_ID not found")
    return db_vaca_id


@app.get("/Vacas_name/{NAME_VACA}", response_model=schemas.VacasT)  # sT
def read_vacas_name(NAME_VACA: str, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    db_vaca_name = crud.get_vaca_by_name(db, name_vaca=NAME_VACA)
    if db_vaca_name is None:
        raise HTTPException(status_code=404, detail="VACA_NOMBRE not found")
    return db_vaca_name


@app.post("/Mastitis/", response_model=Union[schemas.MastitisT, schemas.ActInfo])
async def write_mastitis(mastitis: schemas.MastitisT, av:schemas.ActInfo, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_active_user)):
    id_to_use = crud.reg_actividades_vacas(db=db, av=av)
    id_to_use
    id_to_use = id_to_use.ID_Actividad 
    return crud.registrar_mastitis(db=db, mastitis=mastitis, id_to_use=id_to_use)


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


#################################################
# API module only for Google Cloud Functions
@app.post("/Meteo/", response_model=schemas.MeteorologiaT)
def write_meteo(meteo: schemas.MeteorologiaT, db: Session = Depends(get_db)): #, current_user: schemas.UserInfo = Depends(get_current_active_user)):
    return crud.registrar_meteo(db=db, meteo=meteo)

##################################################