import tensorflow as tf
import numpy as np
import utils
import oracledb
import config.config_db as config_db
import sql


def predict(model_name, predict_data):
    print('predict')
    predict_arr = list()
    if type(predict_data) is list:
        predict_arr = predict_data
    else:
        predict_arr.append(predict_data)

    predict_arr = list(map(utils.str_to_arr, predict_arr))

    predict_arr = tf.stack(predict_arr)

    print('predict_arr = ' + predict_arr)
    model = tf.keras.models.load_model(model_name)
    return list(map(np.argmax, model.predict(predict_arr)))


def test_predict(model_name):
    print('test_predict')
    with oracledb.connect(user=config_db.USER,
                          password=config_db.PASSWORD,
                          dsn=config_db.DSN) as connection:
        with connection.cursor() as cursor:
            for r in cursor.execute(sql.get_predict_select()):
                predict_result = predict(model_name, r[0])
                with connection.cursor() as cursor_upd:
                    cursor_upd.execute(sql.get_predict_update(),
                                       class_check_id=int(predict_result[0]),
                                       record_id=int(r[1]))
                    connection.commit()
