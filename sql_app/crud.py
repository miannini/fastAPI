# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:17:18 2020

@author: Marcelo
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, inspect
from typing import Optional, List
from . import models, schemas
from datetime import date, datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

##########################

#CRUD = Create, Read, Update and Delete

#to join tables and yield a flat result
def obj_to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

def flatten_join(tup_list):
    return [{**obj_to_dict(a), **obj_to_dict(b)} for a,b in tup_list]

#funcion para unir elementos de tablas, pero quitando variables que no se necesiten de la union
def flatten_join_av(tup_list, avoid):
    old_list = [{**obj_to_dict(a), **obj_to_dict(b)} for a,b in tup_list]
    new_list = [{k: v for k, v in d.items() if k not in avoid} for d in old_list]
    return new_list

### Clientes
def get_clientes(db: Session, ciudad:Optional[str]=None, departamento:Optional[str]=None, nombre:Optional[str]=None, date1: Optional[str]=None, id_cliente:Optional[str]=None): #date1: str = datetime.now().strftime("%Y-%m-%d")
    filtros=[]
    if id_cliente:
        filtros.append(models.ClientesT.ID_CLIENTE == id_cliente)
    if ciudad:
        filtros.append((models.ClientesT.CIUDAD.contains(ciudad)))
    if departamento:
        filtros.append((models.ClientesT.DEPARTAMENTO.contains(departamento)))    
    if nombre:
        filtros.append((models.ClientesT.NOMBRE.contains(nombre)))            
    if date1:
        filtros.append(func.DATE(models.ClientesT.FECHA_CONTRATO) >= datetime.strptime(date1,'%Y-%m-%d').date())
    if len(filtros)>0:
        return db.query(models.ClientesT).filter(*filtros).all()
    else:
        return db.query(models.ClientesT).all()

def create_cliente(db: Session, cliente: schemas.ClientesCreate):
    #cliente2 = cliente.pop('ID_CLIENTE')
    db_cliente = models.ClientesT(**cliente.dict(exclude_unset=True)) #cliente.dict().pop('ID_CLIENTE'))
    #del db_cliente['ID_CLIENTE']
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente
#edit clientes

### Operarios
def get_operarios(db: Session, finca:Optional[str]=None, rol:Optional[str]=None, nombre:Optional[str]=None,  id_cliente: str = 0):
    filtros=[]
    filtros.append(models.OperarioT.ID_CLIENTE == id_cliente)
    if finca:
        filtros.append((models.OperarioT.ID_FINCA == finca))
    if rol:
        filtros.append((models.OperarioT.Rol.contains(rol)))
    if nombre:
        filtros.append((models.OperarioT.NombreOperario.contains(nombre)))   
    return db.query(models.OperarioT).filter(*filtros).all()
    #evaluar si retornar con Usuario API joined

def create_operario(db: Session, operario: schemas.OperarioN):
    db_operario = models.OperarioT(**operario.dict(exclude_unset=True))
    db.add(db_operario)
    db.commit()
    db.refresh(db_operario)
    return db_operario.ID_OPERARIO

def delete_operario(db: Session, id_operario: int): #operario: schemas.OperarioDelete,
    db.query(models.OperarioT).filter(models.OperarioT.ID_OPERARIO == id_operario).delete()
    db.commit()
 
# -- edit operario

### Fincas    
def get_fincas(db: Session, finca:Optional[int]=None, id_cliente: str = 0, nombre:Optional[str]=None):
    filtros=[]
    filtros.append(models.FincaT.ID_cliente == id_cliente)
    if finca:
        filtros.append((models.FincaT.ID_FINCA == finca))
    if nombre:
        filtros.append((models.FincaT.NOMBRE.contains(nombre))) 
    return db.query(models.FincaT).filter(*filtros).all()

def create_finca(db: Session, finca: schemas.FincaP, id_cliente: str = 0): 
    db_finca = models.FincaT(**finca.dict(exclude_unset=True))
    db.add(db_finca)
    db.commit()
    #db.refresh(db_finca)
    return "post_finca=Success"

#-- edit

