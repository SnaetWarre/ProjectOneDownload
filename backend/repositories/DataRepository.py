from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.method != 'GET' and request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    


    @staticmethod
    def insert_values_history(DeviceID, ActionID, SessionID, Value, Comments):
        sql = "INSERT INTO History (DeviceID, ActionID, SessionID, ActionDate, Value, Comments) VALUES (%s, %s, %s, NOW(), %s, %s)"
        params = [DeviceID, ActionID, SessionID, Value, Comments]
        return Database.execute_sql(sql, params) 

    @staticmethod
    def read_values_bpm():
        sql = "SELECT Value, ActionDate FROM History WHERE DeviceID = 1 and SessionID = (SELECT MAX(SessionID) FROM Sessions)"
        return Database.get_rows(sql)

    
    @staticmethod
    def read_values_temp():
        sql = "SELECT Value, ActionDate FROM History WHERE DeviceID = 2 and SessionID = (SELECT MAX(SessionID) FROM Sessions)"
        return Database.get_rows(sql)
    
    @staticmethod
    def read_values_air():
        sql = "SELECT Value, ActionDate FROM History WHERE DeviceID = 3 and SessionID = (SELECT MAX(SessionID) FROM Sessions)"
        return Database.get_rows(sql)
    
    @staticmethod
    def read_bpm_by_id(sessionid):
        sql = 'Select Value, ActionDate from History where SessionID = %s and DeviceID = 1;'
        params = [sessionid]
        return Database.get_rows(sql, params)
    
    @staticmethod
    def read_temp_by_id(sessionid):
        sql = 'Select Value, ActionDate from History where SessionID = %s and DeviceID = 2;'
        params = [sessionid]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_air_by_id(sessionid):
        sql = 'Select Value, ActionDate from History where SessionID = %s and DeviceID = 3;'
        params = [sessionid]
        return Database.get_rows(sql, params)
    

    @staticmethod
    def get_all_sessions(username):
        sql = 'SELECT * FROM Sessions s join User u on u.UserID = s.UserID where u.Username = %s'
        params = [username]
        return Database.get_rows(sql, params)


    @staticmethod
    def start_session(userid, timestamp):
        sql = "INSERT INTO Sessions (UserID, StartTime, Endtime) VALUES (%s, %s, null);"
        params = [userid, timestamp]
        return Database.execute_sql(sql, params)
        
    
    @staticmethod
    def end_session(timestamp):
        sql = "UPDATE Sessions SET EndTime = %s WHERE SessionID = (SELECT MAX(SessionID) FROM Sessions);"
        params = [timestamp]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def update_title(title):
        sql = "Update Sessions set Titel = %s where SessionID = (SELECT MAX(SESSIONID) from Sessions);"
        params = [title]
        return Database.execute_sql(sql, params)



    #maxbpm(db) voor beetje duidelijkheid tussen bpm value en maxbpm
    @staticmethod
    def create_user(Username, DOB, Maxbpm):
        sql = "INSERT INTO User (Username, DOB, Maxbpm) VALUES (%s, %s, %s);"
        params = [Username, DOB, Maxbpm]
        return Database.execute_sql(sql, params)
    


    @staticmethod
    def check_user(username):
        sql = "SELECT * FROM User WHERE Username = %s;"
        params = [username]
        return Database.get_one_row(sql, params)

    
    @staticmethod
    def update_user_bpm(username, maxbpm):
        print(maxbpm)
        sql = "UPDATE User SET Maxbpm = %s WHERE Username = %s;"
        params = [maxbpm, username]
        return Database.execute_sql(sql, params)

    