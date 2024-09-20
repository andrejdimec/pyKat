all_om_sql = """
            SELECT
              inkasso_2021_om_radgona.OM AS om,
              bass_location_list.location_hsmid AS omhsmid,
              inkasso_2021_om_radgona.OM_NAZIV AS omnaziv,
              CONCAT(bass_location_street.street_name, ' ', IFNULL(inkasso_2021_om_radgona.OM_HS, ''), inkasso_2021_om_radgona.OM_HSD) AS omnaslov,
              stranke_radgona_2021.NAZIV AS placnik,
              CONCAT(stranke_radgona_2021.NASLOV,', ',stranke_radgona_2021.KRAJ) as pl_naslov,
              '0' AS vod,
              '0' AS odv,
              '0' AS odv_dod,
              '0' AS cis,
              '0' AS gre,
              '0' AS odp,
              inkasso_2021_komercialisti_radgona.KOMERCIALIST_SIFRA AS id_upravljalec,
              inkasso_2021_komercialisti_radgona.KOMERCIALIST_NAZIV AS upravljalec,
              bass_location_list.agl_cannal_code AS aglok,
              bass_location_list.agl_code AS aglov,
              '' as aglok_ime,
              '' as aglov_ime,
              inkasso_2021_statusi_radgona.STATUS_NAZIV AS status,
              inkasso_2021_meters_radgona.meter_meteridentification AS meter_id,
              inkasso_2021_rrmetertype_radgona.rrmetertype_desc AS meter_desc,
              bass_location_list.location_xh AS x,
              bass_location_list.location_yh AS y,
              bass_location_list.location_code AS location_code

              
            FROM inkasso_2021_om_radgona
              INNER JOIN stranke_radgona_2021
                ON inkasso_2021_om_radgona.OM_PLACNIK = stranke_radgona_2021.SIFRA
              LEFT OUTER JOIN inkasso_2021_omstoritve_radgona
                ON inkasso_2021_om_radgona.OM = inkasso_2021_omstoritve_radgona.OM
              LEFT OUTER JOIN inkasso_2021_meters_radgona
                ON inkasso_2021_om_radgona.OM = inkasso_2021_meters_radgona.om
              LEFT OUTER JOIN inkasso_2021_rrmetertype_radgona
                ON inkasso_2021_meters_radgona.rrmetertype_type = inkasso_2021_rrmetertype_radgona.rrmetertype_type
              LEFT OUTER JOIN inkasso_2021_statusi_radgona
                ON inkasso_2021_om_radgona.STATUS_SIFRA = inkasso_2021_statusi_radgona.STATUS_SIFRA
              LEFT OUTER JOIN inkasso_2021_komercialisti_radgona
                ON inkasso_2021_om_radgona.KOMERCIALIST_SIFRA = inkasso_2021_komercialisti_radgona.KOMERCIALIST_SIFRA
              LEFT OUTER JOIN bass_location_list
                ON inkasso_2021_om_radgona.location_code = bass_location_list.location_code
              LEFT OUTER JOIN bass_location_sett
                ON bass_location_list.sett_code = bass_location_sett.sett_code
              LEFT OUTER JOIN bass_location_street
                ON bass_location_list.street_code = bass_location_street.street_code
            WHERE inkasso_2021_om_radgona.OM_AKTIVEN = 'T' 
            # AND bass_location_list.location_hsmid=0 OR bass_location_list.location_hsmid=99 
            GROUP BY inkasso_2021_om_radgona.OM,
                    bass_location_list.location_hsmid,  
                     inkasso_2021_komercialisti_radgona.KOMERCIALIST_SIFRA
            ORDER BY omnaslov
            
"""