### Lotes    
def get_lotes(db: Session, id_finca:Optional[int]=None, id_lote:Optional[int]=None, nombre:Optional[str]=None, id_cliente: str = 0):
    filtros=[]
    filtros.append(models.FincaT.ID_cliente == id_cliente)
    if id_finca:
        filtros.append(models.LotesT.ID_FINCA == id_finca)   
    if id_lote:
        filtros.append(models.LotesT.ID_LOTE == id_lote) 
    if nombre:
        filtros.append((models.LotesT.NOMBRE_LOTE.contains(nombre)))            
    #if len(filtros)>0:
    return db.query(models.LotesT).join(models.FincaT).filter(*filtros).all()
    #evaluar si se queire con Finca Joined
    

### ************************************************
#create lote_de_finca
def create_finca_lote(db: Session, lote: schemas.LotesN, finca_id: int):
    db_lote = models.LotesT(**lote.dict(exclude_unset=True))#, ID_FINCA=finca_id)
    db.add(db_lote)
    db.commit()
    db.refresh(db_lote)
    return db_lote

def delete_lote(db: Session, id_lote: int): #operario: schemas.OperarioDelete,
    db.query(models.LotesT).filter(models.LotesT.ID_LOTE == id_lote).delete()
    db.commit()

def update_lote(db: Session, lote: schemas.LotesN, id_lote: int):
    db.query(models.LotesT).filter(models.LotesT.ID_LOTE == id_lote).update(lote.dict(exclude_unset=True))
    db.commit()    
### **************************************************

### Acti Lotes
def get_acti_lotes(db: Session, id_finca:Optional[int]=None, id_lote:Optional[int]=None, nombre_lote:Optional[str]=None, nombre_oper:Optional[str]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), id_cliente: str = 0): #
    filtros=[]
    filtros.append(models.FincaT.ID_cliente == id_cliente)
    filtros.append(models.OperarioT.ID_CLIENTE == id_cliente)
    filtros.append(func.DATE(models.Actividades_LotesT.FECHA_ACTIVIDAD) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.Actividades_LotesT.FECHA_ACTIVIDAD) <= datetime.strptime(date2,'%Y-%m-%d').date()) 
    if id_finca:
        filtros.append(models.LotesT.ID_FINCA == id_finca)   
    if id_lote:
        filtros.append(models.LotesT.ID_LOTE == id_lote) 
    if nombre_lote:
        filtros.append((models.LotesT.NOMBRE_LOTE.contains(nombre_lote)))
    if nombre_oper:
        filtros.append((models.OperarioT.NombreOperario.contains(nombre_oper)))               
    return db.query(models.Actividades_LotesT).join(models.OperarioT).join(models.LotesT).join(models.FincaT).filter(*filtros).all()  
    #evaluar si se quisiera obtener el join completo

def create_acti_lotes(db: Session, ac_lo: schemas.Actividades_LotesT):
    db_ac_lo = models.Actividades_LotesT(**ac_lo.dict(exclude_unset=True))
    db.add(db_ac_lo)
    db.commit()
    #db.refresh(db_ac_lo)
    return "post_acti_lotes=Success"

#update actividades lotes
#cambiar de programada a ejecutada o fechas


 
### Hatos    
def get_hatos(db: Session, id_finca:Optional[int]=None, id_hato:Optional[int]=None, nombre:Optional[str]=None, tipo:Optional[str]=None,  id_cliente: str = 0):
    filtros=[]
    filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
    if id_finca:
        filtros.append((models.HatosT.ID_FINCA == id_finca))
    if id_hato:
        filtros.append((models.HatosT.ID_HATO == id_hato))
    if nombre:
        filtros.append((models.HatosT.Nombre_Hato.contains(nombre))) 
    if tipo:
        filtros.append((models.HatosT.TIPO_Hato.contains(tipo)))
    
    return db.query(models.HatosT).filter(*filtros).all()

def create_hato(db: Session, hato: schemas.HatosP, id_cliente: str = 0): 
    db_hato = models.HatosT(**hato.dict(exclude_unset=True))
    db.add(db_hato)
    db.commit()
    db.refresh(db_hato)
    return db_hato.ID_HATO

# -- edit

### leche hatos
def get_leche_hatos(db: Session, id_hato:Optional[int]=None, id_operario:Optional[int]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), id_cliente: str = 0): 
    filtros=[]
    filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
    if id_operario:
        filtros.append(models.Leche_HatosT.ID_OPERARIO == id_operario)
    if id_hato:
        filtros.append(models.Leche_HatosT.ID_HATO== id_hato)
    filtros.append(func.DATE(models.Leche_HatosT.FECHA_ACTIVIDAD) >= datetime.strptime(date1,'%Y-%m-%d').date())#.isoformat(timespec='milliseconds'))
    filtros.append(func.DATE(models.Leche_HatosT.FECHA_ACTIVIDAD) <= datetime.strptime(date2,'%Y-%m-%d').date())#.isoformat(timespec='milliseconds')) 
    return db.query(models.Leche_HatosT).join(models.HatosT).filter(*filtros).all()

