# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 19:18:16 2020

@author: Marcelo
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float#, Date
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date, DateTime, Time
from .database import Base #deploy
#from database import Base #local
'''
When accessing the attribute items in a User, as in my_user.items, it will have a list of Item SQLAlchemy models (from the items table) that have a foreign key pointing to this record in the users table.

When you access my_user.items, SQLAlchemy will actually go and fetch the items from the database in the items table and populate them here.

And when accessing the attribute owner in an Item, it will contain a User SQLAlchemy model from the users table. It will use the owner_id attribute/column with its foreign key to know which record to get from the users table.

'''
#######################     USERS   ###################################################
class API_UsersT(Base):
    __tablename__ = "API_Users"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(45))
    full_name = Column(String(45)) #, ForeignKey("Operario.NombreOperario"))
    email = Column(String(45))
    password = Column(String(99))
    active_status = Column(Integer, nullable=True)
    id_user_rol = Column(Integer, ForeignKey("API_Users_Privileges.id_user_rol"), nullable=True)
    ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID_CLIENTE"), nullable=True)
    ID_OPERARIO = Column(Integer, ForeignKey("Operario.ID_OPERARIO"), nullable=True)
    Deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)


class API_Users_PrivT(Base):
    __tablename__ = "API_Users_Privileges"
    id_user_rol = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=True)
    description= Column(String(45), nullable=True)
    Deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)


class PermisosT(Base):
    __tablename__ = "Permisos"
    ID_permisos = Column(Integer, primary_key=True, index=True)
    User_ID = Column(Integer, ForeignKey("API_Users.id"))
    Crear = Column(Integer)
    Activar_User = Column(Integer)
    Imagenes_Sat = Column(Integer)
    Leche = Column(Integer)
    Hatos_Traslado = Column(Integer)
    Hatos_Suplementa = Column(Integer)
    Hatos_Servicios = Column(Integer)
    Animales_Traslados = Column(Integer)
    Animales_Mastitis = Column(Integer)
    Animales_CrearEditar = Column(Integer)
    Animales_Examenes = Column(Integer)
    Animales_Salud = Column(Integer)
    Lotes = Column(Integer)


class API_Users_FincasT(Base):
    __tablename__ = "API_Users_Fincas"
    ID = Column(Integer, primary_key=True, index=True)
    ID_user = Column(Integer,  ForeignKey("API_Users.id"))
    ID_FINCA = Column(Integer, ForeignKey("Finca.ID_FINCA"), nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)


class Roles_tablasT(Base):
    __tablename__ = "Roles_tablas"
    id = Column(Integer, primary_key=True, index=True)
    Rol = Column(String(32), nullable=True)
    API_method = Column(String(32), nullable=True)
    Permiso = Column(Integer)

#Permisos_Tipo


###################################################################################################


############################       CLIENTS      ###############################################
class ClientesT(Base):
    __tablename__ = "clientes" #nombre de la tabla de la DB
    ID_CLIENTE = Column(Integer, primary_key=True, index=True) #
    NOMBRE = Column(String(32), nullable=True) #definicion de cada columna, con tipo
    NIT_CC = Column(Integer, nullable=True)
    RAZON_SOCIAL = Column(String(32), nullable=True)
    TELEFONO = Column(Integer, nullable=True)
    EMAIL = Column(String(32), nullable=True)
    DIRECCION = Column(String(32), nullable=True)
    CIUDAD = Column(String(32), nullable=True)
    DEPARTAMENTO = Column(String(32), nullable=True)
    DESCRIPCION = Column(String(45), nullable=True)
    FECHA_CONTRATO = Column(Date, nullable=True)
    FECHA_VENCIMIENTOCO = Column(Date, nullable=True)
    ESTADO = Column(String(33), nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)
    Fecha_Hoy = Column(DateTime, nullable=True)
    Dias_vencimiento = Column(DateTime, nullable=True)


####################################################################################################


##################################      OPERARIOS    #################################################
class OperarioT(Base):
    __tablename__ = "Operario"
    ID_OPERARIO = Column(Integer, primary_key=True, index=True)
    ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID_CLIENTE"))
    NombreOperario = Column(String(32))
    FechaDeIngreso = Column(Date, nullable=True)
    Telefono = Column(Integer, nullable=True)
    Rol = Column(String(140), nullable=True)
    Descripcion = Column(String(140), nullable=True)
    Email = Column(String(32), nullable=True)
    Direccion = Column(String(32), nullable=True)
    Fecha_Creacion = Column(DateTime, nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)

class Operario_Sin_UserT(Base):
    __tablename__ = "Operario_sin_user"
    ID_OPERARIO = Column(Integer, ForeignKey("Operario.ID_OPERARIO"), primary_key=True, index=True)
    NombreOperario = Column(String(32))
    ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID_CLIENTE"))

