import MySQLdb


class DatabaseUtils:
    HOST = "35.244.74.229"
    USER = "root"
    PASSWORD = "abc123"
    DATABASE = "CarBookingApp"

    def __init__(self, connection=None):
        if connection == None:
            connection = MySQLdb.connect(
                DatabaseUtils.HOST,
                DatabaseUtils.USER,
                DatabaseUtils.PASSWORD,
                DatabaseUtils.DATABASE,
            )
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def createTables(self):
        with self.connection.cursor() as cursor:
            # cursor.execute("drop table if exists Car")
            # cursor.execute("drop table if exists User")
            # cursor.execute("drop table if exists Login")
            cursor.execute(
                """
            create table if not exists Car (
                CarID int not null auto_increment,
                Make text not null,
                Type text not null,
                Location text not null,
                Color text  null,
                Seats text  null,
                CostPerHour text  null,
                Status text not null,
                constraint PK_Car primary key (CarID)
                )"""
            )
            cursor.execute(
                """
            create table if not exists User (
                UserID int not null auto_increment,
                FirstName text not null,
                LastName text not  null,
                UserName text(20) not  null,
                Email text not  null,
                Role text not  null,
                constraint PK_Car primary key (UserID)
                )"""
            )
            cursor.execute(
                """
            create table if not exists Login (
                LoginID int not null auto_increment,
                UserName text(20) not null,
                Password text not  null,
                constraint PK_Car primary key (LoginID)
                )"""
            )
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Honda','Sedan','3073','Red','6','10','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Honda','Sedan','3074','Blue','7','10','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Civic','Sedan','3075','Red','6','10','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Civic','Sedan','3076','Blue','7','20','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Honda','Sedan','3077','Red','6','20','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Honda','Sedan','3076','Blue','7','20','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Civic','Sedan','3073','Red','6','20','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Civic','Sedan','3073','Blue','7','20','Available')")
            # cursor.execute("drop table if exists Booking")
            cursor.execute(
                """
            create table if not exists Booking (
                BookingID int not null auto_increment,
                PickUpDate date not null,
                PickUpTime time not null,
                ReturnDate date not null,
                ReturnTime time not null,
                CarID int not null,
                UserName text not null,
                constraint PK_Car primary key (BookingID)
                )"""
            )
            # cursor.execute("insert into User (FirstName,LastName,UserName,Email,Role) values ('Vineet','Bugtani','s3734938','vineet.bugtani@gmail.com','Customer')")
        self.connection.commit()
