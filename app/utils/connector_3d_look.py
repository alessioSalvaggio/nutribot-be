from fake_useragent import UserAgent
import httpagentparser
from app.utils.utils_3d_look import *
from typing import List

def generate_new_measurement_widget(user_email: str, user_first_name: str, user_gender_tag: str, user_gender: str, user_height: int, user_weight: int, return_url: str) -> List[str]:
    ua = UserAgent(os=["Windows"]).random
    parsed_ua = httpagentparser.detect(ua)
    
    UUID = c1(ua, parsed_ua)
    mtm_client = c2(UUID, ua, parsed_ua)
    welcome_page(UUID, mtm_client, return_url, ua, parsed_ua)
    email_and_full_name(UUID, user_email, user_first_name, ua, parsed_ua)
    gender_page(UUID, user_gender_tag, ua, parsed_ua)
    height_weight_page(UUID, user_weight, user_height, ua, parsed_ua)
    response = final_page(UUID, user_email, user_first_name, user_gender, user_height, user_weight, return_url, mtm_client, ua, parsed_ua)
    return response, UUID

def get_measurement_widget_data(UUID: str):
    ua = UserAgent(os=["Windows"]).random
    parsed_ua = httpagentparser.detect(ua)
    return get_mtm_widget_data(UUID, ua, parsed_ua)

if __name__ == "__main__":
    user_email = "v.1@testemail.net"
    user_first_name = "Vlad I"
    user_gender_tag = "GENDER_PAGE_MALE_GENDER_SELECTED" # "GENDER_PAGE_FEMALE_GENDER_SELECTED"
    user_gender = "male" # "female"
    user_height = 188
    user_weight = 120
    return_url = "https://hypaz.com/"
    print(generate_new_measurement_widget(user_email, user_first_name, user_gender_tag, user_gender, user_height, user_weight, return_url))