class Operarios_FincasT(Base):
    __tablename__ = "Operarios_Fincas"
    ID = Column(Integer, primary_key=True, index=True)
    ID_OPERARIO = Column(Integer, ForeignKey("Operario.ID_OPERARIO"))
    ID_FINCA = Column(Integer, ForeignKey("Finca.ID_FINCA"))
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)

##########################################################################################################


#################################     FINCAS     #########################################################
class FincaT(Base):
    __tablename__ = "Finca"
    ID_FINCA = Column(Integer, primary_key=True, index=True)
    ID_cliente = Column(Integer, ForeignKey("clientes.ID_CLIENTE"))
    NOMBRE = Column(String(32), nullable=True)
    DESCRIPCION = Column(String(134), nullable=True)
    sentinel_zone =  Column(String(32),ForeignKey("monitoreo_descargas_sentinel.zona"), nullable=True)
    Fecha_Creacion = Column(DateTime, nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)
    ID_Zone_sentinel = Column(Integer, nullable=True)
    lotes_list = relationship("LotesT", back_populates="finca_madre")
    
###########################################################################################################


###########################################    LOTES    ###################################################
class LotesT(Base):
    __tablename__ = "lotes"
    ID_LOTE = Column(Integer, primary_key=True, index=True)
    ID_FINCA = Column(Integer, ForeignKey("Finca.ID_FINCA"))
    NOMBRE_LOTE = Column(String(32))
    LATITUD = Column(Float, nullable=True)
    LONGITUD = Column(Float, nullable=True)
    AREA = Column(Float, nullable=True)
    DESCRIPCION = Column(String(45), nullable=True)
    ID_variedad = Column(Integer, ForeignKey("tipo_cultivo.ID_variedad"), nullable=True)
    Fecha_Creacion = Column(DateTime, nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)
    finca_madre = relationship("FincaT", back_populates="lotes_list")
    

class tipo_cultivoT(Base):
    __tablename__ = "tipo_cultivo"
    ID_cultivo = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(45), nullable=True)
    clase = Column(String(45), nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)
    
class variedad_cultivoT(Base):
    __tablename__ = "variedad_cultivo"
    ID_variedad = Column(Integer, primary_key=True, index=True)
    ID_cultivo = Column(Integer, ForeignKey("tipo_cultivo.ID_cultivo"))
    nombre = Column(String(45), nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)
    
#Lotes_geometry
###########################################################################################################


#########################################  ACTIVIDADES LOTES  ############################################
class Actividades_LotesT(Base):
    __tablename__ = "Actividades_Lotes"
    ID_ACT_LOTE = Column(Integer, primary_key=True, index=True)
    ID_LOTE = Column(Integer, ForeignKey("lotes.ID_LOTE"))
    FECHA_ACTIVIDAD = Column(DateTime)
    ID_Tipo_Actividad = Column(Integer, ForeignKey("Tipo_Actividades_Lotes.IDTipo_Actividades_Lotes"))
    Producto = Column(String(45), nullable=True)
    ID_OPERARIO = Column(Integer, ForeignKey("Operario.ID_OPERARIO"))
    Comentario = Column(String(45), nullable=True)
    Fecha_programada = Column(DateTime, nullable=True)
    Estado = Column(Integer, nullable=True)
    

class Tipo_Actividades_LotesT(Base):
    __tablename__ = "Tipo_Actividades_Lotes"
    IDTipo_Actividades_Lotes = Column(Integer, primary_key=True, index=True)
    Code = Column(String(45))
    Nombre = Column(String(45))
    ID_Categoria_Act = Column(Integer)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)

class AforoT(Base):
    __tablename__ = "Aforo"
    ID_ACTIVIDAD = Column(Integer, ForeignKey("Actividades_Lotes.ID_ACT_LOTE"), primary_key=True)
    Aforo = Column(Float)
    
class Ultimas_Act_LotesT(Base):
    __tablename__ = "Ultimas_Act_Lotes"
    ID_ACT_LOTE = Column(Integer, ForeignKey("Actividades_Lotes.ID_ACT_LOTE"), primary_key=True)
    ID_LOTE = Column(Integer, ForeignKey("lotes.ID_LOTE"))
    FECHA_ACTIVIDAD = Column(DateTime)
    ID_Tipo_Actividad = Column(Integer, ForeignKey("Tipo_Actividades_Lotes.IDTipo_Actividades_Lotes"))
    Dias = Column(Integer, nullable=True)
    

class Categoria_Actividades_LotesT(Base):
    __tablename__ = "Categoria_Actividades_Lotes"
    ID_Categoria_Act_Lote = Column(Integer, primary_key=True, index=True)
    Code = Column(String(45))
    Nombre = Column(String(45))
    Deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)
###########################################################################################################


