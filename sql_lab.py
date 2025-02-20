'''
This is the framework you'll fill out for this assignment.
Each question on the lab corresponds to one of the functions in the LabSuite class.
You should fill out each function so that it returns the desired results from the database.

Because changes to the framework can interfere with the autograding tests,
you shouldn't modify any other parts of the framework beyond those indicated.
'''

import sqlite3

class LabSuite(object):

    def __init__(self):
        """Initializes the LabSuite object.      
        """
        self.db_name = './assignment.db'

    def connect(self):
        """Establishes a connection to the database.

        Returns a SQLite connection object to the database defined in self.db_name.

        Returns:
            An open sqlite3.Connection object.
        """
        conn = sqlite3.connect(self.db_name)
        return conn    
    
    def five_year_rangers(self):
        """Returns the first and last names of all rangers who have worked for exactly five years,
        sorted alphabetically by last name, then first name.
        Don't modify this function - it's already filled in for you as an example.
        If your submission is working correctly, the test for this one
        should work without you changing anything.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # You'll write your SQL queries as the string argument passed to cursor.execute(),
        # like so:
        cursor.execute("""SELECT firstname, lastname
                          FROM Ranger
                          WHERE years_worked = 5
                          ORDER BY lastname, firstname;""")
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_overlooks(self):
        """Returns the names of all overlook stations, sorted alphabetically.
        A station is an overlook station if its name begins with the word "Overlook."
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
        cursor.execute("""SELECT name 
                          FROM Station 
                          WHERE name LIKE "%Overlook%" 
                          ORDER BY name """)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_station_elevation(self):
        """Returns the names of all stations and their elevations in miles, 
        sorted alphabetically by station name.
        Note that in the database, elevation is stored in feet.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
        cursor.execute("""SELECT name, elevation * 1.0 / 5280 
                          FROM Station
                          ORDER BY name""")
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_average_deer(self):
        """Returns the average number of deer spotted per deer sighting.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
        cursor.execute("""
                       SELECT AVG(number) 
                        FROM Sighting
                        WHERE species = "Deer" """)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_station_seven_animals(self):
        """Returns the species and total number of each animal that has been
           sighted at the station with station ID 7, sorted alphabetically by 
           species name.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
        cursor.execute("""
                       SELECT species, SUM(number) as total_number
                        FROM Sighting
                        JOIN Shift ON Sighting.shift_id = Shift.shift_id
                       WHERE Shift.station_id = 7
                       GROUP BY species
                       ORDER BY species
                       """)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_birdwatchers(self):
        """Returns the first and last names of all rangers who have seen at least one eagle
        and at least one falcon, sorted alphabetically by last name, then first name.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
        cursor.execute("""
                       SELECT firstname, lastname 
                       FROM Ranger
                       JOIN Shift ON Ranger.ranger_id = Shift.ranger_id
                       JOIN Sighting ON Sighting.shift_id = Shift.shift_id
                       WHERE Sighting.species = "Eagle" AND Sighting.number > 0
                       INTERSECT
                       SELECT firstname, lastname 
                       FROM Ranger
                       JOIN Shift ON Ranger.ranger_id = Shift.ranger_id
                       JOIN Sighting ON Sighting.shift_id = Shift.shift_id
                       WHERE Sighting.species = "Falcon" AND Sighting.number > 0
                       ORDER BY lastname, firstname
                       """)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_distant_stations(self):
        """Returns the names and trail distances of all stations that are further along the trail
        than the station with station ID 4, sorted by trail distance in increasing order.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
        cursor.execute("""
                       SELECT name, trail_distance
                        FROM Station
                        WHERE trail_distance > (SELECT trail_distance FROM Station WHERE station_id = 4)
                        ORDER BY trail_distance
                       """)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_wild_stations(self):
        """Returns the name of each station and the number of unique species that
        have been spotted there for each station where at least six unique species
        have been spotted. Results should be sorted alphabetically by station name.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
        cursor.execute("""
                       SELECT name, COUNT(DISTINCT species) 
                       FROM Station
                       JOIN Shift ON Station.station_id = Shift.station_id
                       JOIN Sighting ON Sighting.shift_id = Shift.shift_id
                       GROUP BY Station.name
                       HAVING COUNT(DISTINCT species) >= 6
                        """)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_first_worker(self):
        """Returns the first and last name of the ranger who worked the 
        earliest recorded shift in the database.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
                          # SELECT firstname, lastname 
#                         FROM Ranger 
#                        JOIN Shift ON Ranger.ranger_id = Shift.ranger_id
#                        GROUP BY Shift.start_time
#                        HAVING Shift.start_time <= MIN(Shift.start_time)

        cursor.execute("""
                       SELECT firstname, lastname
                       FROM Ranger 
                       JOIN Shift ON Ranger.ranger_id = Shift.ranger_id
                       WHERE start_time = (SELECT MIN(start_time) FROM Shift)
                       """)
        results = cursor.fetchall()
        conn.close()
        return results
    

lab = LabSuite()
a = lab.find_first_worker()
print(a)
print(len(a))