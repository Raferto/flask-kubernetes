import requests

BASE_URL='http://localhost:32000'

def lihat_isi_phonebook():
    uri = BASE_URL + '/phones'
    r = requests.get(uri)
    code = r.status_code
    if (code==200):
        hasil = r.json()
        return hasil
    else:
        return None

def isi_data_phonebook(nama='',alamat='',telp=''):
    uri = BASE_URL + '/phones'
    headers={'content-type' : 'application/json'}
    r = requests.post(uri,data=dict(nama=nama,alamat=alamat,telp=telp),headers=headers)
    code = r.status_code
    if (code==200):
        hasil = r.json()
        return hasil
    else:
        return None

if __name__=='__main__':
    #lihat isi phonebook
    print(lihat_isi_phonebook())
    print(isi_data_phonebook(nama='Royyana',alamat='Ketintang',telp='123142'))
    print(lihat_isi_phonebook())

