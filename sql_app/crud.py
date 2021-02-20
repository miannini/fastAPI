# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:17:18 2020

@author: Marcelo
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional
from . import models, schemas
from datetime import date, datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

##########################

#CRUD = Create, Read, Update and Delete

def get_client(db: Session, cliente_id: int):
    return db.query(models.ClientesT).filter(models.ClientesT.ID_CLIENTE == cliente_id).first()

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ClientesT).offset(skip).limit(limit).all()

def get_oper_by_name(db: Session, NombreOperario: str):
    return db.query(models.OperarioT).filter(models.OperarioT.NombreOperario == NombreOperario).first()

def get_oper_by_id(db: Session, id_operario: int):
    return db.query(models.OperarioT).filter(models.OperarioT.ID_OPERARIO == id_operario).first()

def get_oper_by_rol(db: Session, rol_operario: str):
    return db.query(models.OperarioT).filter(models.OperarioT.Rol == rol_operario).first()

def get_operarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.OperarioT).offset(skip).limit(limit).all()

def create_operario(db: Session, operario: schemas.OperarioCreate):
    db_operario = models.OperarioT(**operario.dict())
    db.add(db_operario)
    db.commit()
    db.refresh(db_operario)
    return db_operario

def delete_operario(db: Session, id_operario: int): #operario: schemas.OperarioDelete,
    db.query(models.OperarioT).filter(models.OperarioT.ID_OPERARIO == id_operario).delete()
    db.commit()
 
#get Finca    
def get_fincas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FincaT).offset(skip).limit(limit).all()

#get lotes    
def get_lotes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LotesT).offset(skip).limit(limit).all()

#create lote_de_finca
def create_finca_lote(db: Session, lote: schemas.LotesT, finca_id: int):
    db_lote = models.LotesT(**lote.dict())#, ID_FINCA=finca_id)
    db.add(db_lote)
    db.commit()
    db.refresh(db_lote)
    return db_lote


def get_lote_by_id(db: Session, id_lote: int):
    return db.query(models.LotesT).filter(models.LotesT.ID_LOTE == id_lote).first()

def delete_lote(db: Session, id_lote: int): #operario: schemas.OperarioDelete,
    db.query(models.LotesT).filter(models.LotesT.ID_LOTE == id_lote).delete()
    db.commit()

def update_lote(db: Session, lote: schemas.LotesT, id_lote: int):
    db.query(models.LotesT).filter(models.LotesT.ID_LOTE == id_lote).update(lote.dict(exclude_unset=True))
    db.commit()    
    
#get hatos    
def get_hatos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.HatosT).offset(skip).limit(limit).all()

def get_leche_hatos(db: Session): #, date1: str='2020-01-01'
    return db.query(models.Leche_HatosT).all() #filter(models.Leche_HatosT.FECHA_ACTIVIDAD >= date1)#.all()

def create_leche_hatos(db: Session, le_ha: schemas.Leche_Hatosi):
    db_le_ha = models.Leche_HatosT(**le_ha.dict())
    db.add(db_le_ha)
    db.commit()
    #db.refresh(db_le_ha)
    return "post_leche_hatos=Success"

def get_hato_by_id(db: Session, id_hato: int):
    return db.query(models.HatosT).filter(models.HatosT.ID_HATO == id_hato).first()

#get vacas    
def get_vacas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.VacasT).offset(skip).limit(limit).all()

def get_leche_vacas(db: Session): #, date1: date = '2020-01-01'
    return db.query(models.Leche_VacaT).all() #filter(models.Leche_VacaT.FECHA >= date1)

def create_leche_vacas(db: Session, le_va: schemas.Leche_Vacai):
    db_le_va = models.Leche_VacaT(**le_va.dict())
    db.add(db_le_va)
    db.commit()
    #db.refresh(db_le_va)
    return "post_leche_vacas=Success"

def get_vaca_by_id(db: Session, id_vaca: int):
    return db.query(models.VacasT).filter(models.VacasT.ID_VACA == id_vaca).first()

def get_vaca_by_name(db: Session, name_vaca: int):
    return db.query(models.VacasT).filter(models.VacasT.Nombre_Vaca == name_vaca).first()

#get lotes    
def get_ubva(db: Session):
    return db.query(models.Ubicacion_VacasT).all()

#meteorologia
def registrar_meteo(db: Session, meteo: schemas.MeteorologiaT):
    reg_meteo = models.MeteorologiaT(**meteo.dict())
    db.add(reg_meteo)
    db.commit()
    db.refresh(reg_meteo)
    return reg_meteo

'''
def create_operario(db: Session, operario: schemas.OperarioCreate):
    db_operario = models.OperarioT(**operario.dict())
    db.add(db_operario)
    db.commit()
    db.refresh(db_operario)
    return db_operario
'''

##########################3
#v2 auth
def get_user_by_username(db: Session, user: str):
    return db.query(models.API_UsersT).filter(models.API_UsersT.user == user).first()


def create_user(db: Session, user_t: schemas.UserCreate):
    #hashed_password = bcrypt.hashpw(user_t.password.encode('utf-8'), bcrypt.gensalt())
    hashed_password = pwd_context.hash(user_t.password)
    db_user = models.API_UsersT(user=user_t.user, password=hashed_password, full_name=user_t.full_name, email=user_t.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_t: schemas.User, username: str):
    db.query(models.API_UsersT).filter(models.API_UsersT.user == username).update(user_t.dict(exclude_unset=True))
    db.commit() 