########################################    HATOS     ####################################################    
class HatosT(Base):
    __tablename__ = "Hatos"
    ID_HATO = Column(Integer, primary_key=True, index=True)
    ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID_CLIENTE"))
    ID_FINCA = Column(Integer, ForeignKey("Finca.ID_FINCA"))
    Nombre_Hato = Column(String(45), nullable=True)
    TIPO_Hato = Column(String(32), nullable=True)
    Descripcion = Column(String(32), nullable=True)
    Fecha_Creacion = Column(DateTime, nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)

class Traslado_HatosT(Base):
    __tablename__ = "Traslado_Hatos"
    ID_TRASLADO_HATO = Column(Integer, primary_key=True, index=True)
    Fecha_Traslado = Column(DateTime)
    ID_HATO = Column(Integer, ForeignKey("Hatos.ID_HATO"))
    ID_LOTE = Column(Integer, ForeignKey("lotes.ID_LOTE"))
    ID_OPERARIO = Column(Integer, ForeignKey("Operario.ID_OPERARIO"), nullable=True)

#RangoFechas_Hato
###########################################################################################################


#############################################   VACAS    #################################################    
class VacasT(Base):
    __tablename__ = "vacas"
    ID_VACA = Column(Integer, primary_key=True, index=True)
    ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID_CLIENTE"))
    ElectronicID = Column(String(32), nullable=True)
    Nombre_Vaca = Column(String(32))
    Raza = Column(Integer, ForeignKey("Raza.ID_RAZA"), nullable=True)
    Sexo = Column(Integer, nullable=True)
    VacaMadre = Column(Integer, nullable=True)
    IDparto = Column(Integer, nullable=True)
    FechaRegistro = Column(Date, nullable=True)
    IDTipoOrigen = Column(Integer, nullable=True)
    FechaNacimiento = Column(Date, nullable=True)
    IDTipoSalida = Column(Integer, nullable=True)
    FechaSalida = Column(Date, nullable=True)
    Sire = Column(Integer, nullable=True)
    
class razaT(Base):
    __tablename__ = "Raza"
    ID_RAZA= Column(Integer,  primary_key=True)
    Codigo = Column(String(11), nullable=True)
    Nombre = Column(String(45), nullable=True)
    Gestacion = Column(Integer, nullable=True)
    MaxGestacion = Column(Integer, nullable=True)
    MinGestacion  = Column(Integer, nullable=True)
    Leche = Column(String(33), nullable=True)
    Carne = Column(String(33), nullable=True)
    Pureza = Column(Float, nullable=True)
    Fecha_Creacion = Column(DateTime, nullable=True)
    Deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)
    
class sexoT(Base):
    __tablename__ = "Sexo"
    idSexo= Column(Integer,  primary_key=True)
    Codigo = Column(String(4), nullable=True)
    Nombre = Column(String(45), nullable=True)
    Genero = Column(Integer, nullable=True)
    VacaRep = Column(Integer, nullable=True)
    ToroRep  = Column(Integer, nullable=True)
    Fecha_Creacion = Column(DateTime, nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)

class tipo_destinoT(Base):
    __tablename__ = "Tipo_Destino"
    IDTipo_Destino= Column(Integer,  primary_key=True)
    Nombre = Column(String(45), nullable=True)
    Descripcion = Column(String(45), nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)

class siresT(Base):
    __tablename__ = "Sires"
    IDsire= Column(Integer,  primary_key=True)
    Active = Column(Integer, nullable=True)
    IDOfficial = Column(String(45),  nullable=True)
    AINumber = Column(String(45),  nullable=True)
    Nombre_Largo = Column(String(45), nullable=True)
    Registro = Column(String(45), nullable=True)
    Raza = Column(Integer, nullable=True)
    #Fecha_descontinuado = Column(DateTime, nullable=True)
    Fecha_Creacion = Column(DateTime, nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)
    
#Estado_vaca = remover y hacer en forma de View
#Tipo_Origen
class tipo_origenT(Base):
    __tablename__ = "Tipo_origen"
    IDTipo_origen= Column(Integer,  primary_key=True)
    Nombre = Column(String(45), nullable=True)
    Descripcion = Column(String(45), nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)

class eventosT(Base):
    __tablename__ = "eventos"
    ID_evento= Column(Integer,  primary_key=True)
    evento = Column(String(45), nullable=True)

class Precios_VacasT(Base):
    __tablename__ = "Precios_Vacas"
    ID_Precios= Column(Integer,  primary_key=True)
    ID_Vaca = Column(Integer,  ForeignKey("vacas.ID_VACA"))
    ID_razon = Column(Integer, ForeignKey("eventos.ID_evento"))
    Fecha = Column(DateTime, nullable=True)
    precio = Column(Integer, nullable=True)
    tipo_moneda = Column(String(45), nullable=True)
#########################################################################################################


###########################################   ACTIVIDADES VACAS   #########################################
class tipo_operacionesT(Base):
    __tablename__ = "Tipo_operaciones"
    ID_TipoOperaciones= Column(Integer,  primary_key=True)
    Codigo = Column(String(45), nullable=True)
    Nombre = Column(String(45), nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)
    #evento_vs_cate = relationship('Eventos_vs_categoriasT')