def create_leche_hatos(db: Session, le_ha: schemas.Leche_Hatosi):
    db_le_ha = models.Leche_HatosT(**le_ha.dict(exclude_unset=True))
    db.add(db_le_ha)
    db.commit()
    #db.refresh(db_le_ha)
    return "post_leche_hatos=Success"

#edit leche hatos, solo para admin

### Vacas    
def get_vacas(db: Session, id_vaca:Optional[int]=None, nombre:Optional[str]=None, sexo:Optional[int]=None, raza:Optional[int]=None, activa:Optional[int]=None ,id_cliente: str = 0): #id_finca:Optional[int]=None
    filtros=[]
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    #if id_finca:
    #    filtros.append(models.VacasT.ID_FINCA == id_finca)
    if id_vaca:
        filtros.append(models.VacasT.ID_VACA == id_vaca)
    if nombre:
        filtros.append(models.VacasT.Nombre_Vaca.contains(nombre)) 
    if sexo:
        filtros.append(models.VacasT.Sexo == sexo)
    if raza:
        filtros.append(models.VacasT.Raza == raza)
    if activa==1:
        filtros.append(models.VacasT.FechaSalida.is_(None))
    return db.query(models.VacasT).filter(*filtros).all()
    
def create_vaca(db: Session, wr_va: schemas.VacaN, id_cliente: str = 0): 
    wr_va.ID_CLIENTE = int(id_cliente)
    db_vaca = models.VacasT(**wr_va.dict(exclude_unset=True))
    db.add(db_vaca)
    db.commit()
    db.refresh(db_vaca)
    return db_vaca.ID_VACA

def update_vaca(db: Session, vaca: schemas.VacaN, id_vaca: int):
    db.query(models.VacasT).filter(models.VacasT.ID_VACA == id_vaca).update(vaca.dict(exclude_unset=True))
    db.commit() 
    
 
### raza
def get_razas(db: Session, id_raza:Optional[int]=None, nombre:Optional[str]=None, codigo:Optional[str]=None):
    filtros=[]
    if id_raza:
        filtros.append(models.razaT.ID_RAZA == id_raza)
    if nombre:
        filtros.append(models.razaT.Nombre.contains(nombre)) 
    if codigo:
        filtros.append(models.razaT.Codigo.contains(codigo))
    if len(filtros)>0:
        return db.query(models.razaT).filter(*filtros).all()
    else:
        return db.query(models.razaT).all()  

    
### sexo
def get_sexo(db: Session, id_sexo:Optional[int]=None, nombre:Optional[str]=None, codigo:Optional[str]=None):
    filtros=[]
    if id_sexo:
        filtros.append(models.sexoT.idSexo == id_sexo)
    if nombre:
        filtros.append(models.sexoT.Nombre.contains(nombre)) 
    if codigo:
        filtros.append(models.sexoT.Codigo.contains(codigo)) 
    if len(filtros)>0:
        return db.query(models.sexoT).filter(*filtros).all()
    else:
        return db.query(models.sexoT).all() 
    

### Tipo_Destino
def get_t_destino(db: Session, id_destino:Optional[int]=None, nombre:Optional[str]=None):
    filtros=[]
    if id_destino:
        filtros.append(models.tipo_destinoT.IDTipo_Destino == id_destino)
    if nombre:
        filtros.append(models.tipo_destinoT.Nombre.contains(nombre)) 
    if len(filtros)>0:
        return db.query(models.tipo_destinoT).filter(*filtros).all()
    else:
        return db.query(models.tipo_destinoT).all() 

### tipo de operaciones    
def get_t_operacion(db: Session, id_tipo:Optional[int]=None, nombre:Optional[str]=None, codigo:Optional[str]=None):
    filtros=[]
    if id_tipo:
        filtros.append(models.tipo_operacionesT.ID_TipoOperaciones == id_tipo)
    if nombre:
        filtros.append(models.tipo_operacionesT.Nombre.contains(nombre)) 
    if codigo:
        filtros.append(models.tipo_operacionesT.Codigo.contains(codigo)) 
    if len(filtros)>0:
        return db.query(models.tipo_operacionesT).filter(*filtros).all()
    else:
        return db.query(models.tipo_operacionesT).all() 

