from miio import CloudInterface, ChuangmiPlug
from miio.cloud import CloudDeviceInfo


class MiCloud(CloudInterface):
    def __init__(self, username: str, password: str):
        super().__init__(
            username=username,
            password=password
        )

        self.__username = username
        self.__password = password

    def get_smart_plug(self, smart_plug_id: str) -> ChuangmiPlug:
        devices = self.get_devices()

        try:
            smart_plug_info: CloudDeviceInfo = devices[smart_plug_id]
        except KeyError:
            raise KeyError(
                f'The device with id {smart_plug_id} could not be found in your devices. '
                f'Available devices are: {list(devices.keys())}. If not sure about your device, please '
                f'refer to this library (https://github.com/rytilahti/python-miio/tree/master) and use CLI '
                f'to list all your devices.'
            )

        return ChuangmiPlug(
            ip=smart_plug_info.ip,
            token=smart_plug_info.token
        )