class MastitisT(Base):
    __tablename__ = "Mastitis"
    ID_ACTIVIDAD = Column(Integer, ForeignKey("Actividades_Vacas.ID_Actividad"), primary_key=True, index=True)#, ForeignKey("Actividades_Vacas.ID_FINCA"))
    AI = Column(Integer, nullable=True)
    AD = Column(Integer, nullable=True)
    PI = Column(Integer, nullable=True)
    PD = Column(Integer, nullable=True)
    Chequeo_revision = Column(String(45), nullable=True)
    Ubre_sana = Column(Float, nullable=True)
    Calificacion = Column(Float, nullable=True)
    GAP = Column(Float, nullable=True)

class Result_MastitisT(Base):
    __tablename__ = "Result_Mastitis"
    ID_Actividad = Column(Integer, ForeignKey("Actividades_Vacas.ID_Actividad"), primary_key=True, index=True)#, ForeignKey("Actividades_Vacas.ID_FINCA"))
    ID_VACA = Column(Integer, ForeignKey("vacas.ID_VACA"))
    Fecha = Column(Date, nullable=True)
    AI = Column(Integer, nullable=True)
    AD = Column(Integer, nullable=True)
    PI = Column(Integer, nullable=True)
    PD = Column(Integer, nullable=True)
    Chequeo_revision = Column(String(45), nullable=True)

    
class PartosT(Base):
    __tablename__ = "Partos"
    IDparto = Column(Integer, primary_key=True, index=True)
    ID_VACA = Column(Integer, ForeignKey("vacas.ID_VACA"))
    Numero_Parto = Column(Integer, nullable=True)
    Sire = Column(Integer, nullable=True)
    ID_ACTIVIDAD = Column(Integer, ForeignKey("Actividades_Vacas.ID_Actividad"), nullable=True)
    Dificultad = Column(String(250), nullable=True)

class ActividadesVacasT(Base):
    __tablename__ = "Actividades_Vacas"
    ID_Actividad = Column(Integer, primary_key=True, index=True)
    ID_VACA = Column(Integer, ForeignKey("vacas.ID_VACA"))
    ID_TipoOperacion = Column(Integer)
    ID_Resultado = Column(Integer, ForeignKey("Actividades_vacas_resultado.ID_Resultado"))
    ID_OPERARIO = Column(Integer, ForeignKey("Operario.ID_OPERARIO"))
    ID_Categoria = Column(Integer)
    Fecha = Column(Date, nullable=True)
    Comentario = Column(String(450), nullable=True)

class ActividadesVacasView(Base):
    __tablename__ = "Actividades_vacas_view"
    ID_Actividad = Column(Integer, ForeignKey("Actividades_Vacas.ID_Actividad"), primary_key=True, index=True)
    Vaca = Column(String(45), ForeignKey("vacas.Nombre_Vaca"))
    Codigo_oper = Column(String(45), nullable=True)
    Operacion = Column(String(45), nullable=True)
    Resultado = Column(String(45), nullable=True)
    Categoria = Column(String(45), nullable=True)
    Operario = Column(String(45), nullable=True)
    Rol = Column(String(45), nullable=True)
    Fecha  = Column(Date, nullable=True)
    Comentario = Column(String(45), nullable=True)

class CriaT(Base):
    __tablename__ = "Cria"
    ID_CRIA = Column(Integer, primary_key=True, index=True)
    ID_VACA = Column(Integer, ForeignKey("vacas.ID_VACA"))
    ID_INSEMINACION = Column(Integer, nullable=True)
    FECHA_NACIMIENTO = Column(Date)

class Actividades_vacas_categoriaT(Base):
    __tablename__ = "Actividades_vacas_categoria"
    ID_Categoria= Column(Integer,  primary_key=True)
    Nombre = Column(String(45))
    Descripcion = Column(String(45), nullable=True)
    Deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)
    
class Actividades_vacas_resultadoT(Base):
    __tablename__ = "Actividades_vacas_resultado"
    ID_Resultado= Column(Integer,  primary_key=True)
    Nombre = Column(String(45))
    Descripcion = Column(String(45), nullable=True)
    Deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)



class Eventos_vs_categoriasT(Base):
    __tablename__ = "eventos_vs_categorias"
    ID_eventos_vs_categorias = Column(Integer,  primary_key=True)
    ID_evento = Column(Integer, ForeignKey("Tipo_operaciones.ID_TipoOperaciones"), nullable=True)
    ID_categoria = Column(Integer, ForeignKey("Actividades_vacas_categoria.ID_Categoria"), nullable=True)
    #evento = relationship('tipo_operacionesT', backref='eventos_vs_categorias',  uselist=False, lazy='joined')

