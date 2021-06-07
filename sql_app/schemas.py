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

class OperarioN(BaseModel): 
    ID_CLIENTE: Optional[int] = None
    ID_FINCA: Optional[int] = None
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

class LotesT(BaseModel): 
    ID_LOTE: int
    #ID_CLIENTE: int
    ID_FINCA: int
    NOMBRE_LOTE: Optional[str] = None
    LATITUD: Optional[float] = None
    LONGITUD: Optional[float] = None
    AREA: Optional[float] = None
    DESCRIPCION: Optional[str] = None
    ID_variedad: Optional[int] = None
    #finca_madre: int
    class Config:
        orm_mode = True

class LotesT2(BaseModel): 
    NOMBRE_LOTE: Optional[str] = None
    class Config:
        orm_mode = True

class LotesN(BaseModel): 
    #ID_LOTE: int
    ID_FINCA: Optional[int] = None
    NOMBRE_LOTE: Optional[str] = None
    LATITUD: Optional[float] = None
    LONGITUD: Optional[float] = None
    AREA: Optional[float] = None
    DESCRIPCION: Optional[str] = None
    ID_variedad: Optional[int] = None
    #finca_madre: int
    class Config:
        orm_mode = True

class LotesPasto(BaseModel): 
    ID_LOTE: int
    ID_variedad: Optional[int] = None
    class Config:
        orm_mode = True
        
class LoteInfo2(LotesN):
    ID_LOTE: int
    class Config:
        orm_mode = True
        
class Actividades_LotesT(BaseModel):
    ID_ACT_LOTE : int
    ID_LOTE : int
    FECHA_ACTIVIDAD  : datetime #datetime
    ID_Tipo_Actividad : int
    Producto : Optional[str] = None
    ID_OPERARIO : int
    Comentario : Optional[str] = None
    Fecha_programada : Optional[datetime] = None
    Estado : Optional[int] = None
    class Config:
        orm_mode = True
        

class Tipo_Actividades_LotesT(BaseModel):
    IDTipo_Actividades_Lotes : int
    Code : str
    Nombre  : str
    ID_Categoria_Act : int
    class Config:
        orm_mode = True
        
class FincaT(BaseModel):
    ID_FINCA: int
    ID_cliente: int
    NOMBRE: Optional[str] = None
    DESCRIPCION: Optional[str] = None
    lotes_list: List[LotesT] = []
    class Config:
        orm_mode = True
  
class FincaP(BaseModel):
    #ID_FINCA: int #posiblemente quitar, para que no se defina por el usuario
    ID_cliente: int
    NOMBRE: Optional[str] = None
    DESCRIPCION: Optional[str] = None
    #lotes_list: List[LotesT] = []
    class Config:
        orm_mode = True

class FincaR(BaseModel):
    ID_FINCA: int
    ID_cliente: int
    NOMBRE: Optional[str] = None
    #DESCRIPCION: Optional[str] = None
    #lotes_list: List[LotesT] = []
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
        
class HatosP(BaseModel):
    #ID_HATO : int = 0 #posiblemente quitar, para que no se defina por el usuario
    ID_CLIENTE : int
    ID_FINCA : int
    Nombre_Hato : Optional[str] = None
    TIPO_Hato : Optional[str] = None
    Descripcion : Optional[str] = None
    class Config:
        orm_mode = True
        
class HatosR(BaseModel):
    ID_HATO : int
    ID_CLIENTE : int
    ID_FINCA : int
    Nombre_Hato : Optional[str] = None
    class Config:
        orm_mode = True
        
class HatosT2(BaseModel):
    Nombre_Hato : Optional[str] = None
    class Config:
        orm_mode = True
        
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

class VacasT(BaseModel):
    ID_VACA : int
    ID_CLIENTE : int
    #ID_FINCA : int
    ElectronicID : Optional[str] = None
    Nombre_Vaca : str
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
    #Estado : Optional[int] = None
    #Estado_Final : Optional[int] = None 
    class Config:
        orm_mode = True   
        
class VacasT2(BaseModel):
    #ID_VACA : int
    Nombre_Vaca : str
    class Config:
        orm_mode = True 

class VacasR(BaseModel):
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
    
class VacaInfo2(VacaN):
    ID_VACA: int
    class Config:
        orm_mode = True

#

class CriasT(BaseModel):
    ID_CRIA : int
    ID_VACA : int
    ID_INSEMINACION : Optional[int] = None
    FECHA_NACIMIENTO : date
    class Config:
        orm_mode = True 
        
class Leche_VacaT(BaseModel):
    #ID_Leche_vaca : int   
    ID_VACA : int
    ID_OPERARIO : Optional[int] = None
    FECHA : date #datetime
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
#privileges

class API_Users_PrivT(BaseModel):
    id_user_rol : int
    name : Optional[str] = None
    description : Optional[str] = None
    class Config:
        orm_mode = True
    
#################

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
    #Nombre_Vaca : str
    #Nombre_Vaca: Optional[str] = None
    #nombre_vaca: VacasT2 = None
    #nombre_hato: HatosT2 = None
    #nombre_lote: LotesT2 = None
    
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
    ID_registro : int
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
        
class monitoreo_descargas_sentinelT(BaseModel):
    ID_cliente : int
    zona : Optional [str] = None
    file : Optional [str] = None
    municipio : Optional [str] = None
    departamento : Optional [str] = None
    fecha  : Optional[date] = None
    mode : Optional [str] = None
    machine_name : Optional [str] = None
    duration : Optional [float] = None
    end_time : Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prct_clouds : Optional [float] = None
    class Config:
        orm_mode = True
        
class razaT(BaseModel):
    ID_RAZA : int
    Codigo : Optional [str] = None
    Nombre : Optional [str] = None
    Gestacion : Optional [int] = None 
    MaxGestacion : Optional [int] = None
    MinGestacion  : Optional [int] = None
    Leche : Optional [str] = None
    Carne : Optional [str] = None
    Pureza : Optional [float] = None
    class Config:
        orm_mode = True
        
class razaR(BaseModel):
    ID_RAZA : int
    Codigo : Optional [str] = None
    Nombre : Optional [str] = None
    class Config:
        orm_mode = True
    
class sexoT(BaseModel):
    idSexo : int
    Codigo : Optional [str] = None
    Nombre : Optional [str] = None
    Genero : Optional [int] = None 
    VacaRep : Optional [int] = None
    ToroRep  : Optional [int] = None
    class Config:
        orm_mode = True  
    
class tipo_destinoT(BaseModel):   
    IDTipo_Destino : int
    Nombre : Optional [str] = None
    Descripcion : Optional [str] = None
    class Config:
        orm_mode = True
        
class tipo_operacionesT(BaseModel):
    ID_TipoOperaciones : int
    Codigo : Optional [str] = None
    Nombre : Optional [str] = None
    class Config:
        orm_mode = True
        
class Actividades_vacas_categoriaT(BaseModel):   
    ID_Categoria : int
    Nombre : Optional [str] = None
    Descripcion : Optional [str] = None
    class Config:
        orm_mode = True
        
class Actividades_vacas_resultadoT(BaseModel):   
    ID_Resutlado : int
    Nombre : Optional [str] = None
    Descripcion : Optional [str] = None
    class Config:
        orm_mode = True