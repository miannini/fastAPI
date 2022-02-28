# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:10:03 2020

@author: Marcelo
"""

from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel #, Field


#######################     USERS   ###################################################
# TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user: str

# USER sec schemas    
class UserInfoBase(BaseModel):
    user: str
  
class UserCreate(UserInfoBase):
    full_name: str
    password: str
    email: str
    ID_CLIENTE : Optional[int] = None
    #active_status : Optional[int] = None
   
class UserAuthenticate(UserInfoBase):
    password: str

class UserInfo(UserInfoBase):
    id: int
    class Config:
        orm_mode = True

class UserInfoFull(UserInfoBase):
    id: int
    active_status : Optional[int] = None
    id_user_rol : Optional[int] = None
    ID_CLIENTE : Optional[int] = None
    ID_OPERARIO : Optional[int] = None
    class Config:
        orm_mode = True

#USER sec alternative
class User(BaseModel):
    user: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    active_status: Optional[int] = None
    id_user_rol : Optional[int] = None
    ID_CLIENTE : Optional[int] = None
    ID_OPERARIO : Optional[int] = None
    Deshabilitado : Optional[int] = None
    Fecha_deshabilitado : Optional[datetime] = None
    
class UserInDB(User):
    password: str

class UserInfo2(User):
    id: int
    class Config:
        orm_mode = True
  
#privileges
class API_Users_PrivT(BaseModel):
    id_user_rol : int
    name : Optional[str] = None
    description : Optional[str] = None
    Deshabilitado : Optional[int] = None
    Fecha_deshabilitado : Optional[datetime] = None
    class Config:
        orm_mode = True
        
#permisos
class PermisosT(BaseModel):
    ID_permisos : int
    User_ID : int
    Crear : Optional[int] = None
    Activar_User : Optional[int] = None
    Imagenes_Sat : Optional[int] = None
    Leche : Optional[int] = None
    Hatos_Traslado : Optional[int] = None
    Hatos_Suplementa : Optional[int] = None
    Hatos_Servicios : Optional[int] = None
    Animales_Traslados : Optional[int] = None
    Animales_Mastitis : Optional[int] = None
    Animales_CrearEditar : Optional[int] = None
    Animales_Examenes : Optional[int] = None
    Animales_Salud : Optional[int] = None
    Lotes : Optional[int] = None
    class Config:
        orm_mode = True

class PermisosU(BaseModel):
    #ID_permisos : int
    User_ID : int
    Crear : Optional[int] = None
    Activar_User : Optional[int] = None
    Imagenes_Sat : Optional[int] = None
    Leche : Optional[int] = None
    Hatos_Traslado : Optional[int] = None
    Hatos_Suplementa : Optional[int] = None
    Hatos_Servicios : Optional[int] = None
    Animales_Traslados : Optional[int] = None
    Animales_Mastitis : Optional[int] = None
    Animales_CrearEditar : Optional[int] = None
    Animales_Examenes : Optional[int] = None
    Animales_Salud : Optional[int] = None
    Lotes : Optional[int] = None
    class Config:
        orm_mode = True
    
###################################################################################################


############################       CLIENTS      ###############################################
class ClientesU(BaseModel):
    NOMBRE: Optional[str] = None
    NIT_CC: Optional[int] = None
    RAZON_SOCIAL: Optional[str] = None
    TELEFONO: Optional[int] = None
    EMAIL: Optional[str] = None
    DIRECCION: Optional[str] = None
    DESCRIPCION: Optional[str] = None
    CIUDAD: Optional[str] = None
    DEPARTAMENTO: Optional[str] = None
    FECHA_CONTRATO: Optional[date] = None
    FECHA_VENCIMIENTOCO : Optional[date] = None
    ESTADO : Optional[str] = None
    deshabilitado : Optional[int] = None
    Fecha_deshabilitado : Optional[datetime] = None
    Fecha_Hoy : Optional[datetime] = None
    Dias_vencimiento : Optional[datetime] = None
    class Config:
        orm_mode = True

class ClientesT(ClientesU):
    ID_CLIENTE: int
    class Config:
        orm_mode = True
'''
class Clientes_id(BaseModel):
    ID_CLIENTE: int
    
class ClientesCreate(BaseModel): #(Clientes_id):
    NOMBRE: Optional[str] = None
    NIT_CC: Optional[int] = None
    RAZON_SOCIAL: Optional[str] = None
    TELEFONO: Optional[int] = None
    EMAIL: Optional[str] = None
    DIRECCION: Optional[str] = None
    DESCRIPCION: Optional[str] = None
    CIUDAD: Optional[str] = None
    DEPARTAMENTO: Optional[str] = None
    FECHA_CONTRATO: Optional[date] = None
    class Config:
        orm_mode = True
'''       
####################################################################################################


##################################      OPERARIOS    #################################################
class OperarioC(BaseModel): 
    ID_CLIENTE: int
    #ID_FINCA: int
    NombreOperario: str
    FechaDeIngreso: Optional[date] = None
    Telefono: Optional[int] = None
    Rol: Optional[str] = None
    Descripcion: Optional[str] = None
    Email: Optional[str] = None
    Direccion: Optional[str] = None
    Fecha_Creacion : Optional[datetime] = None
    deshabilitado : Optional[int] = None
    Fecha_deshabilitado : Optional[datetime] = None
    class Config:
        orm_mode = True

class OperarioT(OperarioC): 
    ID_OPERARIO: int
    class Config:
        orm_mode = True  
'''    
class OperarioN(BaseModel): 
    ID_CLIENTE: Optional[int] = None
    #ID_FINCA: Optional[int] = None
    NombreOperario: Optional[str] = None
    FechaDeIngreso: Optional[date] = None
    Telefono: Optional[int] = None
    Rol: Optional[str] = None
    Descripcion: Optional[str] = None
    Email: Optional[str] = None
    Direccion: Optional[str] = None
    class Config:
        orm_mode = True

class OperarioInfo2(OperarioN):
    ID_OPERARIO: int
    class Config:
        orm_mode = True 
'''        
class Operario_Sin_UserT(BaseModel):
    ID_OPERARIO : int
    NombreOperario : str
    ID_CLIENTE : int
    class Config:
        orm_mode = True


class Operarios_FincasT(BaseModel):
    ID_OPERARIO : int
    ID_FINCA: int
    deshabilitado : Optional[int] = None
    Fecha_deshabilitado : Optional[datetime] = None
    class Config:
        orm_mode = True

class Operarios_FincasF(Operarios_FincasT):
    ID : int
    class Config:
        orm_mode = True
        
##########################################################################################################


###########################################    LOTES    ###################################################
'''
class LotesT2(BaseModel): 
    NOMBRE_LOTE: Optional[str] = None
    class Config:
        orm_mode = True
'''
class LotesN(BaseModel): 
    ID_FINCA: Optional[int] = None
    NOMBRE_LOTE: Optional[str] = None
    LATITUD: Optional[float] = None
    LONGITUD: Optional[float] = None
    AREA: Optional[float] = None
    DESCRIPCION: Optional[str] = None
    ID_variedad: Optional[int] = None
    Fecha_Creacion : Optional[datetime] = None
    deshabilitado : Optional[int] = None
    Fecha_deshabilitado : Optional[datetime] = None
    class Config:
        orm_mode = True

class LotesT(LotesN): 
    ID_LOTE: int
    class Config:
        orm_mode = True
'''        
class LotesPasto(BaseModel): 
    ID_LOTE: int
    ID_variedad: Optional[int] = None
    class Config:
        orm_mode = True
      
class LoteInfo2(LotesN):
    ID_LOTE: int
    class Config:
        orm_mode = True
'''  

class tipo_cultivoT(BaseModel):
    nombre : Optional[str] = None
    clase : Optional[str] = None
    deshabilitado : Optional[int] = None
    Fecha_deshabilitado : Optional[datetime] = None
    class Config:
        orm_mode = True
        
class tipo_cultivoFull(tipo_cultivoT):      
    ID_cultivo : int
    class Config:
        orm_mode = True
    
class variedad_cultivoT(BaseModel):
    ID_cultivo : int
    nombre : Optional[str] = None
    deshabilitado : Optional[int] = None
    Fecha_deshabilitado : Optional[datetime] = None
    class Config:
        orm_mode = True

class variedad_cultivoFull(variedad_cultivoT):
    ID_variedad  : int
    class Config:
        orm_mode = True
###########################################################################################################


#########################################  ACTIVIDADES LOTES  ############################################        
class Actividades_LotesT(BaseModel):
    ID_ACT_LOTE : int
    ID_LOTE : int
    FECHA_ACTIVIDAD  : datetime
    ID_Tipo_Actividad : int
    Producto : Optional[str] = None
    ID_OPERARIO : int
    Comentario : Optional[str] = None
    Fecha_programada : Optional[datetime] = None
    Estado : Optional[int] = None
    class Config:
        orm_mode = True

class Actividades_LotesT2(BaseModel): #Afoto
    ID_LOTE : int
    FECHA_ACTIVIDAD  : datetime
    ID_Tipo_Actividad : int
    ID_OPERARIO : int
    class Config:
        orm_mode = True
        
class Acti_lotes_post(Actividades_LotesT2):
    Producto : Optional[str] = None
    Comentario : Optional[str] = None
    Fecha_programada : Optional[datetime] = None
    Estado : Optional[int] = None
    class Config:
        orm_mode = True
        
class AforoT(BaseModel):
    ID_ACTIVIDAD : int
    Aforo : float
    class Config:
        orm_mode = True
        
class Aforo_Requi(BaseModel):
    ID_LOTE : int
    FECHA_ACTIVIDAD  : datetime #datetime
    ID_Tipo_Actividad : int = 15
    #Producto : Optional[str] = None
    ID_OPERARIO : int
    #Comentario : Optional[str] = None
    #Fecha_programada : Optional[datetime] = None
    #Estado : Optional[int] = None
    Aforo: float
    class Config:
        orm_mode = True

class Tipo_Actividades_LotesT(BaseModel):
    IDTipo_Actividades_Lotes : int
    Code : str
    Nombre  : str
    ID_Categoria_Act : int
    deshabilitado : Optional[int] = None
    Fecha_deshabilitado : Optional[datetime] = None
    class Config:
        orm_mode = True

class Categoria_Actividades_LotesT(BaseModel):
    Code : str
    Nombre : str
    Deshabilitado : Optional[int] = None
    Fecha_deshabilitado : Optional[datetime] = None
    class Config:
        orm_mode = True  
        
class Categoria_Actividades_LotesF(Categoria_Actividades_LotesT):
    ID_Categoria_Act_Lote : int

class Ultimas_Act_LotesT(BaseModel): #VIEW
    ID_ACT_LOTE : int
    ID_LOTE : int
    FECHA_ACTIVIDAD : datetime
    ID_Tipo_Actividad : int
    Dias : Optional[int] = None 
    class Config:
        orm_mode = True  
        
        
###########################################################################################################


#################################     FINCAS  (down here to make word lotes_list)   ######################################
class FincaU(BaseModel):
    NOMBRE: Optional[str] = None
    DESCRIPCION: Optional[str] = None
    sentinel_zone: Optional[str] = None
    Fecha_Creacion : Optional[datetime] = None
    deshabilitado : Optional[int] = None
    Fecha_deshabilitado : Optional[datetime] = None
    ID_Zone_sentinel: Optional[int] = None
    class Config:
        orm_mode = True

class FincaT(FincaU):
    ID_FINCA: int
    ID_cliente: int
    lotes_list: List[LotesT] = []
    class Config:
        orm_mode = True
  
class FincaP(BaseModel):
    ID_cliente: int
    NOMBRE: Optional[str] = None
    DESCRIPCION: Optional[str] = None
    class Config:
        orm_mode = True

class FincaR(BaseModel): #Finca_Small
    ID_FINCA: int
    ID_cliente: int
    NOMBRE: Optional[str] = None
    class Config:
        orm_mode = True

###########################################################################################################

########################################    HATOS     ####################################################       
class HatosP(BaseModel):
    ID_CLIENTE : Optional[int] = None
    ID_FINCA : Optional[int] = None
    Nombre_Hato : Optional[str] = None
    TIPO_Hato : Optional[str] = None
    Descripcion : Optional[str] = None
    Fecha_Creacion : Optional[datetime] = None
    deshabilitado : Optional[int] = None
    Fecha_deshabilitado : Optional[datetime] = None
    class Config:
        orm_mode = True
        
class HatosT(HatosP):
    ID_HATO : int
    #ID_CLIENTE : int
    #ID_FINCA : int
    #Nombre_Hato : Optional[str] = None
    #TIPO_Hato : Optional[str] = None
    #Descripcion : Optional[str] = None
    class Config:
        orm_mode = True
        
class HatosR(BaseModel): #Hatos_Small
    ID_HATO : int
    ID_CLIENTE : int
    ID_FINCA : int
    Nombre_Hato : Optional[str] = None
    class Config:
        orm_mode = True
'''        
class HatosT2(BaseModel):
    Nombre_Hato : Optional[str] = None
    class Config:
        orm_mode = True
'''        
   
class Traslado_HatosT(BaseModel):
    Fecha_Traslado : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ID_HATO : int
    ID_LOTE : int
    #ID_OPERARIO : Optional[int] = None
    class Config:
        orm_mode = True

class Traslado_HatosF(Traslado_HatosT):
    ID_TRASLADO_HATO : int
###########################################################################################################


#############################################   VACAS    ################################################# 
'''        
class VacasT2(BaseModel):
    #ID_VACA : int
    Nombre_Vaca : str
    class Config:
        orm_mode = True 
'''

class VacasR(BaseModel): #Vacas_small
    ID_VACA : int
    ID_CLIENTE : int
    Nombre_Vaca : str
    Raza : Optional[int] = None
    Sexo : Optional[int] = None
    class Config:
        orm_mode = True  

#vacas edit and create
class VacaN(BaseModel):
    ID_CLIENTE : Optional[int] = None
    ElectronicID : Optional[str] = None
    Nombre_Vaca : Optional[str] = None
    Raza : Optional[int] = None
    Sexo : Optional[int] = None
    VacaMadre : Optional[int] = None
    IDparto : Optional[int] = None
    FechaRegistro : Optional[date] = None
    IDTipoOrigen : Optional[int] = None
    FechaNacimiento : Optional[date] = None
    IDTipoSalida : Optional[int] = None
    FechaSalida : Optional[date] = None 
    Sire : Optional[int] = None
    class Config:
        orm_mode = True
        
class VacasT(BaseModel):
    ID_VACA : int
    #ID_CLIENTE : int
    #ElectronicID : Optional[str] = None
    #Nombre_Vaca : str
    #Raza : Optional[int] = None
    #Sexo : Optional[int] = None
    #VacaMadre : Optional[int] = None
    #IDparto : Optional[int] = None
    #FechaRegistro : Optional[date] = None
    #IDTipoOrigen : Optional[int] = None
    #FechaNacimiento : Optional[date] = None
    #IDTipoSalida : Optional[int] = None
    #FechaSalida : Optional[date] = None 
    #Sire : Optional[int] = None
    class Config:
        orm_mode = True   
'''    
class VacaInfo2(VacaN):
    ID_VACA: int
    class Config:
        orm_mode = True
'''
  
class razaR(BaseModel): #Raza-small
    ID_RAZA : int
    Codigo : Optional [str] = None
    Nombre : Optional [str] = None
    class Config:
        orm_mode = True
        
class razaT(razaR):
    #ID_RAZA : int
    #Codigo : Optional [str] = None
    #Nombre : Optional [str] = None
    Gestacion : Optional [int] = None 
    MaxGestacion : Optional [int] = None
    MinGestacion  : Optional [int] = None
    Leche : Optional [str] = None
    Carne : Optional [str] = None
    Pureza : Optional [float] = None
    Fecha_Creacion : Optional [datetime] = None
    Deshabilitado : Optional [int] = None
    Fecha_deshabilitado : Optional [datetime] = None
    class Config:
        orm_mode = True
    
class sexoT(BaseModel):
    idSexo : int
    Codigo : Optional [str] = None
    Nombre : Optional [str] = None
    Genero : Optional [int] = None 
    VacaRep : Optional [int] = None
    ToroRep  : Optional [int] = None
    Fecha_Creacion : Optional [datetime] = None
    deshabilitado : Optional [int] = None
    Fecha_deshabilitado : Optional [datetime] = None
    class Config:
        orm_mode = True  
    
class tipo_destinoT(BaseModel):   
    IDTipo_Destino : int
    Nombre : Optional [str] = None
    Descripcion : Optional [str] = None
    Fecha_Creacion : Optional [datetime] = None
    deshabilitado : Optional [int] = None
    Fecha_deshabilitado : Optional [datetime] = None
    class Config:
        orm_mode = True

class siresT(BaseModel):
    IDsire : int
    Active : Optional [int] = None
    IDOfficial : Optional [str] = None
    AINumber : Optional [str] = None
    Nombre_Largo : Optional [str] = None
    Registro : Optional [str] = None
    Raza : Optional [int] = None
    #Fecha_descontinuado : Optional[datetime] = None
    Fecha_Creacion : Optional [datetime] = None
    deshabilitado : Optional [int] = None
    Fecha_deshabilitado : Optional [datetime] = None
    class Config:
        orm_mode = True
    
class tipo_origenT(BaseModel):
    IDTipo_origen: Optional [int] = None
    Nombre : Optional [str] = None
    Descripcion : Optional [str] = None
    deshabilitado : Optional [int] = None
    Fecha_deshabilitado : Optional [datetime] = None
    class Config:
        orm_mode = True
#########################################################################################################


###########################################   ACTIVIDADES VACAS   #########################################
class ActInfoBase(BaseModel):
    ID_Actividad : int

class ActInfo(ActInfoBase):
    ID_VACA : int
    ID_TipoOperacion : int = 9
    ID_Resultado : int = 34
    ID_OPERARIO : int = 35
    ID_Categoria : int = 1
    Fecha  : Optional[datetime] = None
    Comentario : Optional[str] = None
    class Config:
        orm_mode = True 
        
class Actividades(BaseModel):
    ID_VACA : int
    ID_TipoOperacion : int
    ID_Resultado : int
    ID_OPERARIO : int
    ID_Categoria : int
    Fecha  : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    Comentario : Optional[str] = None
    class Config:
        orm_mode = True 
        
class ActividadesU(BaseModel):
    ID_VACA : Optional [int] = None
    ID_OPERARIO : Optional [int] = None
    Fecha  : Optional[datetime] = None 
    Comentario : Optional[str] = None
    class Config:
        orm_mode = True 
        
class ActividadesVacasView(BaseModel):
    ID_Actividad : int
    Vaca : str
    Codigo_oper : Optional[str] = None
    Operacion : Optional[str] = None
    Resultado : Optional[str] = None
    Categoria : Optional[str] = None
    Operario : Optional[str] = None
    Rol : Optional[str] = None
    Fecha : Optional[datetime] = None
    Comentario : Optional[str] = None
    class Config:
        orm_mode = True 

class tipo_operacionesT(BaseModel):
    ID_TipoOperaciones : int
    Codigo : Optional [str] = None
    Nombre : Optional [str] = None
    deshabilitado : Optional [int] = None
    Fecha_deshabilitado : Optional [datetime] = None
    class Config:
        orm_mode = True
        
class Actividades_vacas_categoriaT(BaseModel):   
    ID_Categoria : int
    Nombre : Optional [str] = None
    Descripcion : Optional [str] = None
    deshabilitado : Optional [int] = None
    Fecha_deshabilitado : Optional [datetime] = None
    class Config:
        orm_mode = True
        
class Actividades_vacas_resultadoT(BaseModel):   
    ID_Resultado : int
    Nombre : Optional [str] = None
    Descripcion : Optional [str] = None
    deshabilitado : Optional [int] = None
    Fecha_deshabilitado : Optional [datetime] = None
    class Config:
        orm_mode = True

class MastitisT(BaseModel):
    ID_ACTIVIDAD : int
    AI : Optional [int] = None
    AD : Optional [int] = None
    PI : Optional [int] = None
    PD : Optional [int] = None
    Chequeo_revision : Optional[str] = None
    Ubre_sana : Optional [float] = None
    Calificacion : Optional [float] = None
    GAP : Optional [float] = None
    class Config:
        orm_mode = True 

class MastitisU(BaseModel):
    #ID_ACTIVIDAD : Optional [int] = None
    AI : Optional [int] = None
    AD : Optional [int] = None
    PI : Optional [int] = None
    PD : Optional [int] = None
    Chequeo_revision : Optional[str] = None
    Ubre_sana : Optional [float] = None
    Calificacion : Optional [float] = None
    GAP : Optional [float] = None
    class Config:
        orm_mode = True 

class Mast_Requi(BaseModel):
    ID_VACA : int
    ID_TipoOperacion : int = 9
    ID_Resultado : int = 34
    ID_OPERARIO : int = 35
    ID_Categoria : int = 1
    Fecha  : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #None
    Comentario : Optional[str] = None
    AI : Optional [int] = None
    AD : Optional [int] = None
    PI : Optional [int] = None
    PD : Optional [int] = None
    Chequeo_revision : Optional[str] = None
    class Config:
        orm_mode = True 

#new test mastitis        
class Mast_2(BaseModel):
    ID_ACTIVIDAD : int
    AI : Optional [int] = None
    AD : Optional [int] = None
    PI : Optional [int] = None
    PD : Optional [int] = None
    Chequeo_revision : Optional[str] = None
    Ubre_sana : Optional [float] = None
    Calificacion : Optional [float] = None
    GAP : Optional [float] = None
    act_model : ActInfo = None
    class Config:
        orm_mode = True 
 
#DB View results    
class Result_MastitisT(BaseModel):
    ID_Actividad : int
    ID_VACA : int
    Fecha  : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    AI : Optional [int] = None
    AD : Optional [int] = None
    PI : Optional [int] = None
    PD : Optional [int] = None
    Chequeo_revision : Optional[str] = None
    class Config:
        orm_mode = True 
        
class PartosT(BaseModel):
    IDparto : int
    ID_VACA : int
    Numero_Parto : Optional [int] = None
    Sire : Optional [int] = None
    ID_ACTIVIDAD : Optional [int] = None
    class Config:
        orm_mode = True 
    
class Parto_Requi(BaseModel):
    ID_VACA : int
    ID_TipoOperacion : int = 1
    ID_Resultado : int = 1
    ID_OPERARIO : int = 35
    ID_Categoria : int = 1
    Fecha  : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #None
    Comentario : Optional[str] = None
    Fecha_programada : Optional[datetime] = None
    Sire : Optional [int] = None
    class Config:
        orm_mode = True 

class Ubicacion_VacasT(BaseModel):
    ID_VACA : Optional [int] = None
    ID_HATO : Optional [int] = None
    ID_LOTE : Optional [int] = None
    class Config:
        orm_mode = True 

class Ubicacion_VacasBasic(BaseModel):
    #ID_VACA : Optional [int] = None
    ID_HATO : Optional [int] = None
    ID_LOTE : Optional [int] = None    
    class Config:
        orm_mode = True 

class Ubicacion_VacasBasic2(BaseModel):
    ID_VACA : Optional [int] = None
    ID_HATO : Optional [int] = None
    #ID_LOTE : Optional [int] = None    
    class Config:
        orm_mode = True

class Ubicacion_Vacas_FullT(BaseModel):
    ID_VACA : Optional [int] = None
    ID_HATO : Optional [int] = None
    ID_LOTE : Optional [int] = None
    Nombre_vaca : Optional[str] = None
    NOMBRE_LOTE : Optional[str] = None
    Nombre_Hato : Optional[str] = None
    class Config:
        orm_mode = True 

        
class Traslado_Vacas_id(BaseModel):
    ID_TRASLADO : int   
class Traslado_VacasT(Traslado_Vacas_id):
    Fecha_Traslado : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ID_VACA : int
    ID_HATO : int
    #ID_OPERARIO : Optional[int] = None #activar y simplificar esquemas
    class Config:
        orm_mode = True
        
class CriasT(BaseModel):
    ID_CRIA : int
    ID_VACA : int
    ID_INSEMINACION : Optional[int] = None
    FECHA_NACIMIENTO : date
    class Config:
        orm_mode = True 

class celoT(BaseModel):
    #id_celo : int
    ID_vaca : int
    date : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    celotron : Optional[int] = None
    class Config:
        orm_mode = True 


class celo_get(celoT):
    id_celo : int
    class Config:
        orm_mode = True 


#Pesos
class peso_Requi(BaseModel):
    ID_VACA : int
    ID_TipoOperacion : int = 10
    ID_Resultado : int = 1
    ID_OPERARIO : int = 35
    ID_Categoria : int = 1
    Fecha  : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #None
    Comentario : Optional[str] = None
    Peso : int
    class Config:
        orm_mode = True 
        
   
class Incre_Pesos_View(BaseModel):
    ID_VACA : int
    Peso : int
    Fecha : Optional[datetime] = None
    previous_fecha : Optional[datetime] = None
    previous_peso : Optional[int] = None
    dif_fecha : Optional[int] = None
    dif_peso : Optional[int] = None
    Peso_gain_by_day : Optional[float] = None
    class Config:
        orm_mode = True
        
class Servicios_Requi(BaseModel):
    ID_VACA : int
    ID_TipoOperacion : int = 2
    ID_Resultado : int = 2
    ID_OPERARIO : int = 35
    ID_Categoria : int = 12 #Inseminacion
    Fecha  : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #None
    Comentario : Optional[str] = None
    Sire : Optional[int] = None
    ID_Embrion : Optional[int] = None
    class Config:
        orm_mode = True
    #IDservicio : int
    #ID_ACTIVIDAD : int
    
class DiagPre_Requi(BaseModel):
    ID_VACA : int
    ID_TipoOperacion : int = 7 #or 3 to 8
    ID_Resultado : int = 7 # or 6, 8, 9, 10
    ID_OPERARIO : int = 35
    ID_Categoria : int = 18 #Diag Pre
    Fecha  : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #None
    Comentario : Optional[str] = None
    ID_Resultado : int
    Dias : Optional[int] = None #Change to calculated field
    ID_servicio : Optional[int] = None
    class Config:
        orm_mode = True
    #IDdiagpre : int
    #ID_ACTIVIDAD : int

class Dificultad_PartoT(BaseModel):
    ID_dificultad: int
    Dificultad : str
    class Config:
        orm_mode = True


##########################################################################################################


#########################################    LECHE    #####################################################         
class Leche_HatosT(BaseModel):
    #ID_Leche_hato : int
    ID_HATO : int
    FECHA_ACTIVIDAD : datetime #datetime
    ID_OPERARIO : Optional[int] = None
    Comentario : Optional[str] = None
    Numero_Animales : Optional[int] = None
    Leche_Total : Optional [float] = None
    Hora : Optional[str] = None
    Antibiotico : Optional[str] = None
    Terneras : Optional[str] = None   
    class Config:
        orm_mode = True

class Leche_Hatosi(Leche_HatosT):
    ID_Leche_hato : int

class Leche_HatosU(BaseModel):
    #ID_Leche_hato : int
    ID_HATO : Optional[int] = None
    FECHA_ACTIVIDAD : Optional[datetime] = None  #datetime
    ID_OPERARIO : Optional[int] = None
    Comentario : Optional[str] = None
    Numero_Animales : Optional[int] = None
    Leche_Total : Optional [float] = None
    Hora : Optional[str] = None
    Antibiotico : Optional[str] = None
    Terneras : Optional[str] = None   
    class Config:
        orm_mode = True
        
class Leche_VacaT(BaseModel):
    #ID_Leche_vaca : int   
    ID_VACA : int
    ID_OPERARIO : Optional[int] = None
    Fecha_c : datetime #datetime
    Leche_lts : Optional [float] = None
    #Ciclo_Lactancia : Optional[int] = None
    #Numero_Partos : Optional[int] = None
    class Config:
        orm_mode = True 

class Leche_Vacai(Leche_VacaT):
    ID_Leche_vaca : int      

class Leche_VacaU(BaseModel):
    ID_VACA : Optional[int] = None
    ID_OPERARIO : Optional[int] = None
    Fecha_c : Optional[datetime] = None
    Leche_lts : Optional [float] = None
    #Ciclo_Lactancia : Optional[int] = None
    #Numero_Partos : Optional[int] = None
    class Config:
        orm_mode = True 

class Leche_EntregadaT(BaseModel):
    ID_CLIENTE : int
    Fecha :datetime
    Leche_entregada_lts :float
    class Config:
        orm_mode = True
        
class Leche_EntregadaF(Leche_EntregadaT):
    ID_Leche_Entregada : int

        
########################################## TANQUES   ##################################################
class Tanques_FincaT(BaseModel):
    ID_Finca : int
    Capacidad_Max : float
    Fecha_Creacion : Optional [datetime] = None
    deshabilitado : Optional [int] = None
    Fecha_deshabilitado : Optional [datetime] = None
    class Config:
        orm_mode = True

class Tanques_FincaF(Tanques_FincaT):
    ID_TANQUE : int


class Tanques_HatosT(BaseModel):
    ID_TANQUE : int
    ID_HATO : int 
    Fecha_Creacion : Optional [datetime] = None
    deshabilitado : Optional [int] = None
    Fecha_deshabilitado : Optional [datetime] = None
    class Config:
        orm_mode = True
        
class Tanques_HatosF(Tanques_HatosT):
    ID_TANQUE_HATO : int
 
        
class Leche_Tanque_DiariaT(BaseModel):
    ID_TANQUE : int
    Fecha : datetime
    Litros : float
    class Config:
        orm_mode = True
        
class Leche_Tanque_DiariaF(Leche_Tanque_DiariaT):
    ID : int
    
class Test_TanquesT(BaseModel):
    ID_TANQUE : int
    Fecha_Test: datetime
    Proveedor : str
    Cod_seguimiento : int
    Tipo_Muestra : str
    Estado : int
    class Config:
        orm_mode = True

class Test_TanquesF(Test_TanquesT):
    ID : int


class Resultados_TanquesT(BaseModel):
    ID_TANQUE : int
    Fecha_recepcion : datetime
    Fecha_resultado : datetime
    Cod_seguimiento : int
    GRASA : float
    PROTEINA : float
    SOLIDOS_TOTALES : float
    LACTOSA : float
    MUN : float
    UFC : float
    RCS : float
    class Config:
        orm_mode = True

class Resultados_TanquesF(Resultados_TanquesT):
    ID : int
    #RELACION_GP : float

##########################################################################################################

######################################### OTRAS FUENTES LOTES   #########################################
class Lotes_variablesT(BaseModel):
    ID_lote : int
    fecha : Optional[date] = None
    Mean_BM : Optional [float] = None
    Mean_CP : Optional [float] = None
    Mean_NDF : Optional [float] = None
    Mean_LAI : Optional [float] = None
    Mean_NDVI : Optional [float] = None
    cld_percentage : Optional [float] = None
    area_factor : Optional [float] = None
    biomass_corrected : Optional [float] = None
    class Config:
        orm_mode = True
    
class Lotes_quimicosT(BaseModel):
    #ID_registro : int
    ID_lote : int
    Fecha_muestra : Optional[date] = None
    ID_muestra : Optional [int] = None
    Fecha_resultado : Optional[date] = None
    CE : Optional [float] = None
    PH : Optional [float] = None
    Nitrogeno : Optional [float] = None
    Fosforo : Optional [float] = None
    Potasio : Optional [float] = None
    Calcio : Optional [float] = None
    Magnesio : Optional [float] = None
    Sodio : Optional [float] = None
    Aluminio : Optional [float] = None
    Azufre : Optional [float] = None
    Cloro : Optional [float] = None
    Hierro : Optional [float] = None
    Manganeso : Optional [float] = None
    Cobre : Optional [float] = None
    Zinc : Optional [float] = None
    Boro : Optional [float] = None
    Comentarios : Optional [str] = None
    class Config:
        orm_mode = True
        
class Lotes_quimicosi(Lotes_quimicosT):
    ID_registro : int

###########################################################################################################

##########################################  Monitoreo procesamiento imagenes satel   ######################
class monitoreo_descargas_sentinelT(BaseModel):
    zona : str
    file : str
    fecha  : date
    process_date :datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    class Config:
        orm_mode = True

###########################################################################################################

########################################   ESTACION METEOROLOGICA   #######################################
class MeteorologiaT(BaseModel):
    ID_Estacion : int
    #ID_CLIENTE : int
    FECHA_HORA : date
    activacion : Optional [int] = None
    DHT_Humidity_mean : Optional [float] = None
    DHT_Humidity_max : Optional [float] = None
    DHT_Humidity_min : Optional [float] = None
    DHT_Humidity_std : Optional [float] = None
    DHT_Temp_mean : Optional [float] = None
    DHT_Temp_max : Optional [float] = None
    DHT_Temp_min : Optional [float] = None
    Hum_Gnd_mean : Optional [float] = None
    Rain_mm_sum : Optional [float] = None
    Thermo_Couple_mean : Optional [float] = None
    Thermo_Couple_max : Optional [float] = None
    Thermo_Couple_min : Optional [float] = None
    Wind_Dir_Moda : Optional [str] = None
    Wind_Speed_mean : Optional [float] = None
    Wind_Speed_max : Optional [float] = None
    DS18b20_cap_mean : Optional [float] = None
    DS18b20_cap_max : Optional [float] = None
    DS18b20_cap_min : Optional [float] = None
    Solar_Volt_mean : Optional [float] = None
    Solar_Volt_max : Optional [float] = None
    Solar_Volt_min : Optional [float] = None
    Solar_Volt_std : Optional [float] = None
    Sunlight_mean : Optional [float] = None
    Sunlight_max : Optional [float] = None
    Sunlight_min : Optional [float] = None
    Sunlight_std : Optional [float] = None
    Count_Report : Optional [int] = None
    class Config:
        orm_mode = True  

class EstacionesT(BaseModel):
    ID_Estacion : int
    ID_Finca : Optional [int] = None
    comentarios : Optional [str] = None
    Fecha_instalacion : Optional [datetime] = None
    deshabilitado : Optional [int] = None
    Fecha_deshabilitado : Optional [datetime] = None

class Meteo_iot(BaseModel):
    ID_Estacion : int
    Date_Time : datetime
    DHT_Humidity : Optional [float] = None
    DHT_Temp : Optional [float] = None
    DS18b20_cap : Optional [float] = None
    Hum_Gnd : Optional [float] = None
    Rain_mm : Optional [float] = None
    Solar_Volt : Optional [float] = None
    Sunlight : Optional [float] = None
    Thermo_Couple : Optional [float] = None
    Wind_Dir : Optional [str] = None
    Wind_Speed : Optional [float] = None
    class Config:
        orm_mode = True 
###########################################################################################################