class Eventos_vs_resultadosT(Base):
    __tablename__ = "eventos_vs_resultados"
    ID_eventos_vs_resultados = Column(Integer,  primary_key=True)
    ID_evento = Column(Integer, ForeignKey("Tipo_operaciones.ID_TipoOperaciones"), nullable=True)
    ID_resultado = Column(Integer, ForeignKey("Actividades_vacas_resultado.ID_Resultado"), nullable=True)





class Ubicacion_VacasT(Base):
    __tablename__ = "Ubicacion_Vacas"
    ID_VACA = Column(Integer, ForeignKey("vacas.ID_VACA"), primary_key=True)#, index=True)
    ID_HATO = Column(Integer, ForeignKey("Hatos.ID_HATO"))#, primary_key=True, index=True)
    ID_LOTE = Column(Integer, ForeignKey("lotes.ID_LOTE"))#, primary_key=True, index=True)
    #nombre_vaca = relationship("VacasT", backref="Ubicacion_Vacas", lazy='joined') #https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html
    #nombre_hato = relationship("HatosT", backref="Ubicacion_Vacas", lazy='joined')
    #nombre_lote = relationship("LotesT", backref="Ubicacion_Vacas", lazy='joined')

#DB View
class Ubicacion_Vacas_FullT(Base):
    __tablename__ = "ubica_vacas_full"
    ID_VACA = Column(Integer, ForeignKey("vacas.ID_VACA"), primary_key=True)
    ID_LOTE = Column(Integer, ForeignKey("lotes.ID_LOTE"))
    ID_HATO = Column(Integer, ForeignKey("Hatos.ID_HATO"))
    Nombre_vaca = Column(String(45), nullable=True)
    NOMBRE_LOTE = Column(String(45), nullable=True)
    Nombre_Hato = Column(String(45), nullable=True)
    
    
class Traslado_VacasT(Base):
    __tablename__ = "Traslado_Vacas"
    ID_TRASLADO = Column(Integer, primary_key=True, index=True)
    Fecha_Traslado = Column(DateTime)
    ID_VACA = Column(Integer, ForeignKey("vacas.ID_VACA"))
    ID_HATO = Column(Integer, ForeignKey("Hatos.ID_HATO"))
    ID_OPERARIO = Column(Integer, ForeignKey("Operario.ID_OPERARIO"), nullable=True)


#Pesos
class PesosT(Base):
    __tablename__ = "Pesos"
    IDpeso= Column(Integer, primary_key=True, index=True)
    ID_VACA = Column(Integer, ForeignKey("vacas.ID_VACA"))
    Peso = Column(Integer)
    ID_ACTIVIDAD = Column(Integer, ForeignKey("Actividades_Vacas.ID_Actividad"))
    
class Incre_Pesos_View(Base):
    __tablename__ = "incremento_pesos"
    ID_VACA= Column(Integer, ForeignKey("vacas.ID_VACA"), primary_key=True, index=False)
    Peso = Column(Integer)
    Fecha = Column(DateTime, nullable=True)
    previous_fecha = Column(DateTime, nullable=True)
    previous_peso = Column(Integer, nullable=True)
    dif_fecha = Column(Integer, nullable=True)
    dif_peso = Column(Integer, nullable=True)
    Peso_gain_by_day = Column(Float, nullable=True)

#servicios
class ServiciosT(Base):
    __tablename__ = "Servicios"
    IDservicio= Column(Integer, primary_key=True, index=True)
    ID_VACA = Column(Integer, ForeignKey("vacas.ID_VACA"))
    Sire = Column(Integer, ForeignKey("Sires.IDsire"), nullable=True)
    ID_Embrion = Column(Integer, nullable=True) #, ForeignKey("To be defined.ID_Embrion"))
    ID_ACTIVIDAD = Column(Integer, ForeignKey("Actividades_Vacas.ID_Actividad"))

#View de servicios sin diagnostico, para filtro rapido en App


#DiagPre
class DiagPreT(Base):
    __tablename__ = "DiagPre"
    IDdiagpre= Column(Integer, primary_key=True, index=True)
    ID_VACA = Column(Integer, ForeignKey("vacas.ID_VACA"))
    ID_Resultado = Column(Integer, ForeignKey("Actividades_vacas_resultado.ID_Resultado"))
    Dias = Column(Integer, nullable=True) #calculated between diagpre date and service date
    ID_servicio = Column(Integer, ForeignKey("Servicios.IDservicio"), nullable=True)
    ID_ACTIVIDAD = Column(Integer, ForeignKey("Actividades_Vacas.ID_Actividad"))
    
#Dificultad parto
class Dificultad_PartoT(Base):
    __tablename__ = "Dificultad_Parto"
    ID_dificultad= Column(Integer, primary_key=True, index=True)
    Dificultad = Column(String(45), nullable=True)

