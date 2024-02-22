PREDICT_SELECT = ("SELECT VAL, RECORD_ID "
                  "FROM DBRECORDS "
                  "WHERE ROWNUM <= 10 ")


def get_predict_select():
    return PREDICT_SELECT
