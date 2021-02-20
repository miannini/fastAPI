# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 19:18:16 2020

@author: Marcelo
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float#, Date
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date
from .database import Base

'''
When accessing the attribute items in a User, as in my_user.items, it will have a list of Item SQLAlchemy models (from the items table) that have a foreign key pointing to this record in the users table.

When you access my_user.items, SQLAlchemy will actually go and fetch the items from the database in the items table and populate them here.

And when accessing the attribute owner in an Item, it will contain a User SQLAlchemy model from the users table. It will use the owner_id attribute/column with its foreign key to know which record to get from the users table.

'''

class ClientesT(Base):
    __tablename__ = "clientes" #nombre de la tabla de la DB
    ID_CLIENTE = Column(Integer, primary_key=True, index=True) #
    NOMBRE = Column(String(32), unique=True, nullable=True) #definicion de cada columna, con tipo
    NIT_CC = Column(Integer, nullable=True)
    RAZON_SOCIAL = Column(String(32), nullable=True)
    TELEFONO = Column(Integer, nullable=True)
    EMAIL = Column(String(32), nullable=True)
    DIRECCION = Column(String(32), nullable=True)
    CIUDAD = Column(String(32), nullable=True)
    DEPARTAMENTO = Column(String(32), nullable=True)
    DESCRIPCION = Column(String(32), nullable=True)
    FECHA_CONTRATO = Column(Date, nullable=True)
    #Vencimiento_contrato, activo, categoria(oro,plata,etc)
    #is_active = Column(Boolean, default=True)

    #operarios = relationship("OperarioT", back_populates="owner_CLIENTE") #the magic

class OperarioT(Base):
    __tablename__ = "Operario"
    ID_OPERARIO = Column(Integer, primary_key=True, index=True)
    ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID_CLIENTE"))
    ID_FINCA = Column(Integer, ForeignKey("Finca.ID_FINCA"))
    NombreOperario = Column(String(32))
    FechaDeIngreso = Column(Date, nullable=True)
    Telefono = Column(Integer, nullable=True)
    Rol = Column(String(140), nullable=True)
    Descripcion = Column(String(140), nullable=True)
    Email = Column(String(32), nullable=True)
    Direccion = Column(String(32), nullable=True)
    #owner_CLIENTE = relationship("ClientesT", back_populates="operarios")


class FincaT(Base):
    __tablename__ = "Finca"
    ID_FINCA = Column(Integer, primary_key=True, index=True)
    NOMBRE = Column(String(32), nullable=True)
    DESCRIPCION = Column(String(134), nullable=True)
    lotes_list = relationship("LotesT", back_populates="finca_madre")
    

class LotesT(Base):
    __tablename__ = "lotes"
    ID_LOTE = Column(Integer, primary_key=True, index=True)
    ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID_CLIENTE"))
    ID_FINCA = Column(Integer, ForeignKey("Finca.ID_FINCA"))
    NOMBRE_LOTE = Column(String(32))
    LATITUD = Column(Float, nullable=True)
    LONGITUD = Column(Float, nullable=True)
    AREA = Column(Float, nullable=True)
    DESCRIPCION = Column(String(45), nullable=True)
    finca_madre = relationship("FincaT", back_populates="lotes_list")
    
class HatosT(Base):
    __tablename__ = "Hatos"
    ID_HATO = Column(Integer, primary_key=True, index=True)
    ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID_CLIENTE"))
    ID_FINCA = Column(Integer, ForeignKey("Finca.ID_FINCA"))
    Nombre_Hato = Column(String(45), nullable=True)
    TIPO_Hato = Column(String(32), nullable=True)
    Descripcion = Column(String(32), nullable=True)
    
class Leche_HatosT(Base):
    __tablename__ = "Leche_Hatos"
    ID_Leche_hato = Column(Integer, primary_key=True, index=True)     #, ForeignKey("Actividades_Vacas.ID_Actividad")
    ID_HATO = Column(Integer, ForeignKey("Hatos.ID_HATO"))
    FECHA_ACTIVIDAD = Column(Date)
    ID_OPERARIO = Column(Integer, ForeignKey("Operario.ID_OPERARIO"), nullable=True)
    Comentario = Column(String(45), nullable=True)
    Numero_Animales = Column(Integer, nullable=True)
    Leche_Total = Column(Float, nullable=True)
    Hora = Column(String(2), nullable=True)
    Antibiotico = Column(String(45), nullable=True)
    Terneras = Column(String(45), nullable=True)

    