# View estatus Vacas
"""
class V_estatus_vacasT(Base):
    __tablename__ = "v_estatus_vacas"
    ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID_CLIENTE"))
    ID_VACA = Column(Integer, ForeignKey("vacas.ID_VACA"))
    Genero = Column(String(45), nullable=True)
    Edad_Years = Column(Float, nullable=True)
    Activa = Column(String(45), nullable=True)
    Ultimo_Peso_KG = Column(Float, nullable=True)
    Fecha_pesaje = Column(DateTime, nullable=True)
    Numero_Parto = Column(Integer, nullable=True)
    Fecha_ultimo_parto = Column(DateTime, nullable=True)
    Fecha_ultimo_servicio = Column(DateTime, nullable=True)
    Fecha_ultimo_diagpre = Column(DateTime, nullable=True)
    Diagpre_Resultado = Column(String(45), nullable=True)
    Fecha_ultimo_diagpre_5 = Column(DateTime, nullable=True)
    Diagpre5_Resultado = Column(String(45), nullable=True)
    Fecha_ultima_eco = Column(DateTime, nullable=True)
    Eco_Resultado = Column(String(45), nullable=True)
    Fecha_ultima_eco2 = Column(DateTime, nullable=True)
    Eco2_Resultado = Column(String(45), nullable=True)
    Fecha_ultimo_exrep = Column(DateTime, nullable=True)
    Exrep_Resultado = Column(String(45), nullable=True)
    Fecha_ultimo_presecado = Column(DateTime, nullable=True)
    Presecado_Resultado = Column(String(45), nullable=True)
    Fecha_ultimo_secado = Column(DateTime, nullable=True)
    Secado_Resultado = Column(String(45), nullable=True)
"""

#log_traslados_vacas_lotes
#parto_vaca_Full
#RangoFechas_Vacas
#vacas_mastitis
##########################################################################################################


#########################################    LECHE    #####################################################    
class Leche_HatosT(Base):
    __tablename__ = "Leche_Hatos"
    ID_Leche_hato = Column(Integer, primary_key=True, index=True)     #, ForeignKey("Actividades_Vacas.ID_Actividad")
    ID_HATO = Column(Integer, ForeignKey("Hatos.ID_HATO"))
    FECHA_ACTIVIDAD = Column(DateTime)
    ID_OPERARIO = Column(Integer, ForeignKey("Operario.ID_OPERARIO"), nullable=True)
    Comentario = Column(String(45), nullable=True)
    Numero_Animales = Column(Integer, nullable=True)
    Leche_Total = Column(Float, nullable=True)
    Hora = Column(String(2), nullable=True)
    Antibiotico = Column(String(45), nullable=True)
    Terneras = Column(String(45), nullable=True)

class Leche_VacaT(Base):
    __tablename__ = "Leche_Vaca"
    ID_Leche_vaca = Column(Integer, primary_key=True, index=True)    #, ForeignKey("Actividades_Vacas.ID_Actividad")
    ID_VACA = Column(Integer, ForeignKey("vacas.ID_VACA"))
    ID_OPERARIO = Column(Integer, ForeignKey("Operario.ID_OPERARIO"), nullable=True)
    Fecha_c = Column(DateTime)
    Leche_lts = Column(Float, nullable=True)
    #Ciclo_Lactancia = Column(Integer, nullable=True)    ## deberia ir en vaca
    #Numero_Partos = Column(Integer, nullable=True)      ##deberia ir en vaca

#Leche_Entregada
class Leche_EntregadaT(Base):
    __tablename__ = "Leche_Entregada"
    ID_Leche_Entregada = Column(Integer, primary_key=True, index=True)
    ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID_CLIENTE"), nullable=True)
    Fecha= Column(DateTime, nullable=True)
    Leche_entregada_lts = Column(Float, nullable=True)

#################################### TANQUE   ###############################################################
#Tanque_Finca
class Tanques_FincaT(Base):
    __tablename__ = "Tanques_Finca"
    ID_TANQUE = Column(Integer, primary_key=True, index=True)
    ID_Finca= Column(Integer, ForeignKey("Finca.ID_FINCA"), nullable=True)
    Capacidad_Max = Column(Float, nullable=True)
    Fecha_Creacion = Column(DateTime, nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)

#Tanque_hatos
class Tanques_HatosT(Base):
    __tablename__ = "Tanques_Hatos"
    ID_TANQUE_HATO = Column(Integer, primary_key=True, index=True)
    ID_TANQUE= Column(Integer, ForeignKey("Tanques_Finca.ID_TANQUE"), nullable=True)
    ID_HATO= Column(Integer, ForeignKey("Hatos.ID_HATO"), nullable=True)
    Fecha_Creacion = Column(DateTime, nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)
    
#Leche_tanque_Diaria
class Leche_Tanque_DiariaT(Base):
    __tablename__ = "Leche_Tanque_Diaria"
    ID = Column(Integer, primary_key=True, index=True)
    ID_TANQUE = Column(Integer, ForeignKey("Tanques_Finca.ID_TANQUE"), nullable=True)
    Fecha= Column(DateTime, nullable=True)
    Litros = Column(Float, nullable=True)

