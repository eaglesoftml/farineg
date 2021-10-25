#-*- coding: utf-8 -*-

import random
import hashlib
import base64
from io import BytesIO
from os import urandom
from Crypto.Cipher import AES
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import qrcode
from datetime import datetime
import cv2
import pandas as pd



class etiquette(models.Model):
    _name = "farinegmm.etiquette"
    _description = "farinegmm.etiquette"

    ref = fields.Char("reference", compute="generate_qr_code",default="New")
    refseq = fields.Char("reference",default="New")
    produit = fields.Char(default="Farine GMM")
    etat = fields.Selection([('brl','Brouillon'),('enrg','Enregistré'),('atbclt','Attribué'),('utl','Utilisé'),('vld','Validé'),('anl','Annulé')],default="brl")
    renumere = fields.Boolean("Renumeré", required="True")
    # next = fields.Integer(compute="_radom")
    datedebut = fields.Date("Date debut", compute="_date")
    datelimite = fields.Date("Date limite", compute="_date")
    client_id = fields.Many2one("res.partner", string="client id")

    qr_code = fields.Binary("QR Code", attachment=True, store=True)

    test = fields.Char("source qrcode", compute="generate_qr_code")

    # @api.onchange('ref')
    # def _random(self):
    #     for line in self:
    #         line.ref = "etq_000"+str(random.randint(1, 1000000))
    #         secret_key = urandom(16)
    #         # data = pd.read_csv(filename, encoding='unicode_escape')
    #         iv = urandom(16)
    #         obj = AES.new(secret_key, AES.MODE_CBC, iv)
    #         message = line.ref
    #         # ref_crypt = obj.encrypt(message*16)
    #         # line.ref = ref_crypt
    #         line.ref = base64.b64encode(obj.encrypt(message*16))
    #     return line.ref

    @api.onchange('ref')
    def generate_qr_code(self):
        for line in self:
            # if line.ref == "":
            line.ref = "etq_" + str(random.randint(1, 1000000000))
            secret_key = urandom(16)
            # data = pd.read_csv(filename, encoding='unicode_escape')
            iv = urandom(16)
            obj = AES.new(secret_key, AES.MODE_CBC, iv)
            message = line.ref
            # ref_crypt = obj.encrypt(message*16)
            # line.ref = ref_crypt
            ref_crypt = obj.encrypt(message*16)
            line.ref = base64.b64encode(ref_crypt)

            rev_obj = AES.new(secret_key, AES.MODE_CBC, iv)
            ref_decrypt = rev_obj.decrypt(ref_crypt)
            line.test = ref_decrypt.decode('latin-1')
            # line.test = base64.b64decode(ref_decrypt.decode(encoding='utf-8'))
            # line.test = pd.read_csv(ref_decrypt, encoding='unicode_escape')

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(line.ref)
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            line.qr_code = qr_image


    @api.model
    def create(self, values):
        res = super(etiquette, self).create(values)
        res.write({refseq: f'{res.id}'})
        return res

    @api.model
    def create(self, values):
        values['refseq'] = self.env['ir.sequence'].next_by_code('seq.etiquette.refseq') or _('New')
        return super(etiquette, self).create(values)


    def next_level(self):
        for line in self:
            if line.etat == 'brl':
                return line.write({'etat':'enrg'})
            elif line.etat == 'enrg':
                return line.write({'etat':'atbclt'})
            elif line.etat == 'atbclt':
                return line.write({'etat':'utl'})
            elif line.etat == 'utl':
                return line.write({'etat': 'vld'})
            elif line.etat == 'vld':
                return line.write({'etat': 'anl'})
            else:
                raise ValidationError("Impossible d'aller de l'avant")

    def previous_level(self):
        for line in self:
            line.ensure_one()
            if line.etat == "anl":
                return line.write({'etat': 'vld'})
            elif line.etat == 'vld':
                return line.write({'etat':'utl'})
            if line.etat == 'utl':
                return line.write({'etat': 'atbclt'})
            elif line.etat == 'atbclt':
                return line.write({'etat':'enrg'})
            elif line.etat == 'enrg':
                return line.write({'etat':'brl'})
            else:
                raise ValidationError("C'est la toute première étape")

    def annuler(self):
        for line in self:
            return line.write({'etat': 'anl'})


    def _date(self):
        for line in self:
            line.ensure_one()
            line.datedebut = datetime.strptime('07/28/2022', '%m/%d/%Y')
            line.datelimite = datetime.strptime('07/28/2023', '%m/%d/%Y')


    # def lecteur_qrcode(self):
    #     img = cv2.imread(self.qr_code)
    #     det = cv2.QRCodeDetector()
    #     test = det.detectAndDecode(img)

