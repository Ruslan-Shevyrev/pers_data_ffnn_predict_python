import tensorflow as tf
import numpy as np
import utils
import oracledb
import config.config_db as config_db
import sql
import os

os.environ['CUDA_VISIBLE_DEVICES'] = ''


def predict(model, predict_data):
    predict_arr = list()
    if type(predict_data) is list:
        predict_arr = predict_data
    else:
        predict_arr.append(predict_data)

    predict_arr = list(map(utils.str_to_arr, predict_arr))

    predict_arr = tf.stack(predict_arr)

    return list(map(np.argmax, model.predict(predict_arr)))


def predict_model_name(model_name, predict_data):
    model = tf.keras.models.load_model(model_name)
    return predict(model, predict_data)


def test_predict(model_name):

    sql.CONTAINERS_COUNT = os.getenv('CONTAINERS_COUNT', '')
    sql.CONTAINER_NUM = os.getenv('CONTAINERS_NUM', '')

    model = tf.keras.models.load_model(model_name)

    prev_id = ''

    with oracledb.connect(user=config_db.USER,
                          password=config_db.PASSWORD,
                          dsn=config_db.DSN) as connection:
        with connection.cursor() as cursor:
            if sql.CONTAINERS_COUNT != '' and sql.CONTAINER_NUM != '':
                for r in cursor.execute(sql.get_container_records_count(),
                                        containers_cnt=int(sql.CONTAINERS_COUNT),
                                        container_num=int(sql.CONTAINER_NUM)):
                    sql.RECORDS_OFFSET = str(r[0])
                    sql.RECORDS_COUNT = str(r[1])
                    print('Running in parallel mode: from '+sql.RECORDS_OFFSET+' to '+sql.RECORDS_COUNT)
            else:
                print('Running in single mode')

            try:
                for r in cursor.execute(sql.get_predict_select()):
                    predict_result = predict(model, r[0])
                    with connection.cursor() as cursor_upd:
                        cursor_upd.execute(sql.get_predict_update(),
                                           class_check_id=int(predict_result[0]),
                                           record_id=int(r[1]))
                        connection.commit()
                        prev_id = r[1]
            except UnicodeDecodeError:
                print('UnicodeDecodeError: previous id:' + str(prev_id))
