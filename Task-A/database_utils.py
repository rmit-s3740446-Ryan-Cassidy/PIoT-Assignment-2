import MySQLdb

class DatabaseUtils:
    HOST = "35.244.74.229"
    USER = "root"
    PASSWORD = "abc123"
    DATABASE = "CarBookingApp"

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(DatabaseUtils.HOST, DatabaseUtils.USER,
                DatabaseUtils.PASSWORD, DatabaseUtils.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def createTables(self):
        with self.connection.cursor() as cursor:
            cursor.execute("drop table if exists Car")
            cursor.execute("""
            create table if not exists Car (
                CarID int not null auto_increment,
                Make text not null,
                Type text  null,
                Location text  null,
                Color text  null,
                Seats text  null,
                CostPerHour text  null,
                constraint PK_Car primary key (CarID)
                )""")
            cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour) values ('Honda','Sedan','3073','Red','6','20')")
            cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour) values ('Civic','Sedan','3073','Red','6','20')")
        self.connection.commit()