#Test_tanque
class Test_TanquesT(Base):
    __tablename__ = "Test_Tanques"
    ID = Column(Integer, primary_key=True, index=True)
    ID_TANQUE = Column(Integer, ForeignKey("Tanques_Finca.ID_TANQUE"), nullable=True)
    Fecha_Test= Column(DateTime, nullable=True)
    Proveedor = Column(String(45), nullable=True)
    Cod_seguimiento = Column(Integer, nullable=True)
    Tipo_Muestra = Column(String(45), nullable=True)
    Estado = Column(Integer, nullable=True)

#Resultado_Tanques
class Resultados_TanquesT(Base):
    __tablename__ = "Resultados_Tanques"
    ID = Column(Integer, primary_key=True, index=True)
    ID_TANQUE = Column(Integer, ForeignKey("Tanques_Finca.ID_TANQUE"), nullable=True)
    Fecha_recepcion= Column(DateTime, nullable=True)
    Fecha_resultado= Column(DateTime, nullable=True)
    Cod_seguimiento = Column(Integer, ForeignKey("Test_Tanques.Cod_seguimiento"), nullable=True)
    GRASA = Column(Float, nullable=True)
    PROTEINA = Column(Float, nullable=True)
    #RELACION_GP = Column(Float, nullable=True)
    SOLIDOS_TOTALES = Column(Float, nullable=True)
    LACTOSA = Column(Float, nullable=True)
    MUN = Column(Float, nullable=True)
    UFC = Column(Float, nullable=True)
    RCS = Column(Float, nullable=True)
    


##################################### PRODUCTOS   ##############################################3
#Actividades_Producto
#Map_clases_suministros
#Productos
#Proveedores
#Suministros
#Suministros_destino
#Suministros_origen
#Tipo_Suministros


##################################### COMUNICACION  ##############################################
#Contact_Comm
#Items_Communicacion
#Logicas_Comunicacion
#Pref_Client_Comm

##########################################################################################################

######################################### OTRAS FUENTES LOTES   #########################################
class Lotes_variablesT(Base):
    __tablename__ = "Lotes_variables"
    ID_lote= Column(Integer,  ForeignKey("lotes.ID_LOTE"), primary_key=True)
    fecha = Column(Date, nullable=True)
    Mean_BM= Column(Float, nullable=True)
    Mean_CP = Column(Float, nullable=True)
    Mean_NDF = Column(Float, nullable=True)
    Mean_LAI = Column(Float, nullable=True)
    Mean_NDVI = Column(Float, nullable=True)
    cld_percentage = Column(Float, nullable=True)
    area_factor = Column(Float, nullable=True)
    biomass_corrected = Column(Float, nullable=True)

class Lotes_quimicosT(Base):
    __tablename__ = "Lotes_quimicos"
    ID_registro= Column(Integer, primary_key=True)
    ID_lote= Column(Integer,  ForeignKey("lotes.ID_LOTE"))
    Fecha_muestra = Column(Date, nullable=True)
    ID_muestra = Column(Integer, nullable=True)
    Fecha_resultado = Column(Date, nullable=True)
    CE= Column(Float, nullable=True)
    PH = Column(Float, nullable=True)
    Nitrogeno = Column(Float, nullable=True)
    Fosforo = Column(Float, nullable=True)
    Potasio = Column(Float, nullable=True)
    Calcio = Column(Float, nullable=True)
    Magnesio = Column(Float, nullable=True)
    Sodio = Column(Float, nullable=True)
    Aluminio = Column(Float, nullable=True)
    Azufre = Column(Float, nullable=True)
    Cloro = Column(Float, nullable=True)
    Hierro = Column(Float, nullable=True)
    Manganeso = Column(Float, nullable=True)
    Cobre = Column(Float, nullable=True)
    Zinc = Column(Float, nullable=True)
    Boro = Column(Float, nullable=True)
    Comentarios = Column(String(450), nullable=True)

#Test_Bromatologico
#crecimiento_lotes_meteo
#rangocrecimiento_lotes


###########################################################################################################

##########################################  Monitoreo procesamiento imagenes satel   ######################
class monitoreo_descargas_sentinelT(Base):
    __tablename__ = "monitoreo_descargas_sentinel"
    zona= Column(String(45), primary_key=True)
    file = Column(String(45))
    fecha  = Column(Date)
    process_date = Column(DateTime)

#Indices_remote_sense
#monitoreo_imagenes_proces
#Zonas_sentinel
###########################################################################################################

