from typing import Optional
from json.decoder import JSONDecodeError

from requests import post
from requests.auth import HTTPBasicAuth

from .error import BadLogin, NotFound, BadResponse
from .base import ShellyBase


class ShellyGen1(ShellyBase):

    def __init__(self, ip: str, port: int = 80, *args, **kwargs) -> None:
        """
        @param      ip      the target IP of the shelly device. Can be a string, list of strings or list of integers
        @param      port    target port, may be useful for non Shelly devices that have the same HTTP Api
        @param      login   dict of login credentials. Keys needed are "username" and "password"
        @param      timeout specify the amount of time until requests are aborted.
        @param      debug   enable debug printing
        @param      init    calls the update method on init
        """

        super().__init__(ip, port, *args, **kwargs)
        self._generation = 1

    def update(self) -> None:
        """
        @brief update the Shelly attributes
        """
        status = self.settings()

        self._type = status['device'].get("type", self._type)
        self._name = status['device'].get("hostname", self._name)

        # Settings are already fetched to get device information might as well put the list of things the device has somewhere
        self.relays = status.get("relays", [])
        self.rollers = status.get("rollers", [])
        # RGBW reuses the same lights array
        self.lights = status.get("lights", [])

        self.irs = status.get("light_sensor", None)

        self.emeters = status.get("emeter", [])

        self.meters = []
        meter_index = 0
        # Meters are not returned as part of the settings
        while True:
            try:
                # Request meter information
                self.meter.append(self.meter(meter_index))
                meter_index += 1
            except Exception:
                break

    def post(self, page, values = None):
        """
        @brief      returns settings

        @param      page    page to be accessed. Use the Shelly HTTP API Reference to see what's possible

        @return     returns json response
        """

        url = f"{self._proto}://{self._hostname}:{self._port}/{page}?"

        if values:
            url += "&".join([f"{key}={value}" for key, value in values.items()])

        if self._debugging:
            print(f"Target Address: {url}\nAuthentication: {any(self._credentials)}\nTimeout: {self._timeout}")

        credentials = HTTPBasicAuth(*self._credentials)

        response = post(url, auth=credentials,
                        timeout=self._timeout)

        if response.status_code == 401:
            raise BadLogin()
        elif response.status_code == 404:
            raise NotFound("Not Found")

        try:
            return response.json()
        except JSONDecodeError:
            raise BadResponse("Bad JSON")

    def status(self):
        """
        @brief      returns status response

        @return     status dict
        """
        return self.post("status")

    def settings(self, subpage = None):
        """
        @brief      returns settings

        @param      subpage page to be accessed. Use the Shelly HTTP API Reference to see what's possible

        @return     returns settings as a dict
        """

        page = "settings"
        if subpage:
            page += "/" + subpage

        return self.post(page)

    def meter(self, index):
        """
        @brief      Get meter information from a relay at the given index

        @param      index  index of the relay
        @return     returns attributes of meter: power, overpower, is_valid, timestamp, counters, total
        """

        return self.post(f"meter/{index}")

    def relay(self, index, *args, **kwargs):
        """
        @brief      Interacts with a relay at the given index

        @param      index  index of the relay
        @param      turn   Will turn the relay on or off
        @param      timer  a one-shot flip-back timer in seconds
        """

        values = {}

        turn = kwargs.get("turn", None)
        timer = kwargs.get("timer", None)

        if turn is not None:
            if turn:
                values["turn"] = "on"
            else:
                values["turn"] = "off"

        if timer:
            values["timer"] = timer

        return self.post(f"relay/{index}", values)

    def roller(self, index, *args, **kwargs):
        """
        @brief      Interacts with a roller at a given index

        @param      self        The object
        @param      index       index of the roller. When in doubt use 0
        @param      go          way of the roller to go. Accepted are "open", "close", "stop", "to_pos"
        @param      roller_pos  the wanted position in percent
        @param      duration    how long it will take to get to that position
        """

        go = kwargs.get("go", None)
        roller_pos = kwargs.get("roller_pos", None)
        duration = kwargs.get("duration", None)

        values = {}

        if go:
            values["go"] = go

        if roller_pos is not None:
            values["roller_pos"] = self._clamp_percentage(roller_pos)

        if duration is not None:
            values["duration"] = duration

        return self.post(f"roller/{index}", values)

    def light(self, index, *args, **kwargs):
        """
        @brief      Interacts with lights at a given index

        @param      mode        Accepts "white" and "color" as possible modes
        @param      index       index of the light. When in doubt use 0
        @param      timer       a one-shot flip-back timer in seconds
        @param      turn        Will turn the lights on or off
        @param      red         Red brightness, 0..255, only works if mode="color"
        @param      green       Green brightness, 0..255, only works if mode="color"
        @param      blue        Blue brightness, 0..255, only works if mode="color"
        @param      white       White brightness, 0..255, only works if mode="color"
        @param      gain        Gain for all channels, 0...100, only works if mode="color"
        @param      temp        Color temperature in K, 3000..6500, only works if mode="white"
        @param      brightness  Brightness, 0..100, only works if mode="white"
        """
        mode = kwargs.get("mode", None)
        timer = kwargs.get("timer", None)
        turn = kwargs.get("turn", None)
        red = kwargs.get("red", None)
        green = kwargs.get("green", None)
        blue = kwargs.get("blue", None)
        white = kwargs.get("white", None)
        gain = kwargs.get("gain", None)
        temp = kwargs.get("temp", None)
        brightness = kwargs.get("brightness", None)

        values = {}

        if mode:
            values["mode"] = mode

        if timer is not None:
            values["timer"] = timer

        if turn is not None:
            if turn:
                values["turn"] = "on"
            else:
                values["turn"] = "off"

        if red is not None:
            values["red"] = self._clamp(red)

        if green is not None:
            values["green"] = self._clamp(green)

        if blue is not None:
            values["blue"] = self._clamp(blue)

        if white is not None:
            values["white"] = self._clamp(white)

        if gain is not None:
            values["gain"] = self._clamp_percentage(gain)

        if temp is not None:
            values["temp"] = self._clamp_kelvin(temp)

        if brightness is not None:
            values["brightness"] = self._clamp_percentage(brightness)

        return self.post(f"light/{index}", values)

    def emeter(self, index, *args, **kwargs):

        return self.post(f"emeter/{index}")

# backwards compatibility with old code
Shelly = ShellyGen1
