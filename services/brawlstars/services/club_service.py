import os
import requests
import urllib.parse

class ClubService:
    def __init__(self):
        self.base_url = "https://api.brawlstars.com/v1/clubs"

    def get_all_members_dict_by_id(self, clubTag):
        requestUrl = f"{self.base_url}/{urllib.parse.quote(clubTag)}"
       
        response = requests.get(
            requestUrl,
            headers={'Authorization': "Bearer " + os.environ['JWT_TOKEN']}
        )

        members_dict = {}
        print(response.content)
        if response.status_code == 200:
            json_response = response.json()

            for member in json_response["members"]:
                member_tag = member["tag"]
                members_dict[member_tag] = member

        return members_dict
