from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.util.parse import match_one
from mycroft.audio import wait_while_speaking

from . import hotels


class HotelSearcher(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.is_reading = False

    @intent_handler('searcher.hotel.intent')
    def handle_searcher_hotel(self, message):
        if message.data.get('city') is None:
            response = self.get_response('searcher.hotel', num_retries=0)
            if response is None:
                return
        else:
            response = message.data.get('city')
        self.speak_dialog('let_me_think', data={'city': response})
        hotels_result = hotels.search(response)
        self.log.info(f'Hotels result: {str(hotels_result)}')
        for hotel in hotels_result:
            self.speak(hotel, wait=True)
        # self.speak_dialog('searcher.hotel')


def create_skill():
    return HotelSearcher()
