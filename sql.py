'''
PREDICT_SELECT = ("SELECT VAL, RECORD_ID "
                  "FROM DBRECORDS "
                  "WHERE CLASS_CHECK_ID IS NULL "
                  "AND VAL = CONVERT(VAL,'UTF8')")
'''


PREDICT_SELECT = ("SELECT VAL, RECORD_ID "
                  "FROM TABLE(PKG_CLEAR_DATA.GET_DBRECORDS)")


PREDICT_UPDATE = ("UPDATE DBRECORDS "
                  "SET CLASS_CHECK_ID = :class_check_id "
                  "WHERE RECORD_ID = :record_id")


def get_predict_select():
    return PREDICT_SELECT


def get_predict_update():
    return PREDICT_UPDATE
