# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:10:03 2020

@author: Marcelo
"""

from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel #, Field

#option expanded
#class ClienteBase(BaseModel):
#    NOMBRE: str


#class ClienteCreate(ClienteBase):
#    pass

class ClientesT(BaseModel):
    ID_CLIENTE: int
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

class Clientes_id(BaseModel):
    ID_CLIENTE: int
    
class ClientesCreate(Clientes_id):
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
        


#other tables    
#class OperarioBase(BaseModel):
#    NombreOperario: str

'''
class OperarioCreate(BaseModel):
    ID_OPERARIO: int
    ID_CLIENTE: int
    ID_FINCA: int
    NombreOperario: str
    FechaDeIngreso: date
    Telefono: int
    Rol: str
    Descripcion: str
    Email: str
    Direccion: str
    class Config:
        orm_mode = True
    #pass
'''
#class OperarioDelete(BaseModel):
#    ID_OPERARIO: int #= Field(..., example="Enter ID to delete")

class Operario_id(BaseModel): 
    ID_OPERARIO: int
    
class OperarioT(Operario_id): 
    ID_CLIENTE: int
    ID_FINCA: int
    NombreOperario: str
    FechaDeIngreso: Optional[date] = None
    Telefono: Optional[int] = None
    Rol: Optional[str] = None
    Descripcion: Optional[str] = None
    Email: Optional[str] = None
    Direccion: Optional[str] = None
    class Config:
        orm_mode = True


class LotesT(BaseModel): 
    ID_LOTE: int
    #ID_CLIENTE: int
    ID_FINCA: int
    NOMBRE_LOTE: Optional[str] = None
    LATITUD: Optional[float] = None
    LONGITUD: Optional[float] = None
    AREA: Optional[float] = None
    DESCRIPCION: Optional[str] = None
    #finca_madre: int
    class Config:
        orm_mode = True

class LotesT2(BaseModel): 
    NOMBRE_LOTE: Optional[str] = None
    class Config:
        orm_mode = True
        
#class Lote_list(LotesT):
#    ID_LOTE: int
#    ID_FINCA: int
#    NOMBRE_LOTE: str
#    class Config:
#        orm_mode = True

        
class FincaT(BaseModel):
    ID_FINCA: int
    ID_cliente: int
    NOMBRE: Optional[str] = None
    DESCRIPCION: Optional[str] = None
    lotes_list: List[LotesT] = []
    class Config:
        orm_mode = True
        

class HatosT(BaseModel):
    ID_HATO : int
    ID_CLIENTE : int
    ID_FINCA : int
    Nombre_Hato : Optional[str] = None
    TIPO_Hato : Optional[str] = None
    Descripcion : Optional[str] = None
    class Config:
        orm_mode = True
        
class HatosT2(BaseModel):
    Nombre_Hato : Optional[str] = None
    class Config:
        orm_mode = True
        
class Leche_HatosT(BaseModel):
    #ID_Leche_hato : int
    ID_HATO : int
    FECHA_ACTIVIDAD : date
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

class VacasT(BaseModel):
    ID_VACA : int
    ID_CLIENTE : int
    ID_FINCA : int
    ElectronicID : Optional[str] = None
    Nombre_Vaca : str
    Raza : Optional[int] = None
    Sexo : Optional[int] = None
    #FECHA_NACIMIENTO : Optional[date] = None
    VacaMadre : Optional[int] = None
    IDparto : Optional[int] = None
    FechaRegistro : Optional[date] = None
    IDTipoOrigen : Optional[int] = None
    FechaNacimiento : Optional[date] = None
    IDTipoSalida : Optional[int] = None
    FechaSalida : Optional[date] = None
    #FECHA_NACIMIENTO = Column(Date, nullable=True)   
    Sire : Optional[int] = None    
    Estado : Optional[int] = None
    Estado_Final : Optional[int] = None 
    class Config:
        orm_mode = True   
        
class VacasT2(BaseModel):
    #ID_VACA : int
    Nombre_Vaca : str
    class Config:
        orm_mode = True 
        
class Leche_VacaT(BaseModel):
    #ID_Leche_vaca : int   
    ID_VACA : int
    ID_OPERARIO : Optional[int] = None
    FECHA : date
    Litros : Optional [float] = None
    Ciclo_Lactancia : Optional[int] = None
    Numero_Partos : Optional[int] = None
    class Config:
        orm_mode = True 

class Leche_Vacai(Leche_VacaT):
    ID_Leche_vaca : int      

       
class MeteorologiaT(BaseModel):
    ID_FINCA : int
    ID_CLIENTE : int
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
    class Config:
        orm_mode = True  

########################## TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user: str

######################### USER sec schemas    
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

################### USER sec alternative
class User(BaseModel):
    user: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    active_status: Optional[int] = None
    id_user_rol : Optional[int] = None
    ID_CLIENTE : Optional[int] = None
    ID_OPERARIO : Optional[int] = None
    
class UserInDB(User):
    password: str

class UserInfo2(User):
    id: int
    class Config:
        orm_mode = True
################  


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

class Mast_Requi(BaseModel):
    ID_VACA : int
    ID_TipoOperacion : int = 9
    ID_Resultado : int = 34
    ID_OPERARIO : int = 35
    ID_Categoria : int = 1
    Fecha  : Optional[date] = datetime.now().strftime("%Y-%m-%d") #None
    Comentario : Optional[str] = None
    AI : Optional [int] = None
    AD : Optional [int] = None
    PI : Optional [int] = None
    PD : Optional [int] = None
    Chequeo_revision : Optional[str] = None
    class Config:
        orm_mode = True 
        
class ActInfoBase(BaseModel):
    ID_Actividad : int

class ActInfo(ActInfoBase):
    ID_VACA : int
    ID_TipoOperacion : int = 9
    ID_Resultado : int = 34
    ID_OPERARIO : int = 35
    ID_Categoria : int = 1
    Fecha  : Optional[date] = None
    Comentario : Optional[str] = None
    class Config:
        orm_mode = True 
'''        
class Act_Requi(BaseModel):
    ID_VACA : int
    ID_TipoOperacion : int = 9
    ID_Resultado : int = 34
    ID_OPERARIO : int = 35
    ID_Categoria : int = 1
    Fecha  : Optional[date] = None
    Comentario : Optional[str] = None
    class Config:
        orm_mode = True 
'''
 
class Ubicacion_VacasT(BaseModel):
    ID_VACA : Optional [int] = None
    ID_HATO : Optional [int] = None
    ID_LOTE : Optional [int] = None
    #Nombre_Vaca : str
    #Nombre_Vaca: Optional[str] = None
    nombre_vaca: VacasT2 = None
    nombre_hato: HatosT2 = None
    nombre_lote: LotesT2 = None
    
    class Config:
        orm_mode = True 

class Ubicacion_VacasBasic(BaseModel):
    ID_VACA : Optional [int] = None
    ID_HATO : Optional [int] = None
    ID_LOTE : Optional [int] = None    
    class Config:
        orm_mode = True 

        
class Traslado_Vacas_id(BaseModel):
    ID_TRASLADO : int   
class Traslado_VacasT(Traslado_Vacas_id):
    Fecha_Traslado : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ID_VACA : int
    ID_HATO : int
    class Config:
        orm_mode = True

class Traslado_Hatos_id(BaseModel):
    ID_TRASLADO_HATO : int
class Traslado_HatosT(Traslado_Hatos_id):
    Fecha_Traslado : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ID_HATO : int
    ID_LOTE : int
    class Config:
        orm_mode = True