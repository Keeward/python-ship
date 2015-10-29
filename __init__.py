#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from config import UPSConfig
except:
    print 'HELLO THERE! test_config not found. If you want to run this test, you need to setup test_config.py with your account information.'
    raise

import os, tempfile
from shipping import Package, Address, Product

import ups
import fedex

class ReportGenerator():
    __all__ = [ 'UPS', 'USPS', 'endicia', 'common' ]

    def save_file(self,filename, extension, data):
        filepath =  filename
        file = open(filepath, "w")
        file.write(data)
        file.close()
        return filename

    def show_file(self,extension, data):
        with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as temp_file:
            temp_file.write(data)
            os.system('open %s' % temp_file.name)

    class P(object):
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    def generarte_UPS_report(self, path, shipper_from_name,shipper_from_address,
     shipper_from_city, shipper_from_state, shipper_from_zipcode,
     shipper_from_countrycode,shipper_from_phone,ship_from_name,
     ship_from_address, ship_from_city, ship_from_state,
     ship_from_zipcode, ship_from_countrycode,ship_from_phone,
     ship_to_name,ship_to_address,ship_to_address2, ship_to_city,
     ship_to_state, ship_to_zipcode, ship_to_countrycode,ship_to_phone,
     shipment_weight,USPSEndorsement='', costCenter='', packageID=''):

        print 'params for the generate UPS report function:'
        print shipper_from_name,shipper_from_address, shipper_from_city, shipper_from_state, shipper_from_zipcode, shipper_from_countrycode,shipper_from_phone,ship_from_name,ship_from_address, ship_from_city, ship_from_state, ship_from_zipcode, ship_from_countrycode,ship_from_phone,ship_to_name,ship_to_address,ship_to_address2, ship_to_city, ship_to_state, ship_to_zipcode, ship_to_countrycode,ship_to_phone,shipment_weight

        shipper = Address(shipper_from_name, shipper_from_address, shipper_from_city, shipper_from_state, shipper_from_zipcode, shipper_from_countrycode, phone=shipper_from_phone, email='')
        ship_from = Address(ship_from_name, ship_from_address, ship_from_city, ship_from_state, ship_from_zipcode, ship_from_countrycode, phone=ship_from_phone, email='')
        recipient = Address(ship_to_name, ship_to_address, ship_to_city, ship_to_state, ship_to_zipcode, ship_to_countrycode, address2=ship_to_address2, phone=ship_to_phone, email='')

        print 'shipmentweight is '
        print shipment_weight

        shipmentweight = shipment_weight *  2.20462262185
        package = Package(shipmentweight, 12, 12, 12, require_signature=4)
        packages = [ package ]

        debug = TRUE #app.config['DEBUG']
        print 'debug is '
        print debug
        u = ups.UPS(UPSConfig, debug=debug)

        validate = False
        try:
            response = u.label(packages, shipper, ship_from, recipient, ups.SERVICES[13][0], ups.PACKAGES[8][0], validate, [], create_commercial_invoice=False, customs_info=[],USPSEndorsement=USPSEndorsement, costCenter=costCenter, packageID=packageID)
            status = response['status']
            print 'Status: %s' % status,
            for info in response['shipments']:
                print 'tracking: %s' % (info['tracking_number'])
                tracking_number = info['tracking_number']
                createdFile = self.save_file(filename=path, extension='.gif', data=info['label'])
                print 'created the UPS image at ' + createdFile
                return tracking_number
        except ups.UPSError as e:
            print e

    if __name__ == '__main__':
        print 'this is __main__'
