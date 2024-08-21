def prenesi_om():
    print("Prenašam tabelo OM...")
    result_om = ConnectMySql().get_all_om()
    stevec = 0
    if result_om:
        for rowl in result_om:
            stevec += 1
            print(stevec)
            # Če so v bass polja za aglomeracijo prazna, daj -1
            if not (isanumber(rowl[14])):
                rowl[14] = "-1"
            if not (isanumber(rowl[15])):
                rowl[15] = "-1"

            # Za vsako om poišči storitve

            om_id = rowl[0]
            # Voda - določi glede na šifro upravitelja
            upravitelj_id = rowl[12]
            match upravitelj_id:
                case "01":  # Radgonski vodovod
                    rowl[7] = "1"
                case "25":  # MB vodovod
                    rowl[7] = "2"
                case "09", "10", "27", "28":  # Lastna voda
                    rowl[7] = "3"
                case _:
                    rowl[7] = "0"

            result_storitve = ConnectMySql().get_storitve(om_id)
            if result_storitve:
                # Odvajanje
                if result_storitve.count("ODV") > 0:
                    rowl[8] = "1"
                # Čiščenje
                if result_storitve.count("CIS") > 0:
                    rowl[9] = "1"
                # Greznice
                if (
                    result_storitve.count("GRE") > 0
                    or result_storitve.count("GRES") > 0
                ):
                    rowl[10] = "1"

            elif result_storitve:
                print("Nima storitev")

        print("Zapisov: ", len(result_om))

        # Zapiši tabelo v ArcGis om_table
        # Izprazni staro tabelo

        tbl_name = "om_table_novo"
        try:
            arcpy.management.TruncateTable(tbl_name)
            print("Praznim tabelo " + tbl_name + "... ok")
        except Exception as e:
            print("Napaka", e)

        #     Napolni novo tabelo s podatki
        print("Dodajam odjemna mesta v tabelo ", tbl_name)
        with arcpy.da.InsertCursor(
            tbl_name,
            [
                "id_om",
                "hs_mid",
                "naziv",
                "naslov",
                "placnik",
                "ulica",
                "posta",
                "vod",
                "odv",
                "cis",
                "gre",
                "odp",
                "id_upravljalec",
                "upravljalec",
                "aglok",
                "aglov",
                "aglok_ime",
                "aglov_ime",
                "status",
                "meter_id",
                "meter_desc",
            ],
        ) as cursor:
            for row in result_om:
                # print(row)
                try:
                    cursor.insertRow(row)
                except Exception as e:
                    print("Napaka pri dodajanju " + row[2] + " ", e)
        print("Končano.")
    else:
        print("Warning", "No data from database")
        return
