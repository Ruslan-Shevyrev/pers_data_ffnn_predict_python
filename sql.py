CONTAINERS_COUNT = ''
CONTAINER_NUM = ''
RECORDS_OFFSET = ''
RECORDS_COUNT = ''

'''
PREDICT_SELECT = ("SELECT VAL, RECORD_ID "
                  "FROM TABLE(PKG_CLEAR_DATA.GET_DBRECORDS)")
'''

PREDICT_SELECT = ("SELECT VAL, RECORD_ID "
                  "FROM V_DBRECORDS_FOR_PREDICT")


PREDICT_UPDATE = ("UPDATE DBRECORDS "
                  "SET CLASS_CHECK_ID = :class_check_id "
                  "WHERE RECORD_ID = :record_id")


CONTAINER_RECORDS_COUNT = ("SELECT (trunc((SELECT COUNT(*) FROM V_DBRECORDS_FOR_PREDICT)/ :containers_cnt) + 1) * (:container_num - 1) AS RECORDS_OFFSET, "
                           "(trunc((SELECT COUNT(*) FROM V_DBRECORDS_FOR_PREDICT) / :containers_cnt) + 1) * :container_num AS RECORDS_COUNT "
                            "FROM DUAL ")


def get_predict_select():
    if RECORDS_OFFSET != '' and RECORDS_COUNT != '':
        return PREDICT_SELECT + " OFFSET "+RECORDS_OFFSET+" ROWS FETCH NEXT "+RECORDS_COUNT+" ROWS ONLY"
    else:
        return PREDICT_SELECT


def get_predict_update():
    return PREDICT_UPDATE


def get_container_records_count():
    return CONTAINER_RECORDS_COUNT