### Actividades_vacas_categoria
def get_av_categoria(db: Session, id_cat:Optional[int]=None, nombre:Optional[str]=None):
    filtros=[]
    if id_cat:
        filtros.append(models.Actividades_vacas_categoriaT.ID_Categoria == id_cat)
    if nombre:
        filtros.append(models.Actividades_vacas_categoriaT.Nombre.contains(nombre)) 
    if len(filtros)>0:
        return db.query(models.Actividades_vacas_categoriaT).filter(*filtros).all()
    else:
        return db.query(models.Actividades_vacas_categoriaT).all() 
    
### Actividades_vacas_resultado
def get_av_resultado(db: Session, id_res:Optional[int]=None, nombre:Optional[str]=None):
    filtros=[]
    if id_res:
        filtros.append(models.Actividades_vacas_resultadoT.ID_Resutlado == id_res)
    if nombre:
        filtros.append(models.Actividades_vacas_resultadoT.Nombre.contains(nombre)) 
    if len(filtros)>0:
        return db.query(models.Actividades_vacas_resultadoT).filter(*filtros).all()
    else:
        return db.query(models.Actividades_vacas_resultadoT).all() 


    
### leche vaca
def get_leche_vacas(db: Session, id_vaca:Optional[int]=None, id_operario:Optional[int]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), id_cliente: str = 0):
    filtros=[]
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    if id_operario:
        filtros.append(models.Leche_VacaT.ID_OPERARIO == id_operario)
    if id_vaca:
        filtros.append(models.Leche_VacaT.ID_VACA == id_vaca)
    filtros.append(func.DATE(models.Leche_VacaT.FECHA) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.Leche_VacaT.FECHA) <= datetime.strptime(date2,'%Y-%m-%d').date()) 
    return db.query(models.Leche_VacaT).join(models.VacasT).filter(*filtros).all()
    

def create_leche_vacas(db: Session, le_va: schemas.Leche_Vacai):
    db_le_va = models.Leche_VacaT(**le_va.dict(exclude_unset=True))
    db.add(db_le_va)
    db.commit()
    #db.refresh(db_le_va)
    return "post_leche_vacas=Success"

def create_leche_vaca_list(db: Session, le_va: List[schemas.Leche_VacaT]):
    db_le_va = []
    for dictio in le_va:
        db_le_va.append(models.Leche_VacaT(**dictio.dict(exclude_unset=True)))
    db.bulk_save_objects(db_le_va)
    db.commit()
    #db.refresh(db_le_va)
    return "post_leche_vacas_list=Success"

#edit solo para admins

### meteorologia
def registrar_meteo(db: Session, meteo: schemas.MeteorologiaT):
    reg_meteo = models.MeteorologiaT(**meteo.dict())
    db.add(reg_meteo)
    db.commit()
    db.refresh(reg_meteo)
    return reg_meteo

def get_meteo(db: Session, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), finca:Optional[str]=None, id_cliente: str = 0) : 
    filtros=[]
    filtros.append(models.MeteorologiaT.ID_CLIENTE == id_cliente)
    filtros.append(func.DATE(models.MeteorologiaT.FECHA_HORA) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.MeteorologiaT.FECHA_HORA) <= datetime.strptime(date2,'%Y-%m-%d').date())    
    if finca:
        filtros.append((models.MeteorologiaT.ID_FINCA == finca))
    return db.query(models.MeteorologiaT).filter(*filtros).all()


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

def get_all_users(db: Session, full_name: Optional[str]=None, email: Optional[str]=None, active_status: Optional[int]=None,  user_rol: Optional[int]=None, operario: Optional[int]=None, id_cliente: str = 0):
    filtros=[]
    filtros.append(models.API_UsersT.ID_CLIENTE == id_cliente)
    if operario:
        filtros.append(models.API_UsersT.ID_OPERARIO == operario)
    if active_status:
        filtros.append(models.API_UsersT.active_status == active_status)
    if user_rol:
        filtros.append(models.API_UsersT.id_user_rol == user_rol)
    if full_name:
        filtros.append(models.API_UsersT.full_name.contains(full_name))
    if email:
        filtros.append(models.API_UsersT.email.contains(email))
    return db.query(models.API_UsersT).filter(*filtros).all()

