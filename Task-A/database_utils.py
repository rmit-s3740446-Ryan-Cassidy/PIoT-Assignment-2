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
        """
        Closes the database connection. 
        """
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def createTables(self):
        """
        Create database tables if tables do not exists
        """
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
                credentials json,
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
            # location = '{"location": {"lat": -37.810021, "lng": 144.963001}, "accuracy": 2312}'
            # locationOne = '{"location": {"lat": -37.808016, "lng": 144.960125}, "accuracy": 2312}'
            # locationTwo = '{"location": {"lat": -37.798249, "lng": 144.953120}, "accuracy": 2312}'
            # locationThree = '{"location": {"lat": -37.803272, "lng": 144.951275}, "accuracy": 2312}'
            # locationFour = '{"location": {"lat": -37.799966, "lng": 144.957605}, "accuracy": 2312}'
            # locationFive = '{"location": {"lat": -37.793078, "lng": 144.976059}, "accuracy": 2312}'
            # locationSix = '{"location": {"lat": -37.817555, "lng": 144.989964}, "accuracy": 2312}'
            # locationSeven = '{"location": {"lat": -37.819449, "lng": 144.960224}, "accuracy": 2312}'
            # locationEight = '{"location": {"lat": -37.832392, "lng": 144.937795}, "accuracy": 2312}'
            # locationNine = '{"location": {"lat": -37.826083, "lng": 144.892047}, "accuracy": 2312}'
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Honda','Sedan','"+location+"','Blue','7','20','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Alto','Sedan','"+locationOne+"','Red','8','10','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Honda','Sedan','"+locationTwo+"','Red','9','20','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Civic','Sedan','"+locationThree+"','Black','6','20','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Honda','Sedan','"+locationFour+"','Red','7','20','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Mercedes','Sedan','"+locationFive+"','Blue','8','10','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Honda','Sedan','"+locationSix+"','Red','9','10','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Civic','Sedan','"+locationSeven+"','Black','6','10','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Mercedes','Sedan','"+locationEight+"','Red','7','20','Available')")
            # cursor.execute("insert into Car (Make,Type,Location,Color,Seats,CostPerHour,Status) values ('Alto','Sedan','"+locationNine+"','Blue','6','10','Available')")
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