########################################   ESTACION METEOROLOGICA   #######################################
class MeteorologiaT(Base):
    __tablename__ = "Meteorologia"
    ID_Estacion = Column(Integer, ForeignKey("Estaciones_Meteo.ID_Estacion"), primary_key=True) #
    #ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID_CLIENTE"), primary_key=True)
    FECHA_HORA = Column(Date, primary_key=True, index=True)
    activacion = Column(Integer, nullable=True)
    DHT_Humidity_mean = Column(Float, nullable=True)
    DHT_Humidity_max = Column(Float, nullable=True)
    DHT_Humidity_min = Column(Float, nullable=True)
    DHT_Humidity_std = Column(Float, nullable=True)
    DHT_Temp_mean = Column(Float, nullable=True)
    DHT_Temp_max = Column(Float, nullable=True)
    DHT_Temp_min = Column(Float, nullable=True)
    Hum_Gnd_mean = Column(Float, nullable=True)
    Rain_mm_sum = Column(Float, nullable=True)
    Thermo_Couple_mean = Column(Float, nullable=True)
    Thermo_Couple_max = Column(Float, nullable=True)
    Thermo_Couple_min = Column(Float, nullable=True)
    Wind_Dir_Moda = Column(String(12), nullable=True)
    Wind_Speed_mean = Column(Float, nullable=True)
    Wind_Speed_max = Column(Float, nullable=True)
    DS18b20_cap_mean = Column(Float, nullable=True)
    DS18b20_cap_max = Column(Float, nullable=True)
    DS18b20_cap_min = Column(Float, nullable=True)
    Solar_Volt_mean = Column(Float, nullable=True)
    Solar_Volt_max = Column(Float, nullable=True)
    Solar_Volt_min = Column(Float, nullable=True)
    Solar_Volt_std = Column(Float, nullable=True)
    Sunlight_mean = Column(Float, nullable=True)
    Sunlight_max = Column(Float, nullable=True)
    Sunlight_min = Column(Float, nullable=True)
    Sunlight_std = Column(Float, nullable=True)
    Count_Report = Column(Integer, nullable=True)

class EstacionesT(Base):
    __tablename__ = "Estaciones_Meteo"
    ID_Estacion = Column(Integer, primary_key=True) #ForeignKey("Finca.ID_FINCA"),
    ID_Finca = Column(Integer, ForeignKey("Finca.ID_FINCA"))
    comentarios = Column(String(45))
    Fecha_instalacion = Column(DateTime, nullable=True)
    deshabilitado = Column(Integer, nullable=True)
    Fecha_deshabilitado = Column(DateTime, nullable=True)
    
class Meteo_iot(Base):
    __tablename__ = "Meteo_iot"
    ID_Estacion = Column(Integer, ForeignKey("Estaciones_Meteo.ID_Estacion"), primary_key=True) 
    Date_Time = Column(DateTime, primary_key=True, index=True)
    DHT_Humidity = Column(Float, nullable=True)
    DHT_Temp = Column(Float, nullable=True)
    DS18b20_cap = Column(Float, nullable=True)
    Hum_Gnd = Column(Float, nullable=True)
    Rain_mm = Column(Float, nullable=True)
    Solar_Volt = Column(Float, nullable=True)
    Sunlight = Column(Float, nullable=True)
    Thermo_Couple = Column(Float, nullable=True)
    Wind_Dir = Column(String(45), nullable=True)
    Wind_Speed = Column(Float, nullable=True)
###########################################################################################################

class celoT(Base):
    __tablename__ = "celo"
    id_celo = Column(Integer, primary_key=True, index=True)
    tag = Column(String(45), ForeignKey("vacas.ElectronicID"))
    sensor = Column(String(45), nullable=True) #, ForeignKey("celotron_tags.TAG_NAME"))
    battery = Column(Float, nullable=True)
    #fecha_envio = Column(DateTime, nullable=True)
    fecha_recibido = Column(DateTime, nullable=True)
    numero_envio = Column(String(32), nullable=True)
    numero_recibido = Column(String(32), nullable=True)
    #direccion = Column(String(32), nullable=True)
    segmentos = Column(Integer, nullable=True)
    #status = Column(String(32), nullable=True)
    #costo = Column(Float, nullable=True)
    fecha_celo = Column(DateTime, nullable=True)


class celo_gsmT(Base):
    __tablename__ = "celo_gsm"
    id_celo_gsm = Column(Integer, primary_key=True, index=True)
    tag = Column(String(45)) #, ForeignKey("celotron_tags.TAG_NAME"))
    date = Column(DateTime, nullable=True)
    sensor = Column(Integer, nullable=True)
    battery = Column(Float, nullable=True)
    duration = Column(Integer, nullable=True)


class pref_sms_contactT(Base):
    __tablename__ = 'Pref_SMS_contact'
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.ID_CLIENTE"), nullable=True)
    id_finca = Column(Integer, ForeignKey("Finca.ID_FINCA"), nullable=True)
    numero = Column(String(45), nullable=True)
    nombre = Column(String(45), nullable=True)
    status = Column(String(45), nullable=True)