def create_user(db: Session, user_t: schemas.UserCreate):
    #hashed_password = bcrypt.hashpw(user_t.password.encode('utf-8'), bcrypt.gensalt())
    hashed_password = pwd_context.hash(user_t.password)
    db_user = models.API_UsersT(user=user_t.user, password=hashed_password, full_name=user_t.full_name, email=user_t.email, ID_CLIENTE=user_t.ID_CLIENTE)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_t: schemas.User, username: str):
    db.query(models.API_UsersT).filter(models.API_UsersT.user == username).update(user_t.dict(exclude_unset=True))
    db.commit() 
    
########################################
### secure users
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

#change pswd o change email

#get_all_privs
def get_all_privs(db: Session, name:Optional[int]=None, description:Optional[str]=None):
    filtros=[]
    if name:
        filtros.append(models.API_Users_PrivT.name.contains(name))
    if description:
        filtros.append(models.API_Users_PrivT.description.contains(description)) 
    if len(filtros)>0:
        return db.query(models.API_Users_PrivT).filter(*filtros).all()
    else:
        return db.query(models.API_Users_PrivT).all() 

####################################################
#last ID_Actividad
'''
def get_last_actividad(db: Session):
    return db.query(models.ActividadesVacasT).order_by(models.ActividadesVacasT.ID_Actividad.desc()).first()
'''


### Obtener actividades_vacas Mastitis
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
    
'''    
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
'''

#solution to join tables
#https://stackoverflow.com/questions/27280862/sqlalchemy-getting-a-single-object-from-joining-multiple-tables/60883545#60883545?newreg=418bba09a46f4fe5b0b02ab0e8514acc
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
    res = db.query(models.MastitisT, models.ActividadesVacasT).join(models.ActividadesVacasT).join(models.VacasT).filter(*filtros).all()  
    #remover ID_TipoOperacion, ID_Resultado, ID_Categoria, ID_Actividad
    avoid = ['ID_TipoOperacion', 'ID_Resultado', 'ID_Categoria', 'ID_Actividad']
    res_b = flatten_join_av(res, avoid) #res_b = flatten_join(res)
    
    return res_b


    
    
### Registrar Actividad - cualquiera
def reg_acti_2(db: Session, data: schemas.ActInfo): #Mast_Requi
    reg_av = models.ActividadesVacasT(ID_VACA=data.ID_VACA, ID_TipoOperacion=data.ID_TipoOperacion, ID_Resultado=data.ID_Resultado,
                                      ID_OPERARIO=data.ID_OPERARIO, ID_Categoria=data.ID_Categoria, Fecha=data.Fecha, Comentario=data.Comentario)  
    db.add(reg_av)
    db.commit()
    db.refresh(reg_av)
    return reg_av

### calificacion de pezones
def pez_cor(pez, valids): #correccion de valor de pezones, para calculo de ubre sana y calificacion
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

### registrar mastitis
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


### partos
def get_act_partos(db: Session, date1: str = '2000-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), vaca:Optional[str]=None, categoria:Optional[int]=None, operario:Optional[int]=None, comentario:Optional[str]=None, id_cliente: str = 0) : # 
    filtros=[]
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    filtros.append(func.DATE(models.ActividadesVacasT.Fecha) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.ActividadesVacasT.Fecha) <= datetime.strptime(date2,'%Y-%m-%d').date())    
    if vaca:
        filtros.append((models.ActividadesVacasT.ID_VACA == vaca))
    if categoria:
        filtros.append((models.ActividadesVacasT.ID_Categoria == categoria))
    if operario:
        filtros.append((models.ActividadesVacasT.ID_OPERARIO == operario))
    if comentario:
        filtros.append((models.ActividadesVacasT.Comentario.contains(comentario)))
    res = db.query(models.PartosT, models.ActividadesVacasT).join(models.ActividadesVacasT).join(models.VacasT).filter(*filtros).all()  
    #remover ID_TipoOperacion, ID_Resultado, ID_Categoria, ID_Actividad
    avoid = ['ID_TipoOperacion', 'ID_Resultado', 'ID_Actividad']
    res_b = flatten_join_av(res, avoid) #res_b = flatten_join(res)
    return res_b

