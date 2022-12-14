import json
import time
import logging
from exceptions import NotFound
from exceptions import NoAccess


Template_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w', format=Template_format)


file_1 = open("company_db.json")
comp_data = file_1.read()
dict_1 = json.loads(comp_data)


file_2 = open("users_db.json")
user_data = file_2.read()
dict_2 = json.loads(user_data)


def time_counter(func):
    def wrap(user_id, company_id):
        t1 = time.time()
        result = func(user_id, company_id)
        t2 = time.time()
        logging.info(f"Execution time {t2 - t1}")
        return result
    return wrap


def exception_handler(func):
    def wrap(user_id, company_id):
        try:
            result = func(user_id, company_id)
            return result
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
    return wrap


def user_access(func):
    def wrap(user_id, company_id):
        user = dict_2.get(user_id)
        if user is None:
            raise NotFound
        elif int(company_id) not in user.get("companies"):
            raise NoAccess
        else:
            result = func(user_id, company_id)
        return result
    return wrap


@exception_handler
@user_access
@time_counter
def get_company_city(user_id, company_id):
    logging.info("Start func get_company_city")
    company = dict_1.get(company_id)
    if company is None:
        raise NotFound
    else:
        city = company.get("city")
        return city


get_company_city("1", "1")
