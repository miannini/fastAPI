# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:17:18 2020

@author: Marcelo
"""
from fastapi import HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, inspect, select, join
from typing import Optional, List, Union
from . import models, schemas, secrets
#import models, schemas, secrets
from datetime import date, datetime
from passlib.context import CryptContext
import os
import pandas as pd
#SMS
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
#Emails
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email
from python_http_client.exceptions import HTTPError
import itertools
from api_folder.encrypt import decrypt
import re


# Twilio Details
NUMBER = decrypt(str.encode(os.getenv('NUMBER')), secrets.key).decode()
SID = decrypt(str.encode(os.getenv('SID')), secrets.key).decode()
TOKEN = decrypt(str.encode(os.getenv('TOKEN')), secrets.key).decode()


#################################################   FUNCIONES   ###########################################################
#encryption
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#to join tables and yield a flat result
def obj_to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

def flatten_join(tup_list):
    return [{**obj_to_dict(a), **obj_to_dict(b)} for a,b in tup_list]

#funcion para unir elementos de tablas, pero quitando variables que no se necesiten de la union
def flatten_join_av(tup_list, avoid):
    print(len(tup_list[0]))
    old_list = [{**obj_to_dict(a), **obj_to_dict(b)} for a, b in tup_list]
    #old_list = [ [{}.update(**obj_to_dict(n)) for n in tup_list[l]] for l in range(len(tup_list))]
    print(old_list)
    new_list = [{k: v for k, v in d.items() if k not in avoid} for d in old_list]
    return new_list

#Funcion para enviar emails a My Kau por creacion de cliente
def email_cliente(alpha, fecha):
    sg = SendGridAPIClient(secrets.EMAIL_API_KEY) #.environ['EMAIL_API_KEY'])
    html_content1 = "<p>ALERT - New registered Client!</p>" + "<p>This email is to Alert for new Client for My Kau App. New ID = " + str(alpha.ID_CLIENTE) + ".</p> <p>"
    html_content2 = "Name is = " + str(alpha.NOMBRE) + " , eMail is = " + str(alpha.EMAIL) +  " , Company is = " + str(alpha.RAZON_SOCIAL) + " , Phone is = " + str(alpha.TELEFONO)
    html_content3 = "</p>" + "<p>Registered on = " + str(fecha) + "</p>"
    html_content = html_content1 + html_content2 + html_content3
                    
    message = Mail(
      to_emails=["jgarboleda@gmail.com", "juancacamacho89@gmail.com", "luchofelipe8023@gmail.com", "marceloiannini@hotmail.com", "nickair90@gmail.com"],
      #bcc_emails="mianninig@gmail.com",
      from_email=Email('mianninig@gmail.com', "MyKau Monitor_Report"),
      subject="New Client [AUTO ALERT] - MyKau",
      html_content=html_content
      )
    #message.add_bcc("mianninig@gmail.com","minds4analytics@gmail.com","salsandres22@gmail.com")

    try:
      response = sg.send(message)
      return f"email.status_code={response.status_code}"
      #expected 202 Accepted
    except HTTPError as e:
      return e.message 

#Funcion para enviar emails a clientes, por creacion de usuarios
def email_user(alpha, tomail, fecha):
    sg = SendGridAPIClient(secrets.EMAIL_API_KEY) #.environ['EMAIL_API_KEY'])
    html_content1 = "<p>ALERTA - Nuevo usuario registrado a su Cuenta de Cliente!</p>" + "<p>Un nuevo usuario se ha registrado con su Numero de Cliente, en MyKau App. Nuevo User_ID = " + str(alpha.user) + ".</p> <p>"
    html_content2 = "Nombre = " + str(alpha.full_name) + " , e-mail = " + str(alpha.email)
    html_content3 = "</p>" + "<p>Fecha de Registro = " + str(fecha) + "</p>"
    html_content4 = "</p> si conoce este usuario, ingrese a MyKauApp, active la cuenta del usuario y asocie con el Operario correspondiente en caso de ser necesario</p>"
    html_content = html_content1 + html_content2 + html_content3 + html_content4
                    
    message = Mail(
      to_emails= [str(tomail)],#["jgarboleda@gmail.com", "juancacamacho89@gmail.com", "luchofelipe8023@gmail.com", "marceloiannini@hotmail.com", "nickair90@gmail.com"],
      #cc_emails=Cc("marceloiannini@hotmail.com"),
      from_email=Email('mianninig@gmail.com', "MyKau User_Report"),
      subject="New User [AUTO ALERT] - MyKau",
      html_content=html_content
      )

    try:
      response = sg.send(message)
      return f"email.status_code={response.status_code}"
      #expected 202 Accepted
    except HTTPError as e:
      return e.message

#Funcion para enviar emails a clientes, por creacion de usuarios
def email_user_initial(alpha, fecha):
    sg = SendGridAPIClient(secrets.EMAIL_API_KEY) #.environ['EMAIL_API_KEY'])
    html_content1 = "<p>ALERTA - Nuevo usuario registrado a su Cuenta de Cliente!</p>" + "<p>Un nuevo usuario se ha registrado con su Numero de Cliente, en MyKau App. Nuevo User_ID = " + str(alpha.user) + ".</p> <p>"
    html_content2 = "Nombre = " + str(alpha.full_name) + " , e-mail = " + str(alpha.email)
    html_content3 = "</p>" + "<p>Fecha de Registro = " + str(fecha) + "</p>"
    html_content4 = "</p> si conoce este usuario, ingrese a MyKauApp, active la cuenta del usuario y asocie con el Operario correspondiente en caso de ser necesario</p>"
    html_content = html_content1 + html_content2 + html_content3 + html_content4
                    
    message = Mail(
      to_emails= ["jgarboleda@gmail.com", "juancacamacho89@gmail.com", "luchofelipe8023@gmail.com", "marceloiannini@hotmail.com", "nickair90@gmail.com"],#["jgarboleda@gmail.com", "juancacamacho89@gmail.com", "luchofelipe8023@gmail.com", "marceloiannini@hotmail.com", "nickair90@gmail.com"],
      #cc_emails=Cc("marceloiannini@hotmail.com"),
      from_email=Email('mianninig@gmail.com', "MyKau User_Report"),
      subject="New Initial User for New Client [AUTO ALERT] - MyKau",
      html_content=html_content
      )

    try:
      response = sg.send(message)
      return f"email.status_code={response.status_code}"
      #expected 202 Accepted
    except HTTPError as e:
      return e.message    


def email_celo(alpha, tomail, fecha):
    sg = SendGridAPIClient(secrets.EMAIL_API_KEY) #.environ['EMAIL_API_KEY'])
    html_content1 = "<p>ALERTA - Celo Detectado!</p>" + "<p>Un nuevo usuario se ha registrado con su Numero de Cliente, en MyKau App. Nuevo User_ID = " + str(alpha.user) + ".</p> <p>"
    html_content2 = "Vaca = " + str(alpha.ID_Vaca) + " , celotron = " + str(alpha.id_celotron)
    html_content3 = "</p>" + "<p>Fecha de Registro = " + str(fecha) + "</p>"
    html_content4 = "</p> mensaje personalizado para intervenir en deteccion de celo</p>"
    html_content = html_content1 + html_content2 + html_content3 + html_content4
                    
    message = Mail(
      to_emails= [str(tomail)], # to_emails= ["jgarboleda@gmail.com", "juancacamacho89@gmail.com", "luchofelipe8023@gmail.com", "marceloiannini@hotmail.com", "nickair90@gmail.com"],#["jgarboleda@gmail.com", "juancacamacho89@gmail.com", "luchofelipe8023@gmail.com", "marceloiannini@hotmail.com", "nickair90@gmail.com"],
      #cc_emails=Cc("marceloiannini@hotmail.com"),
      from_email=Email('mianninig@gmail.com', "MyKau User_Report"),
      subject="Deteccion de Celo [AUTO ALERT] - MyKau",
      html_content=html_content
      )

    try:
      response = sg.send(message)
      return f"email.status_code={response.status_code}"
      #expected 202 Accepted
    except HTTPError as e:
      return e.message


    
#######################     USERS   ###################################################
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
    #get client email
    cliente = get_clientes(db, id_cliente=user_t.ID_CLIENTE)
    if len(cliente) >0:
        cliente_mail = obj_to_dict(cliente[0])["EMAIL"]
        print(cliente_mail)
        db_user = models.API_UsersT(user=user_t.user, password=hashed_password, full_name=user_t.full_name, email=user_t.email, ID_CLIENTE=user_t.ID_CLIENTE)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        #if initial user, send to mykau, else to client
        list_users = get_all_users(id_cliente=user_t.ID_CLIENTE)
        if len(list_users)>0:
            #send a notification
            email_user(db_user, cliente_mail, datetime.now().strftime("%Y-%m-%d"))
        else:
            #send a notification
            email_user_initial(db_user, datetime.now().strftime("%Y-%m-%d"))
        return db_user
    else:
        raise HTTPException(status_code=404, detail="Cliente not found")

def update_user(db: Session, user_t: schemas.User, username: str):
    db.query(models.API_UsersT).filter(models.API_UsersT.user == username).update(user_t.dict(exclude_unset=True))
    db.commit() 
    
### secure users
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    if get_user_by_username(db, user=username) is not None :
        db_user_info: schemas.UserInDB = get_user_by_username(db, username)
        return db_user_info

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
    if len(filtros) == 0:
        filtros.append(True)
    return db.query(models.API_Users_PrivT).filter(*filtros).all()

#get_all_permisos
def get_permisos(db: Session, name:Optional[int]=None, user:Optional[int]=None, id_cliente:Optional[str]=None):
    filtros=[]
    if name:
        filtros.append(models.API_UsersT.name.contains(name))
    if user:
        filtros.append(models.PermisosT.User_ID == user)
    if len(filtros) == 0:
        filtros.append(True)
    return db.query(models.PermisosT).join(models.API_UsersT).filter(*filtros).all()

#patch
def update_permiso(db: Session, permiso: schemas.PermisosU, user_id: int):
    db.query(models.PermisosT).filter(models.PermisosT.User_ID == user_id).update(permiso.dict(exclude_unset=True))
    db.commit()

def get_fincas_user(db: Session, user_id: int, id_cliente:Optional[str]=None):
    filtros=[]
    filtros.append(models.API_Users_FincasT.ID_user == user_id)
    if id_cliente:
        filtros.append(models.API_UsersT.ID_CLIENTE == id_cliente)
    return db.query(models.API_Users_FincasT).join(models.API_UsersT).filter(*filtros).all()

def create_finca_user(db: Session, finca_user: schemas.API_Users_FincasU):
    db_user = models.API_Users_FincasT(**finca_user.dict(exclude_unset=True))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return "post_finca_user=Success"

def update_per_user_finca(db: Session, permiso: schemas.API_Users_FincasU, user_id: int, finca_id:Optional[int]=None):
    filtros =[]
    filtros.append(models.API_Users_FincasT.ID_user == user_id)
    if finca_id:
        filtros.append(models.API_Users_FincasT.ID_FINCA == finca_id)
    db.query(models.API_Users_FincasT).filter(*filtros).update(permiso.dict(exclude_unset=True))
    db.commit()


def get_roles_tablas(db: Session, ID:Optional[int]=None, Rol:Optional[str]=None, method:Optional[str]=None,
                     Permiso:Optional[int]=None):
    filtros=[]
    if ID:
        filtros.append(models.Roles_tablasT.id == ID)
    if Rol:
        filtros.append(models.Roles_tablasT.Rol.contains(Rol))
    if method:
        filtros.append(models.Roles_tablasT.API_method.contains(method))
    if Permiso:
        filtros.append(models.Roles_tablasT.Permiso == Permiso)
    if len(filtros) == 0:
        filtros.append(True)
    return db.query(models.Roles_tablasT).filter(*filtros).all()

def update_roles_tabla(db: Session, roles: schemas.Roles_tablasU, permiso_id: int):
    db.query(models.Roles_tablasT).filter(models.Roles_tablasT.id == permiso_id).update(roles.dict(exclude_unset=True))
    db.commit()

def create_roles_tabla(db: Session, roles: schemas.Roles_tablasU):
    db_roles = models.Roles_tablasT(**roles.dict(exclude_unset=True))
    db.add(db_roles)
    db.commit()
    db.refresh(db_roles)
    return "post_roles_tabla=Success"
###################################################################################################


############################       CLIENTS      ###############################################
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
    if len(filtros) == 0:
        filtros.append(True)
    return db.query(models.ClientesT).filter(*filtros).all()

def create_cliente(db: Session, cliente: schemas.ClientesU):
    #cliente2 = cliente.pop('ID_CLIENTE')
    db_cliente = models.ClientesT(**cliente.dict(exclude_unset=True)) #cliente.dict().pop('ID_CLIENTE'))
    #del db_cliente['ID_CLIENTE']
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    
    #id_cliente2 = pd.DataFrame.from_records([s.__dict__ for s in db_cliente])
    #id_cliente2.reset_index(drop=True, inplace=True)
    #id_cliente = id_cliente2.ID_CLIENTE.mode()
    #actualizar diccionario incluyendo datos del lote
    #id_cliente=int(id_cliente)
    
    email_cliente(db_cliente, datetime.now().strftime("%Y-%m-%d"))
    return db_cliente.ID_CLIENTE
#edit clientes
#patch
def update_cliente(db: Session, cliente: schemas.ClientesU, cliente_id: int):
    db.query(models.ClientesT).filter(models.ClientesT.ID_CLIENTE == cliente_id).update(cliente.dict(exclude_unset=True))
    db.commit()

####################################################################################################


##################################      OPERARIOS    #################################################
### Operarios
def get_operarios(db: Session, finca:Optional[str]=None, id_operario:Optional[str]=None, rol:Optional[str]=None, nombre:Optional[str]=None,  id_cliente: str = 0):
    filtros=[]
    filtros.append(models.OperarioT.ID_CLIENTE == id_cliente)
    if finca:
        filtros.append((models.Operarios_FincasT.ID_FINCA == finca))
    if id_operario:
        filtros.append((models.OperarioT.ID_OPERARIO == id_operario))
    if rol:
        filtros.append((models.OperarioT.Rol.contains(rol)))
    if nombre:
        filtros.append((models.OperarioT.NombreOperario.contains(nombre)))
    
    if finca:
        return db.query(models.OperarioT).outerjoin(models.Operarios_FincasT).filter(*filtros).all()
    else:
        return db.query(models.OperarioT).filter(*filtros).all()
    
    #evaluar si retornar con Usuario API joined

def create_operario(db: Session, operario: schemas.OperarioC):
    db_operario = models.OperarioT(**operario.dict(exclude_unset=True))
    db.add(db_operario)
    db.commit()
    db.refresh(db_operario)
    return db_operario.ID_OPERARIO

def delete_operario(db: Session, id_operario: int): #operario: schemas.OperarioDelete,
    db.query(models.OperarioT).filter(models.OperarioT.ID_OPERARIO == id_operario).delete()
    db.commit()
 
### Operarios sin user App
def get_oper_sin_user(db: Session, nombre:Optional[str]=None,  id_cliente: str = 0):
    filtros=[]
    filtros.append(models.OperarioT.ID_CLIENTE == id_cliente)
    if nombre:
        filtros.append((models.Operario_Sin_UserT.NombreOperario.contains(nombre)))   
    return db.query(models.Operario_Sin_UserT).join(models.OperarioT).filter(*filtros).all()

#patch
def update_operario(db: Session, operario: schemas.OperarioC, id_operario: int):
    db.query(models.OperarioT).filter(models.OperarioT.ID_OPERARIO == id_operario).update(operario.dict(exclude_unset=True))
    db.commit()

#add fincas de operario
#update fincas de operario
##########################################################################################################


#################################     FINCAS     #########################################################  
def get_fincas(db: Session, id_finca: Union[List[int], None] = Query(default=None), id_cliente: str = 0,
               nombre:Optional[str]=None):
    filtros=[]
    filtros.append(models.FincaT.ID_cliente == id_cliente)
    if id_finca:
        filtros.append((models.FincaT.ID_FINCA.in_(id_finca)))
    if nombre:
        filtros.append((models.FincaT.NOMBRE.contains(nombre))) 
    return db.query(models.FincaT).filter(*filtros).all()

def create_finca(db: Session, finca: schemas.FincaP, id_cliente: str = 0): 
    db_finca = models.FincaT(**finca.dict(exclude_unset=True))
    db.add(db_finca)
    db.commit()
    db.refresh(db_finca)
    return db_finca.ID_FINCA

#-- edit
def update_finca(db: Session, finca: schemas.FincaU, id_finca: int):
    db.query(models.FincaT).filter(models.FincaT.ID_FINCA == id_finca).update(finca.dict(exclude_unset=True))
    db.commit()
    
###########################################################################################################


###########################################    LOTES    ###################################################
### Lotes    
def get_lotes(db: Session, id_finca: Union[List[int], None] = Query(default=None), id_lote:Optional[int]=None,
              nombre:Optional[str]=None, id_cliente: str = 0):
    filtros=[]
    filtros.append(models.FincaT.ID_cliente == id_cliente)
    if id_finca:
        filtros.append((models.FincaT.ID_FINCA.in_(id_finca)))
    if id_lote:
        filtros.append(models.LotesT.ID_LOTE == id_lote) 
    if nombre:
        filtros.append((models.LotesT.NOMBRE_LOTE.contains(nombre)))
    return db.query(models.LotesT).join(models.FincaT).filter(*filtros).all()
    #evaluar si se queire con Finca Joined
    
#create lote_de_finca
def create_finca_lote(db: Session, lote: schemas.LotesN, finca_id: int):
    db_lote = models.LotesT(**lote.dict(exclude_unset=True))#, ID_FINCA=finca_id)
    db.add(db_lote)
    db.commit()
    db.refresh(db_lote)
    return db_lote.ID_LOTE

def delete_lote(db: Session, id_lote: int): #operario: schemas.OperarioDelete,
    db.query(models.LotesT).filter(models.LotesT.ID_LOTE == id_lote).delete()
    db.commit()

def update_lote(db: Session, lote: schemas.LotesN, id_lote: int):
    db.query(models.LotesT).filter(models.LotesT.ID_LOTE == id_lote).update(lote.dict(exclude_unset=True))
    db.commit()    
'''    
def update_lote2(db: Session, lote: List[schemas.LotesPasto], id_cliente: str = 0):
    #filtros=[]
    #filtros.append(models.FincaT.ID_cliente == id_cliente)
    #db_up_lot = []
    for dictio in lote:
        #db_up_lot.append(models.LotesT(**dictio.dict(exclude_unset=True))) #.join(models.FincaT).filter(*filtros)
        db.bulk_update_mappings(models.LotesT,**dictio.dict(exclude_unset=True))
    db.commit()
    return "patch_update_lotes = success" 
'''    


### Tipo_cultivo Lotes    
def get_tipo_cultivo(db: Session, id_cultivo:Optional[int]=None, nombre:Optional[str]=None, clase:Optional[str]=None, id_cliente: str = 0):
    filtros=[]
    if id_cultivo:
        filtros.append(models.tipo_cultivoT.ID_cultivo == id_cultivo)   
    if nombre:
        filtros.append(models.tipo_cultivoT.nombre.contains(nombre))
    if clase:
        filtros.append((models.tipo_cultivoT.clase.contains(clase)))
    if len(filtros) == 0:
        filtros.append(True)
    return db.query(models.tipo_cultivoT).filter(*filtros).all()

def create_tipo_cultivo(db: Session, tipo: schemas.tipo_cultivoT):
    db_lote = models.tipo_cultivoT(**tipo.dict(exclude_unset=True))
    db.add(db_lote)
    db.commit()
    db.refresh(db_lote)
    return db_lote.ID_cultivo

### variedad_cultivo Lotes    
def get_variedad_cultivo(db: Session, id_variedad:Optional[int]=None, id_cultivo:Optional[int]=None, nombre:Optional[str]=None, id_cliente: str = 0):
    filtros=[]
    if id_variedad:
        filtros.append(models.variedad_cultivoT.ID_variedad == id_variedad)  
    if id_cultivo:
        filtros.append(models.variedad_cultivoT.ID_cultivo == id_cultivo)   
    if nombre:
        filtros.append(models.variedad_cultivoT.nombre.contains(nombre))
    if len(filtros) == 0:
        filtros.append(True)
    return db.query(models.variedad_cultivoT).filter(*filtros).all()


def create_variedad_cultivo(db: Session, variedad: schemas.variedad_cultivoT):
    db_lote = models.variedad_cultivoT(**variedad.dict(exclude_unset=True))
    db.add(db_lote)
    db.commit()
    db.refresh(db_lote)
    return db_lote.ID_variedad

###########################################################################################################


#########################################  ACTIVIDADES LOTES  ############################################
# Acti Lotes
def get_acti_lotes(db: Session, id_finca: Union[List[int], None] = Query(default=None), id_lote:Optional[int]=None,
                   nombre_lote:Optional[str]=None, nombre_oper:Optional[str]=None, date1: str = '2020-01-01',
                   date2: str = datetime.now().strftime("%Y-%m-%d"), id_cliente: str = 0): #
    filtros=[]
    filtros.append(models.FincaT.ID_cliente == id_cliente)
    filtros.append(models.OperarioT.ID_CLIENTE == id_cliente)
    filtros.append(func.DATE(models.Actividades_LotesT.FECHA_ACTIVIDAD) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.Actividades_LotesT.FECHA_ACTIVIDAD) <= datetime.strptime(date2,'%Y-%m-%d').date()) 
    if id_finca:
        filtros.append(models.LotesT.ID_FINCA.in_(id_finca))   #ID_FINCA
    if id_lote:
        filtros.append(models.LotesT.ID_LOTE == id_lote) 
    if nombre_lote:
        filtros.append((models.LotesT.NOMBRE_LOTE.contains(nombre_lote)))
    if nombre_oper:
        filtros.append((models.OperarioT.NombreOperario.contains(nombre_oper)))               
    return db.query(models.Actividades_LotesT).join(models.LotesT).join(models.FincaT).join(models.Operarios_FincasT).join(models.OperarioT).filter(*filtros).all()  
    #evaluar si se quisiera obtener el join completo

def create_acti_lotes(db: Session, ac_lo: schemas.Acti_lotes_post):
    db_ac_lo = models.Actividades_LotesT(**ac_lo.dict(exclude_unset=True))
    db.add(db_ac_lo)
    db.commit()
    #db.refresh(db_ac_lo)
    return "post_acti_lotes=Success"

# Aforo
#crear actividad
def create_acti_lotes2(db: Session, ac_fo: schemas.Actividades_LotesT2):
    '''ac_fo_cop = ac_fo.copy()
    try:
        del ac_fo_cop.Aforo
    except:
        print('Key Aforo is not in the dictionary')
    #ac_fo_cop.pop('Aforo')
    db_ac_lo = models.Actividades_LotesT(**ac_fo_cop.dict(exclude_unset=True))
    '''
    db_ac_lo = models.Actividades_LotesT(ID_LOTE = ac_fo.ID_LOTE, FECHA_ACTIVIDAD = ac_fo.FECHA_ACTIVIDAD, 
                                         ID_Tipo_Actividad = ac_fo.ID_Tipo_Actividad, ID_OPERARIO=ac_fo.ID_OPERARIO)
    db.add(db_ac_lo)
    db.commit()
    db.refresh(db_ac_lo)
    return db_ac_lo

#registrar aforo
def create_acti_aforo(db: Session, ac_fo: schemas.Aforo_Requi, id_to_use):
    #subida de datos a la API
    reg_aforo = models.AforoT(ID_ACTIVIDAD=id_to_use, Aforo=ac_fo.Aforo)
    db.add(reg_aforo)
    db.commit()
    db.refresh(reg_aforo)
    return "post_Registrar_aforo"

### tipo de operaciones  lotes   
def get_tipo_acti_lotes(db: Session):
        return db.query(models.Tipo_Actividades_LotesT).all() 



#Ultimas Actividades Lotes View
def get_ulti_acti_lotes(db: Session, id_finca: Union[List[int], None] = Query(default=None), id_lote:Optional[int]=None,
                        nombre_lote:Optional[str]=None, id_tipo_act:Optional[int]=None, id_cliente: str = 0): #
    filtros=[]
    filtros.append(models.FincaT.ID_cliente == id_cliente) 
    if id_finca:
        filtros.append(models.LotesT.ID_FINCA.in_(id_finca))
    if id_lote:
        filtros.append(models.Ultimas_Act_LotesT.ID_LOTE == id_lote) 
    if nombre_lote:
        filtros.append((models.LotesT.NOMBRE_LOTE.contains(nombre_lote)))
    if id_tipo_act:
        filtros.append(models.Ultimas_Act_LotesT.ID_Tipo_Actividad == id_tipo_act)
    return db.query(models.Ultimas_Act_LotesT).join(models.LotesT).join(models.FincaT).filter(*filtros).all()  
    #evaluar si se quisiera obtener el join completo

    
#update actividades lotes
#cambiar de programada a ejecutada o fechas

###########################################################################################################


########################################    HATOS     ####################################################    
def get_hatos(db: Session, id_finca: Union[List[int], None] = Query(default=None), id_hato:Optional[int]=None,
              nombre:Optional[str]=None, tipo:Optional[str]=None,  id_cliente: str = 0):
    # Optional[int]=None,
    filtros=[]
    filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
    if id_finca:
        filtros.append((models.HatosT.ID_FINCA.in_(id_finca)))
        # filtros.append((models.HatosT.ID_FINCA == id_finca))
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
def update_hato(db: Session, hato: schemas.HatosP, id_hato: int):
    db.query(models.HatosT).filter(models.HatosT.ID_HATO == id_hato).update(hato.dict(exclude_unset=True))
    db.commit() 
    
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

####
#Como hacer insert de la fecha en el Dictionary y reemplazar valor?

####
#db_le_ha = models.Leche_HatosT(**le_ha.dict(exclude_unset=True))
#    db.add(db_le_ha)
#    db.commit()
    
def get_trashato(db: Session, id_hato:Optional[str]=None, id_lote:Optional[str]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), id_cliente: str = 0):
    filtros=[]
    #filtros.append()
    filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
    filtros.append(models.FincaT.ID_cliente == id_cliente)
    filtros.append(func.DATE(models.Traslado_HatosT.Fecha_Traslado) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.Traslado_HatosT.Fecha_Traslado) <= datetime.strptime(date2,'%Y-%m-%d').date()) 
    if id_hato:
        #filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
        filtros.append(models.Traslado_HatosT.ID_HATO == id_hato)
    if id_lote:
        #filtros.append(models.FincaT.ID_cliente == id_cliente)
        filtros.append(models.LotesT.ID_LOTE == id_lote)
        filtros.append(models.Traslado_HatosT.ID_LOTE == id_lote)
    return db.query(models.Traslado_HatosT).join(models.HatosT).join(models.FincaT).join(models.LotesT).filter(*filtros).all()

### Ubicacion hatos 
def get_ubha(db: Session, id_hato:Optional[str]=None, id_lote:Optional[str]=None, id_cliente: str = 0):
    filtros=[]
    filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    if id_hato:
        filtros.append(models.Ubicacion_VacasT.ID_HATO == id_hato)
    if id_lote:
        filtros.append(models.Ubicacion_VacasT.ID_LOTE == id_lote)
    return db.query(models.Ubicacion_VacasT).join(models.HatosT).join(models.VacasT).filter(*filtros).all() #
###########################################################################################################


#############################################   VACAS    ################################################# 
### Vacas    
def get_vacas(db: Session, id_vaca:Optional[int]=None, nombre:Optional[str]=None, sexo:Optional[int]=None,
              raza: Optional[int]=None, activa:Optional[int]=None,
              id_finca: Union[List[int], None] = Query(default=None), id_tag: Optional[str]=None, id_cliente: str = 0):
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
    if id_finca:
        filtros.append(models.HatosT.ID_FINCA.in_(id_finca))
    if id_tag:
        filtros.append(models.VacasT.ElectronicID == id_tag)
    return db.query(models.VacasT).join(models.Ubicacion_VacasT).join(models.HatosT).filter(*filtros).all()
    
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
    if len(filtros) == 0:
        filtros.append(True)
    return db.query(models.razaT).filter(*filtros).all()

  
### sexo
def get_sexo(db: Session, id_sexo:Optional[int]=None, nombre:Optional[str]=None, codigo:Optional[str]=None):
    filtros=[]
    if id_sexo:
        filtros.append(models.sexoT.idSexo == id_sexo)
    if nombre:
        filtros.append(models.sexoT.Nombre.contains(nombre)) 
    if codigo:
        filtros.append(models.sexoT.Codigo.contains(codigo))
    if len(filtros) == 0:
        filtros.append(True)
    return db.query(models.sexoT).filter(*filtros).all()

    
### Tipo_Destino
def get_t_destino(db: Session, id_destino:Optional[int]=None, nombre:Optional[str]=None):
    filtros=[]
    if id_destino:
        filtros.append(models.tipo_destinoT.IDTipo_Destino == id_destino)
    if nombre:
        filtros.append(models.tipo_destinoT.Nombre.contains(nombre))
    if len(filtros) == 0:
        filtros.append(True)
    return db.query(models.tipo_destinoT).filter(*filtros).all()


### Sires
def get_sires(db: Session, id_sire:Optional[int]=None, id_oficial:Optional[str]=None, nombre_largo:Optional[str]=None, registro:Optional[str]=None, raza:Optional[int]=None, activa:Optional[int]=None ,id_cliente: str = 0): #id_finca:Optional[int]=None
    filtros=[]
    #la tabla no tiene ID_cliente, despues toca ver la forma de filtrar por activas para cada cliente
    #filtros.append(models.siresT.ID_CLIENTE == id_cliente) 
    if id_sire:
        filtros.append(models.siresT.IDsire == id_sire)
    if id_oficial:
        filtros.append(models.siresT.IDOfficial.contains(id_oficial))
    if nombre_largo:
        filtros.append(models.siresT.Nombre_Largo.contains(nombre_largo)) 
    if registro:
        filtros.append(models.siresT.Registro.contains(registro))
    if raza:
        filtros.append(models.siresT.Raza == raza)
    if activa==1:
        filtros.append(models.siresT.Active == activa)
    if len(filtros) == 0:
        filtros.append(True)
    return db.query(models.siresT).filter(*filtros).all()

def get_eventos(db: Session):
    return db.query(models.eventosT).all()

def get_precios_vacas(db: Session, date1: str='2020-01-01', date2: str=datetime.now().strftime("%Y-%m-%d"), vaca:Optional[str]=None,
                  razon: Optional[str]=None , id_cliente: str = 0):
    filtros = []
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    filtros.append(func.DATE(models.Precios_VacasT.Fecha) >= datetime.strptime(date1, '%Y-%m-%d').date())
    filtros.append(func.DATE(models.Precios_VacasT.Fecha) <= datetime.strptime(date2, '%Y-%m-%d').date())
    if vaca:
        filtros.append((models.Precios_VacasT.ID_Vaca == vaca))
    if razon:
        filtros.append((models.Precios_VacasT.ID_razon == razon))
    return db.query(models.Precios_VacasT).join(models.VacasT).filter(*filtros).all()

def write_precios_vaca(db: Session, sch_pre: schemas.Precios_VacasT, id_cliente: str = 0):
    reg_pre = models.Precios_VacasT(**sch_pre.dict())
    db.add(reg_pre)
    db.commit()
    db.refresh(reg_pre) #descommented
    return "post_Registrar_precio_vaca"
#########################################################################################################


###########################################   ACTIVIDADES VACAS   #########################################
### tipo de operaciones    
def get_t_operacion(db: Session, id_tipo:Optional[int]=None, nombre:Optional[str]=None, codigo:Optional[str]=None):
    filtros=[]
    if id_tipo:
        filtros.append(models.tipo_operacionesT.ID_TipoOperaciones == id_tipo)
    if nombre:
        filtros.append(models.tipo_operacionesT.Nombre.contains(nombre)) 
    if codigo:
        filtros.append(models.tipo_operacionesT.Codigo.contains(codigo))
    if len(filtros) == 0:
        filtros.append(True)
    return db.query(models.tipo_operacionesT).filter(*filtros).all()


### Actividades_vacas_categoria
def get_av_categoria(db: Session, id_cat:Optional[int]=None, nombre:Optional[str]=None):
    filtros=[]
    if id_cat:
        filtros.append(models.Actividades_vacas_categoriaT.ID_Categoria == id_cat)
    if nombre:
        filtros.append(models.Actividades_vacas_categoriaT.Nombre.contains(nombre))
    if len(filtros) == 0:
        filtros.append(True)
    return db.query(models.Actividades_vacas_categoriaT).filter(*filtros).all()

    
### Actividades_vacas_resultado
def get_av_resultado(db: Session, id_res:Optional[int]=None, nombre:Optional[str]=None):
    filtros=[]
    if id_res:
        filtros.append(models.Actividades_vacas_resultadoT.ID_Resutlado == id_res)
    if nombre:
        filtros.append(models.Actividades_vacas_resultadoT.Nombre.contains(nombre))
    if len(filtros) == 0:
        filtros.append(True)
    return db.query(models.Actividades_vacas_resultadoT).filter(*filtros).all()


### Eventos vs Categorias
def get_event_categ(db: Session, id_even: Optional[int] = None, id_cate: Optional[int] = None):
    filtros = []
    if id_even:
        filtros.append(models.Eventos_vs_categoriasT.ID_evento == id_even)
    if id_cate:
        filtros.append(models.Eventos_vs_categoriasT.ID_categoria == id_cate)
    if len(filtros) == 0:
        filtros.append(True)
    stmt = select([models.Eventos_vs_categoriasT, models.tipo_operacionesT.Codigo.label('Evento_codigo'),
                   models.tipo_operacionesT.Nombre.label('Evento_nombre'),
                   models.Actividades_vacas_categoriaT.Nombre.label('Categoria_nombre')]). \
        select_from(join(
        join(models.Eventos_vs_categoriasT, models.tipo_operacionesT,
             models.Eventos_vs_categoriasT.ID_evento == models.tipo_operacionesT.ID_TipoOperaciones),
        models.Actividades_vacas_categoriaT,
        models.Eventos_vs_categoriasT.ID_categoria == models.Actividades_vacas_categoriaT.ID_Categoria)). \
        where(and_(*filtros))
    obj = db.execute(stmt).fetchall()
    return obj

### Eventos vs Resultados
def get_event_result(db: Session, id_even: Optional[int] = None, id_resul: Optional[int] = None):
    filtros = []
    if id_even:
        filtros.append(models.Eventos_vs_resultadosT.ID_evento == id_even)
    if id_resul:
        filtros.append(models.Eventos_vs_resultadosT.ID_resultado == id_resul)
    if len(filtros) == 0:
        filtros.append(True)
    stmt = select([models.Eventos_vs_resultadosT, models.tipo_operacionesT.Codigo.label('Evento_codigo'),
                   models.tipo_operacionesT.Nombre.label('Evento_nombre'),
                   models.Actividades_vacas_resultadoT.Nombre.label('Resultado_nombre')]). \
        select_from(join(
        join(models.Eventos_vs_resultadosT, models.tipo_operacionesT,
             models.Eventos_vs_resultadosT.ID_evento == models.tipo_operacionesT.ID_TipoOperaciones),
        models.Actividades_vacas_resultadoT,
        models.Eventos_vs_resultadosT.ID_resultado == models.Actividades_vacas_resultadoT.ID_Resultado)).\
        where(and_(*filtros))
    obj = db.execute(stmt).fetchall()
    return obj

#last ID_Actividad
'''
def get_last_actividad(db: Session):
    return db.query(models.ActividadesVacasT).order_by(models.ActividadesVacasT.ID_Actividad.desc()).first()
'''

## Obtener actividades_vacas Mastitis
def get_act_vacas(db: Session, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), vaca:Optional[str]=None, 
                  operacion:Optional[int]=None, operario:Optional[int]=None,
                  id_finca: Union[List[int], None] = Query(default=None), id_cliente: str = 0) :
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
    if id_finca:
        filtros.append((models.HatosT.ID_FINCA.in_(id_finca)))
    return db.query(models.ActividadesVacasT).join(models.VacasT).join(models.Ubicacion_VacasT).join(models.HatosT).filter(*filtros).all()

def get_view_activacas(db: Session, vaca:Optional[str]=None, cod_oper:Optional[str]=None, operacion:Optional[str]=None,
                       result:Optional[str]=None, categ:Optional[str]=None, operario:Optional[str]=None,
                       rol:Optional[str]=None, date1: str = '2020-01-01',
                       date2: str = datetime.now().strftime("%Y-%m-%d"),
                       id_finca: Union[List[int], None] = Query(default=None), id_cliente: str = 0):
    filtros=[]
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    filtros.append(func.DATE(models.ActividadesVacasView.Fecha) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.ActividadesVacasView.Fecha) <= datetime.strptime(date2,'%Y-%m-%d').date()) 
    if vaca:
        filtros.append(models.ActividadesVacasView.Vaca == vaca)
    if cod_oper:
        filtros.append(models.ActividadesVacasView.Codigo_oper == cod_oper)
    if operacion:
        filtros.append(models.ActividadesVacasView.Operacion == operacion)
    if result:
        filtros.append(models.ActividadesVacasView.Resultado == result)
    if categ:
        filtros.append(models.ActividadesVacasView.Categoria == categ)
    if operario:
        filtros.append(models.ActividadesVacasView.Operario == operario)
    if rol:
        filtros.append(models.ActividadesVacasView.Rol == rol)
    if id_finca:
        filtros.append((models.HatosT.ID_FINCA.in_(id_finca)))

    return db.query(models.ActividadesVacasView).join(models.ActividadesVacasT).join(models.VacasT).join(models.Ubicacion_VacasT).join(models.HatosT).filter(*filtros).all()
    
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
def get_act_mastitis(db: Session, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"),
                     vaca:Optional[str]=None, operacion:Optional[int]=None, operario:Optional[int]=None,
                     id_mastitis:Optional[int]=None, id_finca: Union[List[int], None] = Query(default=None),
                     id_cliente: str = 0):
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
    if id_mastitis:
        filtros.append((models.MastitisT.ID_ACTIVIDAD == id_mastitis))
    if id_finca:
        filtros.append((models.HatosT.ID_FINCA.in_(id_finca)))

    res = db.query(models.MastitisT, models.ActividadesVacasT).join(models.ActividadesVacasT).join(models.VacasT).join(models.Ubicacion_VacasT).join(models.HatosT).filter(*filtros).all()
    #remover ID_TipoOperacion, ID_Resultado, ID_Categoria, ID_Actividad
    avoid = ['ID_TipoOperacion', 'ID_Resultado', 'ID_Categoria', 'ID_Actividad']
    res_b = flatten_join_av(res, avoid) #res_b = flatten_join(res)
    
    return res_b

#DB View
def get_last_mastitis(db: Session, vaca:Optional[str]=None, id_finca: Union[List[int], None] = Query(default=None),
                      id_cliente: str = 0):
    filtros=[]
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)   
    if vaca:
        filtros.append((models.Result_MastitisT.ID_VACA == vaca))
    if id_finca:
        filtros.append((models.HatosT.ID_FINCA.in_(id_finca)))

    #if operario:
    #    filtros.append((models.ActividadesVacasT.ID_OPERARIO == operario))
    res = db.query(models.Result_MastitisT).join(models.VacasT).join(models.Ubicacion_VacasT).join(models.HatosT).filter(*filtros).all()
    #remover ID_TipoOperacion, ID_Resultado, ID_Categoria, ID_Actividad
    #avoid = ['ID_TipoOperacion', 'ID_Resultado', 'ID_Categoria', 'ID_Actividad']
    #res_b = flatten_join_av(res, avoid) #res_b = flatten_join(res)
    
    return res#_b

#patch
def update_mastitis(db: Session, mastitis: schemas.MastitisU, acts:schemas.ActividadesU, id_mastitis: int):
    db.query(models.MastitisT).filter(models.MastitisT.ID_ACTIVIDAD == id_mastitis).update(mastitis.dict(exclude_unset=True))
    db.query(models.ActividadesVacasT).filter(models.ActividadesVacasT.ID_Actividad == id_mastitis).update(acts.dict(exclude_unset=True))
    db.commit()  

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
    reg_parto = models.PartosT(ID_VACA=data.ID_VACA, Numero_Parto=numero, Sire=data.Sire, ID_ACTIVIDAD=id_to_use,
                               Dificultad=data.Dificultad)
    db.add(reg_parto)
    db.commit()
    db.refresh(reg_parto)
    return reg_parto

### Ubicacion vacas  
def get_ubva(db: Session, id_vaca:Optional[str]=None, id_hato:Optional[str]=None, id_lote:Optional[str]=None,
             id_finca: Union[List[int], None] = Query(default=None), id_cliente: str = 0):
    filtros=[]
    filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    if id_hato:
        filtros.append(models.Ubicacion_VacasT.ID_HATO == id_hato)
    if id_vaca:
        filtros.append(models.Ubicacion_VacasT.ID_VACA == id_vaca)
    if id_lote:
        filtros.append(models.Ubicacion_VacasT.ID_LOTE == id_lote)
    if id_finca:
        filtros.append((models.HatosT.ID_FINCA.in_(id_finca)))
    return db.query(models.Ubicacion_VacasT).join(models.HatosT).join(models.VacasT).filter(*filtros).all() #

#DB View - Ubicacion Full
def get_ubvaf(db: Session, id_vaca:Optional[str]=None, id_hato:Optional[str]=None, id_lote:Optional[str]=None,
              id_finca: Union[List[int], None] = Query(default=None), id_cliente: str = 0):
    filtros=[]
    filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    if id_hato:
        filtros.append(models.Ubicacion_Vacas_FullT.ID_HATO == id_hato)
    if id_vaca:
        filtros.append(models.Ubicacion_Vacas_FullT.ID_VACA == id_vaca)
    if id_lote:
        filtros.append(models.Ubicacion_Vacas_FullT.ID_LOTE == id_lote)
    if id_finca:
        filtros.append((models.HatosT.ID_FINCA.in_(id_finca)))
    return db.query(models.Ubicacion_Vacas_FullT).join(models.HatosT).join(models.VacasT).filter(*filtros).all() #

### Traslado vacas    
def write_ubi_vaca(db: Session, sch_ubi: schemas.Ubicacion_VacasT, id_cliente: str = 0):
    reg_uv = models.Ubicacion_VacasT(**sch_ubi.dict())#(ID_VACA=sch_ubi.ID_VACA, ID_HATO=sch_ubi.ID_HATO, ID_LOTE=id_lote)   
    db.add(reg_uv)
    db.commit()
    db.refresh(reg_uv) #descommented
    return reg_uv


def update_ubica_vaca(db: Session, sch_ubi: schemas.Ubicacion_VacasT, id_cliente: str = 0): #vaca:Optional[str]=None
    filtros=[]
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
    filtros.append(models.Ubicacion_VacasT.ID_VACA == sch_ubi.ID_VACA)
    data = db.query(models.Ubicacion_VacasT).join(models.VacasT).join(models.HatosT).filter(*filtros).all()
    print (data)
    if len(data) > 0:
        db.query(models.Ubicacion_VacasT).filter(models.Ubicacion_VacasT.ID_VACA == sch_ubi.ID_VACA).update(sch_ubi.dict(exclude_unset=True))
        db.commit() 
        return "ok"
 
def write_trasvaca(db: Session, sch_ubi: schemas.Ubicacion_VacasT, Fecha_Traslado : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id_cliente: str = 0):
    reg_tv = models.Traslado_VacasT(ID_VACA=sch_ubi.ID_VACA, Fecha_Traslado=Fecha_Traslado, ID_HATO=sch_ubi.ID_HATO)  
    db.add(reg_tv)
    db.commit()
    db.refresh(reg_tv) #descommented
    return  reg_tv #"ok"

def get_trasvaca(db: Session, id_vaca:Optional[str]=None, id_hato:Optional[str]=None, date1: str = '2020-01-01',
                 date2: str = datetime.now().strftime("%Y-%m-%d"),
                 id_finca: Union[List[int], None] = Query(default=None), id_cliente: str = 0):
    filtros=[]
    filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    filtros.append(func.DATE(models.Traslado_VacasT.Fecha_Traslado) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.Traslado_VacasT.Fecha_Traslado) <= datetime.strptime(date2,'%Y-%m-%d').date()) 
    if id_hato:
        #filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
        filtros.append(models.Traslado_VacasT.ID_HATO == id_hato)
    if id_vaca:
        #filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
        filtros.append(models.Traslado_VacasT.ID_VACA == id_vaca)
    if id_finca:
        filtros.append((models.HatosT.ID_FINCA.in_(id_finca)))
    return db.query(models.Traslado_VacasT).join(models.HatosT).join(models.VacasT).filter(*filtros).all()


#Registrar Peso
def registrar_peso(db: Session, data: schemas.peso_Requi, id_to_use):   
    #subida de datos a la API
    reg_peso = models.PesosT(ID_ACTIVIDAD=id_to_use, Peso=data.Peso, ID_VACA=data.ID_VACA)
    db.add(reg_peso)
    db.commit()
    db.refresh(reg_peso)
    return "post_Registrar_Peso"

def get_view_pesos(db: Session, id_vaca:Optional[int]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), id_cliente: str = 0):
    filtros=[]
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    filtros.append(func.DATE(models.Incre_Pesos_View.Fecha) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.Incre_Pesos_View.Fecha) <= datetime.strptime(date2,'%Y-%m-%d').date()) 
    if id_vaca:
        filtros.append(models.Incre_Pesos_View.ID_VACA == id_vaca)
    return db.query(models.Incre_Pesos_View).join(models.VacasT).filter(*filtros).all()


#Registrar Servicio
def registrar_servicio(db: Session, data: schemas.Servicios_Requi, id_to_use):   
    #subida de datos a la API
    reg_servicio = models.ServiciosT(ID_ACTIVIDAD=id_to_use, ID_VACA=data.ID_VACA, Sire=data.Sire, ID_Embrion=data.ID_Embrion)
    db.add(reg_servicio)
    db.commit()
    db.refresh(reg_servicio)
    return "post_Registrar_Servicio" 

#Registrar Diagnostico Prenez
def registrar_diagpre(db: Session, data: schemas.DiagPre_Requi, id_to_use):
    """ change to get from main, and then post with calculated date in main
    act_serv = db.query(models.ServiciosT).filter(models.ServiciosT.IDservicio == data.ID_servicio)
    act_serv
    print(act_serv)
    act_serv = act_serv.ID_ACTIVIDAD
    serv_date = db.query(models.ActividadesVacasT).filter(models.ActividadesVacasT.ID_Actividad == act_serv)
    serv_date = serv_date.Fecha
    days = (data.Fecha - serv_date).days
    """
    #subida de datos a la API
    reg_diagpre = models.DiagPreT(ID_ACTIVIDAD=id_to_use, ID_VACA=data.ID_VACA, ID_servicio=data.ID_servicio, ID_Resultado=data.ID_Resultado, Dias=data.Dias)
    db.add(reg_diagpre)
    db.commit()
    db.refresh(reg_diagpre)
    return "post_Registrar_Diagpre"

def get_dif_parto(db: Session):
    return db.query(models.Dificultad_PartoT).all()


#########################################    LECHE    #####################################################     
# leche hatos
def get_leche_hatos(db: Session, id_hato:Optional[int]=None, id_operario:Optional[int]=None, id_leche_ha:Optional[int]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), id_cliente: str = 0): 
    filtros=[]
    filtros.append(models.HatosT.ID_CLIENTE == id_cliente)
    if id_operario:
        filtros.append(models.Leche_HatosT.ID_OPERARIO == id_operario)
    if id_hato:
        filtros.append(models.Leche_HatosT.ID_HATO== id_hato)
    if id_leche_ha:
        filtros.append(models.Leche_HatosT.ID_Leche_hato== id_leche_ha)
    filtros.append(func.DATE(models.Leche_HatosT.FECHA_ACTIVIDAD) >= datetime.strptime(date1,'%Y-%m-%d').date())#.isoformat(timespec='milliseconds'))
    filtros.append(func.DATE(models.Leche_HatosT.FECHA_ACTIVIDAD) <= datetime.strptime(date2,'%Y-%m-%d').date())#.isoformat(timespec='milliseconds')) 
    return db.query(models.Leche_HatosT).join(models.HatosT).filter(*filtros).all()

def create_leche_hatos(db: Session, le_ha: schemas.Leche_HatosT):
    db_le_ha = models.Leche_HatosT(**le_ha.dict(exclude_unset=True))
    db.add(db_le_ha)
    db.commit()
    #db.refresh(db_le_ha)
    return "post_leche_hatos=Success"

#edit leche hatos, solo para admin
def update_leche_ha(db: Session, leche: schemas.Leche_HatosU, id_leche: int):
    db.query(models.Leche_HatosT).filter(models.Leche_HatosT.ID_Leche_hato == id_leche).update(leche.dict(exclude_unset=True))
    db.commit() 
    
    
# leche vaca
def get_leche_vacas(db: Session, id_vaca:Optional[int]=None, id_operario:Optional[int]=None,
                    id_leche_va:Optional[int]=None, date1: str = '2020-01-01',
                    date2: str = datetime.now().strftime("%Y-%m-%d"),
                    id_finca: Union[List[int], None] = Query(default=None),
                    id_cliente: str = 0):
    filtros=[]
    filtros.append(models.VacasT.ID_CLIENTE == id_cliente)
    if id_operario:
        filtros.append(models.Leche_VacaT.ID_OPERARIO == id_operario)
    if id_vaca:
        filtros.append(models.Leche_VacaT.ID_VACA == id_vaca)
    if id_leche_va:
        filtros.append(models.Leche_VacaT.ID_Leche_vaca== id_leche_va)
    if id_finca:
        filtros.append((models.HatosT.ID_FINCA.in_(id_finca)))
    filtros.append(func.DATE(models.Leche_VacaT.Fecha_c) >= datetime.strptime(date1, '%Y-%m-%d').date())
    filtros.append(func.DATE(models.Leche_VacaT.Fecha_c) <= datetime.strptime(date2, '%Y-%m-%d').date())
    return db.query(models.Leche_VacaT).join(models.VacasT).join(models.Ubicacion_VacasT).join(models.HatosT).filter(*filtros).all()
    
def create_leche_vacas(db: Session, le_va: schemas.Leche_VacaT):
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
def update_leche_va(db: Session, leche: schemas.Leche_VacaU, id_leche: int):
    db.query(models.Leche_VacaT).filter(models.Leche_VacaT.ID_Leche_vaca == id_leche).update(leche.dict(exclude_unset=True))
    db.commit()


## Leche_Entregada
def get_leche_entregada(db: Session, id_leche_entregada:Optional[int]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), id_cliente: str = 0):
    filtros=[]
    filtros.append(models.Leche_EntregadaT.ID_CLIENTE == id_cliente)
    if id_leche_entregada:
        filtros.append(models.Leche_EntregadaT.ID_Leche_Entregada == id_leche_entregada)
    filtros.append(func.DATE(models.Leche_EntregadaT.Fecha) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.Leche_EntregadaT.Fecha) <= datetime.strptime(date2,'%Y-%m-%d').date()) 
    return db.query(models.Leche_EntregadaT).filter(*filtros).all()

def create_leche_entregada(db: Session, le_en: schemas.Leche_EntregadaT):
    db_le_en = models.Leche_EntregadaT(**le_en.dict(exclude_unset=True))
    db.add(db_le_en)
    db.commit()
    return "post_leche_entregada=Success"

#edit solo para admins
def update_leche_entre(db: Session, leche: schemas.Leche_EntregadaT, id_leche_ent: int):
    db.query(models.Leche_EntregadaT).filter(models.Leche_EntregadaT.ID_Leche_Entregada == id_leche_ent).update(leche.dict(exclude_unset=True))
    db.commit()

##########################################################################################################

########################################### TANQUES   ##################################################
## Tanque_Finca
def get_tanque_finca(db: Session, id_tanque:Optional[int]=None, id_finca:Optional[int]=None, capacidad_min:Optional[int]=None, capacidad_max:Optional[int]=None, id_cliente: str = 0):
    filtros=[]
    filtros.append(models.FincaT.ID_cliente == id_cliente)
    if id_tanque:
        filtros.append(models.Tanques_FincaT.ID_TANQUE == id_tanque)
    if id_finca:
        filtros.append(models.Tanques_FincaT.ID_Finca == id_finca)
    if capacidad_min:
        filtros.append(models.Tanques_FincaT.Capacidad_Max >= capacidad_min)
    if capacidad_max:
        filtros.append(models.Tanques_FincaT.Capacidad_Max <= capacidad_max)
    return db.query(models.Tanques_FincaT).join(models.FincaT).filter(*filtros).all()

def create_tanque_finca(db: Session, ta_fi: schemas.Tanques_FincaT):
    db_ta_fi = models.Tanques_FincaT(**ta_fi.dict(exclude_unset=True))
    db.add(db_ta_fi)
    db.commit()
    return "post_tanque-finca=Success"

#edit solo para admins
def update_tanque_finca(db: Session, ta_fi: schemas.Tanques_FincaT, id_tanque: int):
    db.query(models.Tanques_FincaT).filter(models.Tanques_FincaT.ID_TANQUE == id_tanque).update(ta_fi.dict(exclude_unset=True))
    db.commit()

## Tanques Hatos
def get_tanque_hato(db: Session, id_tanque:Optional[int]=None, id_finca:Optional[int]=None, id_hato:Optional[int]=None, id_cliente: str = 0):
    filtros=[]
    filtros.append(models.FincaT.ID_cliente == id_cliente)
    if id_tanque:
        filtros.append(models.Tanques_HatosT.ID_TANQUE == id_tanque)
    if id_finca:
        filtros.append(models.Tanques_FincaT.ID_Finca == id_finca)
    if id_hato:
        filtros.append(models.Tanques_HatosT.ID_HATO == id_hato)
    return db.query(models.Tanques_HatosT).join(models.Tanques_FincaT).join(models.FincaT).filter(*filtros).all()

def create_tanque_hato(db: Session, ta_ha: schemas.Tanques_HatosT):
    db_ta_ha = models.Tanques_HatosT(**ta_ha.dict(exclude_unset=True))
    db.add(db_ta_ha)
    db.commit()
    return "post_tanque-hato=Success"

def update_tanque_hato(db: Session, ta_ha: schemas.Tanques_HatosT, id_tanque: int):
    db.query(models.Tanques_HatosT).filter(models.Tanques_HatosT.ID_TANQUE == id_tanque).update(ta_ha.dict(exclude_unset=True))
    db.commit()
    
#also Delete

##Leche_tanque_diaria
def get_leche_tanque_diaria(db: Session, id_tanque:Optional[int]=None, id_finca:Optional[int]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), id_cliente: str = 0):
    filtros=[]
    filtros.append(models.FincaT.ID_cliente == id_cliente)
    if id_tanque:
        filtros.append(models.Leche_Tanque_DiariaT.ID_TANQUE == id_tanque)
    if id_finca:
        filtros.append(models.Tanques_FincaT.ID_Finca == id_finca)
    filtros.append(func.DATE(models.Leche_Tanque_DiariaT.Fecha) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.Leche_Tanque_DiariaT.Fecha) <= datetime.strptime(date2,'%Y-%m-%d').date()) 
    return db.query(models.Leche_Tanque_DiariaT).join(models.Tanques_FincaT).join(models.FincaT).filter(*filtros).all()

def create_leche_tanque_diaria(db: Session, ta_le: schemas.Leche_Tanque_DiariaT):
    db_ta_le = models.Leche_Tanque_DiariaT(**ta_le.dict(exclude_unset=True))
    db.add(db_ta_le)
    db.commit()
    return "post_tanque-hato=Success"

def update_tanque_leche(db: Session, ta_le: schemas.Leche_Tanque_DiariaT, id_tanque_leche: int):
    db.query(models.Leche_Tanque_DiariaT).filter(models.Leche_Tanque_DiariaT.ID == id_tanque_leche).update(ta_le.dict(exclude_unset=True))
    db.commit()
    
## Test tanques
def get_test_tanque(db: Session, id_tanque:Optional[int]=None, id_finca:Optional[int]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), cod:Optional[str]=None, proveedor:Optional[str]=None, estado:Optional[int]=None, id_cliente: str = 0):
    filtros=[]
    filtros.append(models.FincaT.ID_cliente == id_cliente)
    if id_tanque:
        filtros.append(models.Test_TanquesT.ID_TANQUE == id_tanque)
    if id_finca:
        filtros.append(models.Tanques_FincaT.ID_Finca == id_finca)
    if cod:
        filtros.append(models.Test_TanquesT.Cod_seguimiento.contains(cod))
    if proveedor:
        filtros.append(models.Test_TanquesT.Proveedor.contains(proveedor))
    if estado:
        filtros.append(models.Test_TanquesT.Estado == estado)
    filtros.append(func.DATE(models.Test_TanquesT.Fecha_Test) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.Test_TanquesT.Fecha_Test) <= datetime.strptime(date2,'%Y-%m-%d').date()) 
    return db.query(models.Test_TanquesT).join(models.Tanques_FincaT).join(models.FincaT).filter(*filtros).all()

def create_test_tanque(db: Session, ta_te: schemas.Test_TanquesT):
    db_ta_te = models.Test_TanquesT(**ta_te.dict(exclude_unset=True))
    db.add(db_ta_te)
    db.commit()
    return "post_tanque-test=Success"

def update_tanque_test(db: Session, ta_te: schemas.Test_TanquesT, id_tanque_test: int):
    db.query(models.Test_TanquesT).filter(models.Test_TanquesT.ID == id_tanque_test).update(ta_te.dict(exclude_unset=True))
    db.commit()


## Resultado tanques
def get_result_tanque(db: Session, id_tanque:Optional[int]=None, id_finca:Optional[int]=None, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), cod:Optional[str]=None,  id_cliente: str = 0):
    filtros=[]
    filtros.append(models.FincaT.ID_cliente == id_cliente)
    if id_tanque:
        filtros.append(models.Resultados_TanquesT.ID_TANQUE == id_tanque)
    if id_finca:
        filtros.append(models.Tanques_FincaT.ID_Finca == id_finca)
    if cod:
        filtros.append(models.Resultados_TanquesT.Cod_seguimiento.contains(cod))
    filtros.append(func.DATE(models.Resultados_TanquesT.Fecha_recepcion) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.Resultados_TanquesT.Fecha_recepcion) <= datetime.strptime(date2,'%Y-%m-%d').date()) 
    return db.query(models.Resultados_TanquesT).join(models.Tanques_FincaT).join(models.FincaT).filter(*filtros).all()

def create_result_tanque(db: Session, ta_re: schemas.Resultados_TanquesT):
    db_ta_re = models.Resultados_TanquesT(**ta_re.dict(exclude_unset=True))
    db.add(db_ta_re)
    db.commit()
    return "post_tanque-Resultado=Success"

def update_tanque_result(db: Session, ta_re: schemas.Resultados_TanquesT, id_tanque_result: int):
    db.query(models.Resultados_TanquesT).filter(models.Resultados_TanquesT.ID == id_tanque_result).update(ta_re.dict(exclude_unset=True))
    db.commit()
    
#########################################################################################################

######################################### OTRAS FUENTES LOTES   #########################################
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

###########################################################################################################

##########################################  Monitoreo procesamiento imagenes satel   ######################
def create_moni_des(db: Session, mo_des: schemas.monitoreo_descargas_sentinelT):
    db_mo_des = models.monitoreo_descargas_sentinelT(**mo_des.dict(exclude_unset=True))
    db.add(db_mo_des)
    db.commit()
    #db.refresh(db_le_va)
    return "post_monitoreo_descargas=Success"

def get_moni_des(db: Session, date1: str='2020-01-01', date2: str=datetime.now().strftime("%Y-%m-%d"),  zona: Optional[str] = None, finca:Optional[str]=None, id_cliente: Optional[str]=None) : 
    filtros=[]
    filtros.append(func.DATE(models.monitoreo_descargas_sentinelT.fecha) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.monitoreo_descargas_sentinelT.fecha) <= datetime.strptime(date2,'%Y-%m-%d').date()) 
    if zona:
        filtros.append((models.monitoreo_descargas_sentinelT.zona == finca))
    if id_cliente:
        filtros.append(models.FincaT.ID_cliente == id_cliente)
    if finca:
        filtros.append((models.FincaT.ID_FINCA == finca))
    #return db.query(models.monitoreo_descargas_sentinelT).join(models.FincaT).filter(*filtros).all()
    if finca or id_cliente:
        return db.query(models.monitoreo_descargas_sentinelT).join(models.FincaT).filter(*filtros).all()
    else:
        return db.query(models.monitoreo_descargas_sentinelT).filter(*filtros).all()
###########################################################################################################

########################################   ESTACION METEOROLOGICA   #######################################
### meteorologia
def registrar_meteo(db: Session, meteo: schemas.MeteorologiaT):
    reg_meteo = models.MeteorologiaT(**meteo.dict())
    db.add(reg_meteo)
    db.commit()
    db.refresh(reg_meteo)
    return reg_meteo

def get_meteo(db: Session, date1: str = '2020-01-01', date2: str = datetime.now().strftime("%Y-%m-%d"), estacion:Optional[str]=None, finca:Optional[str]=None, id_cliente: str = 0) : 
    filtros=[]
    filtros.append(models.FincaT.ID_cliente == id_cliente)
    filtros.append(func.DATE(models.MeteorologiaT.FECHA_HORA) >= datetime.strptime(date1,'%Y-%m-%d').date())
    filtros.append(func.DATE(models.MeteorologiaT.FECHA_HORA) <= datetime.strptime(date2,'%Y-%m-%d').date())    
    if estacion:
        filtros.append((models.MeteorologiaT.ID_Estacion == estacion))
    if finca:
        filtros.append((models.EstacionesT.ID_Finca == finca))
    return db.query(models.MeteorologiaT).join(models.EstacionesT).join(models.FincaT).filter(*filtros).all()

def registrar_meteo_iot(db: Session, met_iot: List[schemas.Meteo_iot]):
    db_iot = []
    for dictio in met_iot:
        db_iot.append(models.Meteo_iot(**dictio.dict(exclude_unset=True)))
    db.bulk_save_objects(db_iot)
    db.commit()
    return "post_Meteo_IoT=Success"

###########################################################################################################

#################################################### CELOTRON  ############################################
def write_celo(db: Session): # sch_celo: schemas.celoT, id_cliente: str = 0):
    #reg_celo = models.celoT(**sch_celo.dict())
    reg_celo = models.celoT(ID_vaca=1234, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S") , celotron=987654321)
    db.add(reg_celo)
    db.commit()
    db.refresh(reg_celo)
    return reg_celo.id_celo


def registrar_celo(db: Session, celo: schemas.celo_gsmT):
    reg_celo_gsm = models.celo_gsmT(**celo.dict())
    db.add(reg_celo_gsm)
    db.commit()
    #db.refresh(reg_celo_gsm)
    return "post_celo_gsm= OK"


def get_celo_gsm(db: Session) :
    return db.query(models.celo_gsmT).all()


def sms_celo(db: Session):
    # API GET Twilio -> Twilio ultimo mensaje
    client = Client(SID, TOKEN)
    messages = client.messages.list(limit=1)

    # Twilio entrega Body, numero, fecha, etc  API Parsea
    for record in messages:
        body = record.body
        fecha_recibido = record.date_sent
        fecha_envio = record.date_created
        numero_envio = record.from_
        numero_recibido = record.to
        direccion = record.direction
        costo = record.price
        segmentos = record.num_segments
        status = record.status

        if direccion == 'inbound':
            # Body -> verifica columnas(formato OK)
            try:
                res = dict(map(str.strip, sub.split(':', 1)) for sub in
                           body.replace('\n', '').replace(' ', '').replace('%', '').split(';')
                           if ':' in sub)
            except:
                res = {}
                print('format not valid')
            meta = {'fecha_envio': fecha_envio, 'fecha_recibido': fecha_recibido, 'numero_envio': numero_envio,
                    'numero_recibido': numero_recibido, 'direccion': direccion, 'segmentos': segmentos,
                    'status': status, 'costo': costo}
            parsed = {**res, **meta}
            celotron_data = pd.DataFrame.from_dict([parsed])
            celotron_data.rename(columns={'V': 'tag', 'Hora': 'hora', 'Fecha': 'fecha', 'Ser': 'sensor',
                                          'Bat': 'battery'}, inplace=True, errors='ignore')

            if 'fecha' not in celotron_data.columns:
                continue

            celotron_data['fecha_celo'] = celotron_data['fecha'].astype(str) + ' ' + celotron_data['hora'].astype(str)
            celotron_data['fecha_celo'] = pd.to_datetime(celotron_data['fecha_celo'], format='%d/%m/%Y %H:%M')
            celotron_data['fecha_celo'] = celotron_data['fecha_celo'].astype(str)
            celotron_data['fecha_envio'] = celotron_data['fecha_envio'].dt.tz_localize(None)
            celotron_data['fecha_envio'] = celotron_data['fecha_envio'].astype(str)
            celotron_data['fecha_recibido'] = celotron_data['fecha_recibido'].dt.tz_localize(None)
            celotron_data['fecha_recibido'] = celotron_data['fecha_recibido'].astype(str)
            celotron_data.drop(columns=['hora', 'fecha'], inplace=True, errors='ignore')
            celotron_dict = celotron_data.to_dict('records')

            # Guardar en la DB
            reg_celo = models.celoT(**celotron_dict[0])
            db.add(reg_celo)
            db.commit()
            db.refresh(reg_celo)

            # merge TAG con VACA
            vaca_filtros = []
            vaca_filtros.append(models.VacasT.ElectronicID == celotron_data['tag'][0])
            vaca = db.query(models.VacasT).filter(*vaca_filtros).all()
            if vaca != []:
                vaca_df = pd.DataFrame.from_records([s.__dict__ for s in vaca])
                # print(vaca_df)
                print(f'id_vaca: {vaca_df.ID_VACA[0]}, cliente: {vaca_df.ID_CLIENTE[0]}, '
                      f'nombre_vaca: {vaca_df.Nombre_Vaca[0]}')
                cliente_identificado = vaca_df.ID_CLIENTE[0]
                nombre_vaca = vaca_df.Nombre_Vaca[0]
                id_vaca = vaca_df.ID_VACA[0]
            else:
                print(f"vaca not found, with tag: {celotron_data['tag'][0]}")
                nombre_vaca = 'UNKNOWN'
                id_vaca = None

            # merge Celotron con Toro
            toro_filtros = []
            toro_filtros.append(models.VacasT.ElectronicID == celotron_data['sensor'][0])
            toro_filtros.append(models.VacasT.Sexo.in_([3, 4]))
            toro = db.query(models.VacasT).filter(*toro_filtros).all()
            if toro != []:
                toro_df = pd.DataFrame.from_records([s.__dict__ for s in toro])
                print(f'id_toro: {toro_df.ID_VACA[0]}, cliente: {toro_df.ID_CLIENTE[0]}, '
                      f'nombre_toro: {toro_df.Nombre_Vaca[0]}')
                cliente_identificado = toro_df.ID_CLIENTE[0]
                nombre_toro = toro_df.Nombre_Vaca[0]
                id_toro = toro_df.ID_VACA[0]
            else:
                print(f"Toro not found, with Sensor: {celotron_data['sensor'][0]}")
                nombre_toro = 'UNKNOWN'
                id_toro = None

            # merge vaca / toro con Ubicacion Vacas
            ubicacion_filtros = []
            if id_vaca:
                ubicacion_filtros.append(models.Ubicacion_Vacas_FullT.ID_VACA == id_vaca)
            elif id_toro:
                ubicacion_filtros.append(models.Ubicacion_Vacas_FullT.ID_VACA == id_toro)

            if ubicacion_filtros != []:
                ubicacion = db.query(models.Ubicacion_Vacas_FullT).filter(*ubicacion_filtros).all()
            else:
                ubicacion = []

            if ubicacion != []:
                ubicacion_df = pd.DataFrame.from_records([s.__dict__ for s in ubicacion])
                print(f'id_lote: {ubicacion_df.ID_LOTE[0]}, LOTE: {ubicacion_df.NOMBRE_LOTE[0]}, '
                      f'id_hato: {ubicacion_df.ID_HATO[0]}, HATO: {ubicacion_df.Nombre_Hato[0]}')
                lote = ubicacion_df.NOMBRE_LOTE[0]
                hato = ubicacion_df.Nombre_Hato[0]
            else:
                print("Ubicacion not found")
                lote = 'UNKNOWN'
                hato = 'UNKNOWN'


            # Capturar numero de contacto de clientes
            cliente_filtros = []
            cliente_filtros.append(models.pref_sms_contactT.status == 'Activo')
            if vaca != []:
                cliente_filtros.append(models.pref_sms_contactT.id_cliente == int(cliente_identificado))
            cliente = db.query(models.pref_sms_contactT).filter(*cliente_filtros).all()
            if cliente != []:
                cliente_df = pd.DataFrame.from_records([s.__dict__ for s in cliente])
                numeros_destino = cliente_df['numero'].values.tolist()
                print(numeros_destino)


            # reenviar mensajes con vaca, toro y fecha/hora
            texto = f"Vaca: {nombre_vaca}, Tag: {str(celotron_dict[0]['tag'])}, " \
                    f"Fecha: {celotron_dict[0]['fecha_celo']}, " \
                    f"Toro: {nombre_toro}, Celotron: {celotron_dict[0]['sensor']}, Ubicacion: {lote}, Hato: {hato}"

            for number in numeros_destino:
                try:
                    message = client.messages.create(
                        to=number,
                        from_=NUMBER,
                        body=texto)
                    print(f'exito: {message.sid}')
                except TwilioRestException as e:
                    print(e)
    
            return reg_celo.id_celo
