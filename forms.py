from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from wtforms import validators,SubmitField, SelectField, IntegerField

#########################
###### CLASES ###########
#########################

prod = ['CASH OUT',  'TOP UP', 'DEBIT CARD', 'CASH IN', 'WELLFARE', 'BONO', 'P2P', 'CB', 'AJUSTE', 'INCOMM', 'PAGO EN COMERCIO', 'TARJETA', 'PAGO PRESTI', 'CRIPTO MONEDA', 'PRESTI', 'MERCHPAY', 'COMISION', 'GIRO F', 'SEGURO', 'REMESAS INTERNACIONALES', 'IVA']
subprod = ['TRANSFIYA',  'TOP UP', 'TARJETA', 'BALOTO', 'EXITO', 'MOVIIRED', 'PSE', 'MAYOR OFFICE', 'ACH', 'MEGARED', 'GOVERNMENT', 'BONIFICACION', 'FAMILIAS', 'CASH OUT', 'P2P', 'SUPERPAGOS', 'PRACTISISTEMAS', 'PAGO CONVENIO', 'AJUSTE', 'APUESTAS DEPORTIVAS', 'MULTIPAGAS', 'SERVIBANCA', 'BEMOVIL', 'MONEY TRANSFER', 'MOVILSERVICIOS', 'LA REBAJA', 'COMPRAS CONTENIDO', 'NETFLIX', 'COMERCIALCARD', 'DISBURSEMENT', 'GAS', '4XMIL', 'PILA', 'INCOMM', 'PRESTI', 'CATERING', 'CODENSA', 'NOMINA', 'VILLAS', 'HABITAT', 'MAFEPHONE', 'BITPOINT', 'COMISION', 'ADULTO MAYOR', 'ENVIO', 'SOAT', 'REMITEE', 'REVERSO ENVIO GIRO INTERNACIONAL', 'PAGO EN COMERCIO', 'FUNDACION', 'DEBIT CARD', 'TERRAPAY', 'BALOTO ENVIO', 'GIRO F', 'VANILLA', 'BARRAS Y RECAUDOS']

class InfoForm(FlaskForm):
    startdate = DateField('Start date', format = '%Y-%m-%d', validators=(validators.DataRequired(),))
    enddate = DateField('End date', format = '%Y-%m-%d', validators=(validators.DataRequired(),))
    producto = SelectField("producto", choices=prod,validators=(validators.DataRequired(),))
    user = IntegerField('usr')
    submit = SubmitField('Submit')

class DataStore():
    ini = None
    fin = None
    pro = None
    ids = None