"""
Basic functions for VAT number validation via VIES
Most important function is vatol. It connects to the server
and if success returns something like:
(reply){
   countryCode = "EL"
   vatNumber = "123456789"
   requestDate = 2017-03-10
   valid = True
   name = "name1||name2"
   address = "odos arithmos 26500 - perioxi poli"
}
"""
import re
from suds.client import Client  # To setup run : sudo pip install suds-jurko

URL = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'


def isvat(a):
    '''
    Αλγοριθμικός έλεγχος Ελληνικού ΑΦΜ
    '''
    if len(a) != 9:
        return False
    b = int(a[0]) * 256 + int(a[1]) * 128 + int(a[2]) * 64 + int(a[3]) * 32 + \
        int(a[4]) * 16 + int(a[5]) * 8 + int(a[6]) * 4 + int(a[7]) * 2
    c = b % 11
    d = c % 10
    return d == int(a[8])


def vatol(afm, country_code='EL'):
    '''
    VAT Check online using SOAP client
    returns dictionary with:
    countryCode, vatNumber, requestDate, valid, name, address
    '''
    result = {'valid': False}
    try:
        client = Client(URL, timeout=10)
        result = client.service.checkVat(country_code, afm)
    except:
        result['conError'] = True
    return result


def get_vat(afm):
    final = {}
    if not isvat(afm):
        final['ok'] = False
        final['msg'] = 'Ο Α.Φ.Μ. : %s είναι λανθασμένος.' % afm
        return final
    vat = vatol(afm)

    if 'conError' in vat:
        final['ok'] = False
        final['msg'] = ('Ο έλεγχος Α.Φ.Μ. δεν λειτουργεί.\n'
                        'Παρακαλώ δοκιμάστε αργότερα')
        return final

    if vat['valid']:
        if '||' in vat['name']:
            name, name2 = vat['name'].split('||')
        else:
            name, name2 = vat['name'], ''
        name = name.strip()
        name2 = name2.strip()
        if len(name) > len(name2):
            if len(name2) > 1:
                name, name2 = name2, name
        patterntk = r' \d\d\d\d\d '  # 5 digits with space before and after
        ftk = re.search(patterntk, vat['address'])
        if ftk:
            tk = ftk.group().strip()
            ad1 = vat['address'][:ftk.start()].strip()
            ad2 = vat['address'][ftk.end():].replace('-', '').strip()
        else:
            ad1 = vat['address']
            tk = ''
            ad2 = ''
        final['requestDate'] = vat['requestDate']
        final['name'] = name
        final['name2'] = name2
        final['aff'] = vat['vatNumber']
        final['ad1'] = ad1
        final['ad2'] = ad2
        final['tk'] = tk
        final['ok'] = True
        final['msg'] = 'Ο Α.Φ.Μ. είναι έγκυρος'
    else:
        final['ok'] = False
        final['msg'] = 'Ο Α.Φ.Μ. : %s δεν είναι έγκυρος.' % afm
    return final


def print_vat(afm):
    gvat = get_vat(afm)
    if gvat['ok']:
        print('Ημερομηνία : %s' % gvat['requestDate'])
        print('Όνομα      : %s' % gvat['name'])
        print('Όνομα2     : %s' % gvat['name2'])
        print('ΑΦΜ        : %s' % gvat['aff'])
        print('Διεύθυνση1 : %s' % gvat['ad1'])
        print('Διεύθυνση2 : %s' % gvat['ad2'])
        print('T.K.       : %s' % gvat['tk'])
    else:
        print(gvat['msg'])


if __name__ == '__main__':
    print_vat('094248423')