class VacasT(Base):
    __tablename__ = "vacas"
    ID_VACA = Column(Integer, primary_key=True, index=True)
    ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID_CLIENTE"))
    ID_FINCA = Column(Integer, ForeignKey("Finca.ID_FINCA"))
    ElectronicID = Column(String(32), nullable=True)
    Nombre_Vaca = Column(String(32))
    Raza = Column(String(32), nullable=True)
    Sexo = Column(Integer, nullable=True)
    VacaMadre = Column(Integer, nullable=True)
    IDparto = Column(Integer, nullable=True)
    FechaRegistro = Column(Date, nullable=True)
    IDTipoOrigen = Column(Integer, nullable=True)
    FechaNacimiento = Column(Date, nullable=True)
    IDTipoSalida = Column(Integer, nullable=True)
    FechaSalida = Column(Date, nullable=True)
    #FECHA_NACIMIENTO = Column(Date, nullable=True)
    Sire = Column(Integer, nullable=True)
    Estado = Column(Integer, nullable=True)
    Estado_Final = Column(Integer, nullable=True)
  
    
class Leche_VacaT(Base):
    __tablename__ = "Leche_Vaca"
    ID_Leche_vaca = Column(Integer, primary_key=True, index=True)    #, ForeignKey("Actividades_Vacas.ID_Actividad")
    ID_VACA = Column(Integer, ForeignKey("vacas.ID_VACA"))
    ID_OPERARIO = Column(Integer, ForeignKey("Operario.ID_OPERARIO"), nullable=True)
    FECHA = Column(Date)
    Litros = Column(Float, nullable=True)
    Ciclo_Lactancia = Column(Integer, nullable=True)    ## deberia ir en vaca
    Numero_Partos = Column(Integer, nullable=True)      ##deberia ir en vaca
    

class MeteorologiaT(Base):
    __tablename__ = "Meteorologia"
    ID_FINCA = Column(Integer, ForeignKey("Finca.ID_FINCA"), primary_key=True)
    ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID_CLIENTE"), primary_key=True)
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


class API_UsersT(Base):
    __tablename__ = "API_Users"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(45))
    full_name = Column(String(45)) #, ForeignKey("Operario.NombreOperario"))
    email = Column(String(45))
    password = Column(String(99))
    active_status = Column(Integer, nullable=True)
    id_user_rol = Column(Integer, nullable=True)
    ID_CLIENTE = Column(Integer, ForeignKey("clientes.ID_CLIENTE"), nullable=True)
    ID_OPERARIO = Column(Integer, ForeignKey("Operario.ID_OPERARIO"), nullable=True)


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
  

class ActividadesVacasT(Base):
    __tablename__ = "Actividades_Vacas"
    ID_Actividad = Column(Integer, primary_key=True, index=True)
    ID_VACA = Column(Integer, ForeignKey("vacas.ID_VACA"))
    ID_TipoOperacion = Column(Integer) #, ForeignKey
    ID_Resultado = Column(Integer) #, ForeignKey
    ID_OPERARIO = Column(Integer, ForeignKey("Operario.ID_OPERARIO"))
    ID_Categoria = Column(Integer) #, ForeignKey
    Fecha = Column(Date, nullable=True)
    Comentario = Column(String(450), nullable=True)
    
    
class Ubicacion_VacasT(Base):
    __tablename__ = "Ubicacion_Vacas"
    ID_VACA = Column(Integer, ForeignKey("vacas.ID_VACA"), primary_key=True, index=True)
    ID_HATO = Column(Integer, ForeignKey("Hatos.ID_HATO"), primary_key=True, index=True)
    ID_LOTE = Column(Integer, ForeignKey("lotes.ID_LOTE"), primary_key=True, index=True)