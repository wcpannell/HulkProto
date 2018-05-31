#!/usr/bin/env python3
"""Higher Level class. inherits from rw_pkg_global.py"""

from .rw_pkg_global import PortUser


class ConfigDict(dict):
    """Special @property style setter work-around for dictionary keys

    Keep a copy in memory. Write to instrument when written to. Read from
    instrument when refresh method called. MUST be initialized when called
    """
    def __init__(self, instance, initialize):
        dict.__init__(self, **initialize)
        self.instance = instance
        # Removed because added requirement to initialize when called.
        # Leaving in, incase that ends up being a bad idea.
        # self['COMMONTHINGY'] = self.instance.query('CONF:COMMONTHINGY?')
        # if function == 'volt':
        #     self['range'] = self.instance.query('CONF:RANGE?')
        # elif function == 'amp':
        #     self['AMPTHINGY'] = self.instance.query('CONF:AMPTHINGY?')
        self.refresh()

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.instance.write(f'CONF:{key} {value}')

    def refresh(self):
        for key in self:
            self[key] = self.instance.query(f'CONF:{key}?')


class HigherLevel(PortUser):
    """High level wrapper over :class:`rw_pkg_global.PortUser`

    Parameters
    ----------
    port: str
        port the Instrument is on.

    Attributes
    ----------
    config dict
    """
    def __init__(self, port):
        super().__init__(port)
        self._id = ''
        self._v_config = ConfigDict(self, {'range': 100, 'AC_DC': 'DC'})

    @property
    def voltage(self):
        """Voltage measurements and configuration"""
        self._v_config.refresh()
        return self.query('MEAS:VOLTAGE:PLZ?')

    @property
    def id(self):
        """
        Self-reported ID of the instrument
        """
        return self.query('*IDN?')

    def beep(self):
        self.write('BEEP BEEP')
