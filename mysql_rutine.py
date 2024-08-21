import mysql.connector
import sql_querys
import vars


class ConnectMySql:
    def __init__(self):
        self.host = vars.mydbhost
        self.user = vars.mydbuser
        self.port = vars.mydbport
        self.database = vars.mydbname
        self.password = vars.mydbpass
        self.con = None

    def connect(self):
        self.con = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            port=self.port,
            database=self.database,
        )

    def get_storitve(self, omid):
        # Preberi vse storitve za določeno om
        try:
            self.connect()
            cursor = self.con.cursor()
            sql = """
                SELECT
                inkasso_2021_omstoritve_radgona.OMSTORITVE_STORITEV AS id_stor
                FROM racuni_2021_storitve_radgona,
                        inkasso_2021_omstoritve_radgona
                        INNER JOIN inkasso_2021_om_radgona
                            ON inkasso_2021_omstoritve_radgona.OM = inkasso_2021_om_radgona.OM
                WHERE inkasso_2021_omstoritve_radgona.OM = %s
                GROUP BY inkasso_2021_omstoritve_radgona.OMSTORITVE_STORITEV
            """

            # select sett_code,sett_name from bass_location_sett where municip_code = %s order by sett_name"
            cursor.execute(sql, ([omid]))

            # Vrni navadni list
            result = [result[0] for result in cursor.fetchall()]
            return result

        except Exception as e:
            print("Napaka: get_storitve!")
            print(e)

        finally:
            if self.con:
                self.con.close()

    # Preberi vsa OM
    def get_all_om(self):
        try:
            self.connect()
            cursor = self.con.cursor()
            sql = sql_querys.all_om_sql

            cursor.execute(sql)
            result = cursor.fetchall()
            result_list = [list(row) for row in result]

            return result_list

        except Exception as e:
            print("Get data failed - OM")
            print(e)

        finally:
            if self.con:
                self.con.close()

    def get_all_naselja(self):
        try:
            self.connect()
            cursor = self.con.cursor()
            sql = "select sett_code,sett_name from bass_location_sett where municip_code = %s order by sett_name"
            cursor.execute(sql, ([vars.obcinaId]))
            # cursor.execute(sql)
            result = cursor.fetchall()

            return result

        except Exception as e:
            print("Get data failed")
            print(e)

        finally:
            if self.con:
                self.con.close()

    def get_all_storitve(self):
        try:
            self.connect()
            cursor = self.con.cursor()
            sql = """select storitev_sifra as sifra, 
                      storitev_naziv as naziv from racuni_2021_storitve_radgona 
                      order by sifra"""
            cursor.execute(sql)
            # cursor.execute(sql)
            result = cursor.fetchall()

            return result

        except Exception as e:
            print("Storitve - get data failed")
            print(e)

        finally:
            if self.con:
                self.con.close()

    def get_data(self):
        try:
            self.connect()
            cursor = self.con.cursor()
            sql = """select storitev_sifra as sifra, 
                      storitev_naziv as naziv from racuni_2021_storitve_radgona 
                      order by sifra"""
            cursor.execute(sql)
            # cursor.execute(sql)
            result = cursor.fetchall()

            return result

        except Exception as e:
            print("Storitve - get data failed")
            print(e)

        finally:
            if self.con:
                self.con.close()
