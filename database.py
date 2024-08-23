import mysql.connector
class Database:
    def __init__(self):

        # Setup MySQL connection here and add your db password here
        self.conn = mysql.connector.connect(host='localhost', password='-----------', user='root',database="tkinter_project1")
        self.cursor = self.conn.cursor()
        self.username=None

    def insert_user(self, username, hashed_password, email, phone):
        try:
            query = "INSERT INTO users_info (username, password, email, contact) VALUES (%s, %s,%s, %s)"
            self.cursor.execute(query, (username, hashed_password, email, phone))
            self.conn.commit()
            return True
        except mysql.connector.IntegrityError:  # Handle duplicate usernames
            return False

    def get_user_password(self, username):
        query = "SELECT password FROM users_info WHERE username = %s"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        if result:
            self.username = username
            return result[0]
        return None
    #--------------------------table->problems-----------------------------------------------------------
    def insert_problem(self, name, difficulty, topic, status, url, notes):
        user_Id = self.current_user_id()
        query = "INSERT INTO problems (name, difficulty, topic, status, url, notes, user_Id)  VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (name, difficulty, topic, status, url, notes, user_Id))
        self.conn.commit()
        if(status=="Solved"):
            pid = self.get_problem_Id(name,difficulty,topic,status,url)
            self.insert_problem_solved(pid,difficulty,topic)

    def get_all_problems(self):
        userId = self.current_user_id()
        query = "SELECT name, difficulty, topic, status, url FROM problems WHERE user_Id=%s"
        self.cursor.execute(query,(userId,))
        return self.cursor.fetchall()

    def deleteProblems(self,l1):
        probId = self.get_problem_Id(l1[0][0],l1[0][1],l1[0][2],l1[0][3],l1[0][4])
        query = "DELETE FROM problems where id=%s"
        self.cursor.execute(query, (probId))
        self.conn.commit()

    def get_problem_Id(self,name,difficulty,topic,status,url):
        userId = self.current_user_id()
        query = "SELECT id FROM problems WHERE name=%s and difficulty = %s and topic=%s and status=%s and url=%s and user_Id=%s"
        self.cursor.execute(query, (name,difficulty,topic,status,url,userId))
        myresult = self.cursor.fetchall()
        return myresult[0][0]

    def update_problem(self,updated_name, updated_level, updated_topic, updated_status, updated_url,prevList):
        pID = self.get_problem_Id(prevList[0][0],prevList[0][1],prevList[0][2],prevList[0][3],prevList[0][4])
        query = "UPDATE problems SET name=%s, difficulty = %s, topic=%s, status=%s, url=%s WHERE id=%s "
        self.cursor.execute(query, (updated_name,updated_level,updated_topic,updated_status,updated_url,pID))
        self.conn.commit()
        if(updated_status!="Solved"):
            self.delete_problem_solved(pID)


    def filter_problems(self,level, status):
        userId = self.current_user_id()
        query = "SELECT name, difficulty, topic, status, url FROM problems WHERE user_Id=%s"
        params = [userId]

        if level and level != "All":
            query += " AND difficulty = %s"
            params.append(level)
        if status and status != "All":
            query += " AND status = %s"
            params.append(status)

        self.cursor.execute(query, tuple(params))

        return self.cursor.fetchall()
    
    def get_Notes(self,lst):
        id=self.get_problem_Id(lst[0],lst[1],lst[2],lst[3],lst[4])
        query = "SELECT notes FROM problems WHERE id=%s"
        self.cursor.execute(query, (id,))
        return self.cursor.fetchall()
    
    def updateNote(self,data,lst):
        id=self.get_problem_Id(lst[0],lst[1],lst[2],lst[3],lst[4])
        query = "UPDATE problems SET notes=%s WHERE id=%s"
        self.cursor.execute(query, (data,id))
        self.conn.commit()

    def deleteNote(self,lst):
        id=self.get_problem_Id(lst[0],lst[1],lst[2],lst[3],lst[4])
        query = "UPDATE problems SET notes = NULL WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.conn.commit()

    #tab3 ->> stats table used = users_info

    def current_user_id(self):
        query = "SELECT id FROM users_info WHERE username=%s"
        self.cursor.execute(query, (self.username,))
        userId = self.cursor.fetchall()
        return userId[0][0]
    
    def delete_problem_solved(self, problem_id):
        userId = self.current_user_id()
        query = "DELETE FROM user_progress WHERE problem_id=%s AND user_id=%s "
        self.cursor.execute(query, (problem_id, userId))
        self.conn.commit()

    def insert_problem_solved(self, problem_id, difficulty, topic):
        userId = self.current_user_id()
        query = "INSERT INTO user_progress (user_id, problem_id, solved_date, difficulty, topic) VALUES ( %s, %s, CURDATE(), %s, %s)  "
        self.cursor.execute(query, (userId, problem_id, difficulty, topic))
        self.conn.commit()

    def get_solved_problems(self):
        userId = self.current_user_id()
        query = "SELECT COUNT(*) FROM user_progress WHERE user_id = %s AND solved_date = CURDATE() "
        self.cursor.execute(query, (userId,))
        count = self.cursor.fetchall()
        return count[0][0]

    def get_weekly_report(self):
        userId = self.current_user_id()
        query = "SELECT COUNT(*) FROM user_progress WHERE user_id = %s AND solved_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)"
        self.cursor.execute(query, (userId,))
        count = self.cursor.fetchall()
        return count[0][0]
    
    def get_data_by_difficulty(self):
        userId = self.current_user_id()
        query = "SELECT difficulty, COUNT(*) FROM user_progress WHERE user_id = %s GROUP BY difficulty"
        self.cursor.execute(query, (userId,))
        return self.cursor.fetchall()
    
    def get_data_by_topic(self):
        userId = self.current_user_id()
        query = "SELECT topic, COUNT(*) FROM user_progress WHERE user_id = %s GROUP BY topic"
        self.cursor.execute(query, (userId,))
        return self.cursor.fetchall()
    
    #tab4 ->> plotting
    def plot_problems_db(self):
        userId = self.current_user_id()
        dates = []
        counts = []
        userId = self.current_user_id()
        query = "SELECT solved_date, COUNT(*) FROM user_progress WHERE user_id = %s GROUP BY solved_date;"
        self.cursor.execute(query, (userId,))
        result = self.cursor.fetchall()
        for d, x in result:
            dates.append(str(d))
            counts.append(x)
        return dates, counts
    
    def plot_difficulty_db(self):
        userId = self.current_user_id()
        labels = []
        counts = []
        userId = self.current_user_id()
        query = "SELECT difficulty, COUNT(*) FROM user_progress WHERE user_id = %s GROUP BY difficulty;"
        self.cursor.execute(query, (userId,))
        result = self.cursor.fetchall()
        for l,x in result:
            labels.append(l)
            counts.append(x)
        return labels, counts
    
    def plot_topic_db(self):
        userId = self.current_user_id()
        topic = []
        counts = []
        userId = self.current_user_id()
        query = "SELECT topic, COUNT(*) FROM user_progress WHERE user_id = %s GROUP BY topic;"
        self.cursor.execute(query, (userId,))
        result = self.cursor.fetchall()
        for t,x in result:
            topic.append(t)
            counts.append(x)
        return topic, counts






        

        