########################################
#secure users
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    if get_user_by_username(db, user=username) is not None :
        #user_dict_all = get_user_by_username(db, username) #: models.API_UsersT =
        #only_user = schemas.UserInDB(user_dict_all)
        db_user_info: schemas.UserInDB = get_user_by_username(db, username)
        return db_user_info #schemas.UserInDB(only_user)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password): #user.hashed_password
        return False
    return user

####################################################
#last ID_Actividad
def get_last_actividad(db: Session):
    return db.query(models.ActividadesVacasT).order_by(models.ActividadesVacasT.ID_Actividad.desc()).first()

#actividades_vacas
def reg_actividades_vacas(db: Session, av: schemas.ActInfo):
    reg_av = models.ActividadesVacasT(ID_VACA=av.ID_VACA, ID_TipoOperacion=av.ID_TipoOperacion, ID_Resultado=av.ID_Resultado,
                                      ID_OPERARIO=av.ID_OPERARIO, ID_Categoria=av.ID_Categoria, Fecha=av.Fecha, Comentario=av.Comentario)  
    db.add(reg_av)
    db.commit()
    db.refresh(reg_av)
    return reg_av


def get_act_vacas(db: Session, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), vaca:Optional[str]=None, operacion:Optional[int]=None, operario:Optional[int]=None, id_cliente: str = 0) : 
    filtros=[]
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    filtros.append(func.DATE(models.ActividadesVacasT.Fecha) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.ActividadesVacasT.Fecha) <= datetime.strptime(date2,'%Y-%m-%d').date())    
    if vaca:
        filtros.append((models.ActividadesVacasT.ID_VACA == vaca))
    if operacion:
        filtros.append((models.ActividadesVacasT.ID_TipoOperacion == operacion))
    if operario:
        filtros.append((models.ActividadesVacasT.ID_OPERARIO == operario))
    return db.query(models.ActividadesVacasT).join(models.VacasT).filter(*filtros).all()
    
    
def get_act_mastitis(db: Session, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), vaca:Optional[str]=None, operacion:Optional[int]=None, operario:Optional[int]=None, id_cliente: str = 0) : # 
    filtros=[]
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    filtros.append(func.DATE(models.ActividadesVacasT.Fecha) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.ActividadesVacasT.Fecha) <= datetime.strptime(date2,'%Y-%m-%d').date())    
    if vaca:
        filtros.append((models.ActividadesVacasT.ID_VACA == vaca))
    if operacion:
        filtros.append((models.ActividadesVacasT.ID_TipoOperacion == operacion))
    if operario:
        filtros.append((models.ActividadesVacasT.ID_OPERARIO == operario))
    return db.query(models.MastitisT).join(models.ActividadesVacasT).join(models.VacasT).filter(*filtros).all()  


#masti 2
def reg_acti_2(db: Session, data: schemas.Mast_Requi):
    reg_av = models.ActividadesVacasT(ID_VACA=data.ID_VACA, ID_TipoOperacion=data.ID_TipoOperacion, ID_Resultado=data.ID_Resultado,
                                      ID_OPERARIO=data.ID_OPERARIO, ID_Categoria=data.ID_Categoria, Fecha=data.Fecha, Comentario=data.Comentario)  
    db.add(reg_av)
    db.commit()
    db.refresh(reg_av)
    return reg_av

#correccion de valor de pezones, para calculo de ubre sana y calificacion
def pez_cor(pez, valids):
        if pez==5: #5 = pezon muerto
            res = None
            cor = None
        elif pez<5 and pez>0: #pezon con valores validos mayor a 0
            res = pez*(1/valids) #valids son los pezones vivos (exceptaundo los muertos)
            cor = 1/valids
        else: #pezones perfectos
            res = 0
            cor =0
        return [res,cor]

def registrar_masti_2(db: Session, data: schemas.Mast_Requi, id_to_use):
    #calculo de calificacion y ubre sana
    valids = 4 - sum(float(num) == 5 for num in [data.AI,data.AD,data.PI,data.PD]) #calculo de pezones validos
    ai_res, ai_cor = pez_cor(data.AI, valids)
    ad_res, ad_cor = pez_cor(data.AD, valids)
    pi_res, pi_cor = pez_cor(data.PI, valids)
    pd_res, pd_cor = pez_cor(data.PD, valids)
    ubre = 1 - sum(filter(None,(ai_cor,ad_cor,pi_cor,pd_cor)))
    cali = 1 - sum(filter(None,(ai_res,ad_res,pi_res,pd_res)))
    gap = ubre - cali
    
    #subida de datos a la API
    reg_mastitis = models.MastitisT(ID_ACTIVIDAD=id_to_use, AI=data.AI, AD=data.AD, PI=data.PI, PD=data.PD, Chequeo_revision=data.Chequeo_revision, 
                                    Ubre_sana=ubre, Calificacion=cali, GAP=gap)
    db.add(reg_mastitis)
    db.commit()
    db.refresh(reg_mastitis)
    return "post_Registrar_mastitis_2"