def get_solo_partos(db: Session, date1: str = '2000-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), vaca:Optional[str]=None, idparto:Optional[int]=None, idactividad:Optional[int]=None, id_cliente: str = 0) : # 
    filtros=[]
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    filtros.append(func.DATE(models.ActividadesVacasT.Fecha) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.ActividadesVacasT.Fecha) <= datetime.strptime(date2,'%Y-%m-%d').date())   
    if vaca:
        filtros.append((models.PartosT.ID_VACA == vaca))
    if idparto:
        filtros.append((models.PartosT.IDparto == idparto))
    if idactividad:
        filtros.append((models.PartosT.ID_actividad == idactividad))
    res = db.query(models.PartosT).join(models.ActividadesVacasT).join(models.VacasT).filter(*filtros).all()  
    return res

def get_max_partos(db: Session, vaca:Optional[str]=None, id_cliente: str = 0):
    filtros=[]
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    if vaca:
        filtros.append((models.PartosT.ID_VACA == vaca))
    res = db.query(models.PartosT.ID_VACA.label('ID_VACA'), func.max(models.PartosT.Numero_Parto).label('max_partos')).group_by(models.PartosT.ID_VACA).join(models.VacasT).filter(*filtros).all()
    res_b =  [r._asdict() for r in res] 
    return  res_b 

### Registrar Partos
def registrar_parto(db: Session, data: schemas.Parto_Requi, id_to_use, numero):
    #subida de datos a la API
    reg_parto = models.PartosT(ID_VACA=data.ID_VACA, Numero_Parto=numero, Sire=data.Sire, ID_ACTIVIDAD=id_to_use) #IDparto=0, 
    db.add(reg_parto)
    db.commit()
    db.refresh(reg_parto)
    return reg_parto

### Ubicacion vacas  
def get_ubva(db: Session, id_vaca:Optional[str]=None, id_hato:Optional[str]=None, id_lote:Optional[str]=None, id_cliente: str = 0):
    filtros=[]
    filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    if id_hato:
        filtros.append(models.Ubicacion_VacasT.ID_HATO == id_hato)
    if id_vaca:
        filtros.append(models.Ubicacion_VacasT.ID_VACA == id_vaca)
    if id_lote:
        filtros.append(models.Ubicacion_VacasT.ID_LOTE == id_lote)
    return db.query(models.Ubicacion_VacasT).join(models.HatosT).join(models.VacasT).filter(*filtros).all() #


### Traslado vacas    
def write_ubi_vaca(db: Session, sch_ubi: schemas.Ubicacion_VacasT, id_cliente: str = 0):
    reg_uv = models.Ubicacion_VacasT(**sch_ubi.dict())#(ID_VACA=sch_ubi.ID_VACA, ID_HATO=sch_ubi.ID_HATO, ID_LOTE=id_lote)   
    db.add(reg_uv)
    db.commit()
    db.refresh(reg_uv)
    return reg_uv


def update_ubica_vaca(db: Session, sch_ubi: schemas.Ubicacion_VacasT, id_cliente: str = 0): #vaca:Optional[str]=None
    filtros=[]
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
    filtros.append(models.Ubicacion_VacasT.ID_VACA == sch_ubi.ID_VACA)
    data = db.query(models.Ubicacion_VacasT).join(models.VacasT).join(models.HatosT).filter(*filtros).all()
    if len(data) > 0:
        db.query(models.Ubicacion_VacasT).filter(models.Ubicacion_VacasT.ID_VACA == sch_ubi.ID_VACA).update(sch_ubi.dict(exclude_unset=True)) #(ID_VACA=sch_ubi.ID_VACA, ID_HATO=sch_ubi.ID_HATO, ID_LOTE=id_lote) 
        db.commit() 
        return "ok"
 
def write_trasvaca(db: Session, sch_ubi: schemas.Ubicacion_VacasT, Fecha_Traslado : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id_cliente: str = 0):
    reg_tv = models.Traslado_VacasT(ID_VACA=sch_ubi.ID_VACA, Fecha_Traslado=Fecha_Traslado, ID_HATO=sch_ubi.ID_HATO)  
    db.add(reg_tv)
    db.commit()
    db.refresh(reg_tv)
    return reg_tv

