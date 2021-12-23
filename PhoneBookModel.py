import uuid
import os
import pymysql

class PhoneBook:
    def __init__(self):
        self.db = pymysql.connect(
            host='34.67.9.205',
            user='root',
            password='admin123',
            db='phonebookdb',
            port=3306,
        )
        self.cur = self.db.cursor()
        
    def list(self):
        data = []
        try:
            self.cur.execute("select * from phonebook")
            data = self.cur.fetchall()
            return dict(status='OK',data=data)
        except:
            return dict(status='ERR',msg='Error')

    def create(self,info):
        try:
            id = str(uuid.uuid1())
            sql = "INSERT INTO `phonebook` (`id`, `nama`, `alamat`, `notelp`) VALUES (%s, %s, %s, %s)"
            self.cur.execute(sql, (id, info['nama'], info['alamat'], info['notelp']))
            self.db.commit()

            return dict(status='OK',id=id)
        except:
            return dict(status='ERR',msg='Tidak bisa Create')

    def delete(self,id):
        try:
            sql = "DELETE FROM `phonebook` WHERE id = %s"
            self.cur.execute(sql, (id))
            self.db.commit()
            
            return dict(status='OK',msg='{} deleted' . format(id), id=id)
        except:
            return dict(status='ERR',msg='Tidak bisa Delete')

    def update(self,id,info):
        update_col = ""

        for column in info:
            update_col +=  column + " = '" + info[column] + "', "
        update_col = update_col[:-2]

        try:
            sql = "UPDATE `phonebook` SET {} WHERE id = %s".format(update_col)
            self.cur.execute(sql, id)
            self.db.commit()

            return dict(status='OK',msg='{} updated' . format(id), id=id)
        except:
            return dict(status='ERR',msg='Tidak bisa Update')
            
    def read(self,id):
        try:
            sql = "select * from phonebook WHERE id = %s"
            self.cur.execute(sql, id)
            data = self.cur.fetchone()
            
            return dict(status='OK',id=id,data=data)
        except:
            return dict(status='ERR',msg='Tidak Ketemu')

    def measure(self):
        
        sql = "SELECT SUM(data_length + index_length) / 1024 / 1024 AS 'Size (MB)' FROM information_schema.TABLES WHERE table_schema='phonebook'"
        self.cur.execute(sql)
        data_memory = self.cur.fetchone()

        sql = "SELECT COUNT(*) FROM phonebook"
        self.cur.execute(sql)
        data_record = self.cur.fetchone()
        
        return dict(status="OK",data=dict(size=data_memory,record=data_record))



if __name__=='__main__':
    pd = PhoneBook()
    print(pd.list())
    print(pd.measure())