def get_trasvaca(db: Session, id_vaca:Optional[str]=None, id_hato:Optional[str]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), id_cliente: str = 0):
    filtros=[]
    filtros.append(func.DATE(models.Traslado_VacasT.Fecha_Traslado) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.Traslado_VacasT.Fecha_Traslado) <= datetime.strptime(date2,'%Y-%m-%d').date()) 
    if id_hato:
        filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
        filtros.append(models.Traslado_VacasT.ID_HATO == id_hato)
    if id_vaca:
        filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
        filtros.append(models.Traslado_VacasT.ID_VACA == id_vaca)
    return db.query(models.Traslado_VacasT).join(models.HatosT).join(models.VacasT).filter(*filtros).all()


### traslado hatos
def update_ubica_hato(db: Session, sch_ubi: schemas.Ubicacion_VacasBasic, id_cliente: str = 0): #vaca:Optional[str]=None
    filtros=[]
    filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
    filtros.append(models.FincaT.ID_cliente == id_cliente)
    filtros.append(models.LotesT.ID_LOTE == sch_ubi.ID_LOTE)
    filtros.append(models.Ubicacion_VacasT.ID_HATO == sch_ubi.ID_HATO)
    data = db.query(models.Ubicacion_VacasT).join(models.HatosT).join(models.FincaT).join(models.LotesT).filter(*filtros).all()
    if len(data) > 0:
        db.query(models.Ubicacion_VacasT).filter(models.Ubicacion_VacasT.ID_HATO == sch_ubi.ID_HATO).update(sch_ubi.dict(exclude_unset=True))
        db.commit() 
        return "ok"

def write_trashato(db: Session, sch_ubi: schemas.Ubicacion_VacasBasic, Fecha_Traslado : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id_cliente: str = 0):
    reg_th = models.Traslado_HatosT(ID_HATO=sch_ubi.ID_HATO, Fecha_Traslado=Fecha_Traslado, ID_LOTE=sch_ubi.ID_LOTE)  
    db.add(reg_th)
    db.commit()
    db.refresh(reg_th)
    return reg_th

def get_trashato(db: Session, id_hato:Optional[str]=None, id_lote:Optional[str]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), id_cliente: str = 0):
    filtros=[]
    filtros.append(func.DATE(models.Traslado_HatosT.Fecha_Traslado) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.Traslado_HatosT.Fecha_Traslado) <= datetime.strptime(date2,'%Y-%m-%d').date()) 
    if id_hato:
        filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
        filtros.append(models.Traslado_HatosT.ID_HATO == id_hato)
    if id_lote:
        filtros.append(models.FincaT.ID_cliente == id_cliente)
        filtros.append(models.LotesT.ID_LOTE == id_lote)
        filtros.append(models.Traslado_HatosT.ID_LOTE == id_lote)
    return db.query(models.Traslado_HatosT).join(models.HatosT).join(models.FincaT).join(models.LotesT).filter(*filtros).all()

# Variables de Lotes [Remote Sensing]
def create_lotes_var(db: Session, lo_va: List[schemas.Lotes_variablesT]):
    db_lo_va = []
    for dictio in lo_va:
        db_lo_va.append(models.Lotes_variablesT(**dictio.dict(exclude_unset=True)))
    #db_lo_va = List[models.Lotes_variablesT(**lo_va.dict(exclude_unset=True))]
    #db.add(db_lo_va)
    db.bulk_save_objects(db_lo_va)
    db.commit()
    #db.refresh(db_le_va)
    return "post_lotes_variables=Success"

#get

def create_lotes_qui(db: Session, lo_qu: List[schemas.Lotes_quimicosT]):
    db_lo_qu = []
    for dictio in lo_qu:
        db_lo_qu.append(models.Lotes_quimicosT(**dictio.dict(exclude_unset=True)))
    #db_lo_qu = models.Lotes_quimicosT(**lo_qu.dict(exclude_unset=True))
    #db.add(db_lo_qu)
    db.bulk_save_objects(db_lo_qu)
    db.commit()
    #db.refresh(db_le_va)
    return "post_lotes_quimicos=Success"

#get

def create_moni_des(db: Session, mo_des: schemas.monitoreo_descargas_sentinelT):
    db_mo_des = models.monitoreo_descargas_sentinelT(**mo_des.dict(exclude_unset=True))
    db.add(db_mo_des)
    db.commit()
    #db.refresh(db_le_va)
    return "post_monitoreo_descargas=Success"

#get