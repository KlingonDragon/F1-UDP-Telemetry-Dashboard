from struct import unpack
class _header_:
    def __init__(self, bytes):
        [
            self.version,
            self.major_version,
            self.minor_version,
            self.packet_version,
            self.packet_type,
            self.uID,
            self.time,
            self.frame,
            self.player_car,
            self.coop_car
        ] = unpack('<HBBBBQfIBb', bytes)

    def __repr__(self):
        return 'Format: {}\n\tGame Version: {}.{}\n--------------------------'.format(
                self.version,self.major_version, self.minor_version
            )
class _zones_:
    def __init__(self, bytes):
        [self.zone_start, self._flag_] = unpack('<fb',bytes)
        try:
            self.flag = ['None','Green','Cyan','Yellow','Red'][self._flag_]
        except:
            self.flag = ''
    def __repr__(self):
        return self.flag
class _forecast_:
    def __init__(self, bytes):
        [
            self._session_,
            self.time_to_forcast,
            self._weather_,
            self.track_temp,
            self.track_temp_delta,
            self.air_temp,
            self.air_temp_delta,
            self.rain_pct
        ] = unpack('<BBBbbbbB',bytes)
        try:
            self.session = [
                'None','P1','P2','P3','P','Q1','Q2','Q3',
                'Q','Q','R','R2','Time Trial'
            ][self._session_]
        except: self.session = ''
        try:
            self.weather = [
                'Clear',
                'Light Cloud',
                'Overcast',
                'Light Rain',
                'Heavy Rain',
                'Storm',
                'Storm'
            ][self._weather_]
        except: self.weather = ''
    def __repr__(self):
        return '{} in {} mins'.format(self.weather, self.time_to_forcast)
class _session_:
    def __init__(self, bytes):
        [
            self._weather_,
            self.track_temp,
            self.air_temp,
            self.total_laps,
            self.track_length_m,
            self._session_,
            self.track_id,
            self.formula
        ] = unpack('<BbbBHBbB', bytes[:9])
        [
            self.ideal_pit_lap,
            self.late_pit_lap,
            self.pit_rejoin
        ] = unpack('<BBB', bytes[589:592])
        try:
            self.weather = [
                'Clear',
                'Light Cloud',
                'Overcast',
                'Light Rain',
                'Heavy Rain',
                'Storm',
                'Storm'
            ][self._weather_]
        except:
            self.weather = 'Clear'
        try:
            self.session = [
                'None','P1','P2','P3','P','Q1','Q2','Q3',
                'Q','Q','R','R2','R3','Time Trial'
            ][self._session_]
        except: self.session = ''
        self.zones = []
        for z in range(bytes[18]):
            self.zones.append(_zones_(bytes[19+(5*z):19+(5*(z+1))]))
        try:
            self.sc = ['None','Full','Virtual','Formation'][bytes[124]]
        except:
            self.sc = ''
        self.forecast = []
        for z in range(bytes[126]):
            self.forecast.append(_forecast_(bytes[127+(8*z):127+(8*(z+1))]))
    def __repr__(self):
        return 'Session: {}\nWeather: {}\n SC: {}\nFlags: {}\n\nPit Strategy:\n\tIdeal Lap: {}\n\tLatest Lap: {}\n\tRejoin Poition: {}'.format(
                self.session,
                self.weather,
                self.sc,
                self.zones,
                self.ideal_pit_lap,
                self.late_pit_lap,
                self.pit_rejoin
            )
class _car_status_data_:
    def __init__(self, bytes):
        [
            self.traction_control,
            self.anti_lock,
            self.fuel_mix,
            self.front_brake_bias,
            self.pit_limiter,
            self.fuel_left,
            self.max_fuel,
            self.fuel_laps,
            self.max_rpm,
            self.idle_rpm,
            self.max_gears,
            self.drs_allowed,
            self.drs_distance,
            self._tyre_compound_,
            self._visual_tyre_compound_,
            self.tyre_age,
            self._flags_,
            self.ers_store,
            self.ers_deploy,
            self.ers_mguk,
            self.ers_mguh,
            self.ers_this_lap,
            self.network_pause
        ] = unpack('<BBBBBfffhHBBHBBBbfBfffB', bytes)
        try:
            self.tyre_compound = [
                '','','','','','','','Intermediate',
                'Wet','Dry','Wet','Super Soft','Soft',
                'Medium','Hard','Wet','C5',
                'C4','C3','C2','C1'
            ][self._tyre_compound_]
        except:
            pass
        try:
            self.flags = [
                'None','Green','Blue','Yellow','Red'
            ][self._flags_]
        except:
            self.flags = 'Green'
    def __repr__(self):
        return '{} Flag - {} Tyre - {} ({}) Extra Laps of Fuel'.format(self.flags, self.tyre_compound, self.visual_tyre_compound, self.fuel_laps)
class _car_status_:
    def __init__(self, bytes):
        self.cars = []
        for i in range(22):
            if len(bytes[i*47:(i+1)*47]) == 47:
                self.cars.append(_car_status_data_(bytes[i*47:(i+1)*47]))
class _car_damage_data_:
    def __init__(self, bytes):
        [
            self.tyre_wear_bl,
            self.tyre_wear_br,
            self.tyre_wear_fl,
            self.tyre_wear_fr,
            self.tyre_damage_bl,
            self.tyre_damage_br,
            self.tyre_damage_fl,
            self.tyre_damage_fr,
            self.brake_damage_bl,
            self.brake_damage_br,
            self.brake_damage_fl,
            self.brake_damage_fr,
            self.wing_damage_fl,
            self.wing_damage_fr,
            self.wing_damage_rear,
            self.floor_damage,
            self.diffuser_damage,
            self.sidepod_damage,
            self.drs_fault,
            self.gear_box_damage,
            self.engine_damage,
            self.engine_wear_MGUH,
            self.engine_wear_ES,
            self.engine_wear_CE,
            self.engine_wear_ICE,
            self.engine_wear_MGUK,
            self.engine_wear_TC,
        ] = unpack('<ffffBBBBBBBBBBBBBBBBBBBBBBB', bytes)
        self.tyre_wear_list = [self.tyre_wear_fl, self.tyre_wear_fr, self.tyre_wear_bl, self.tyre_wear_br]
        self.tyre_damage_list = [self.tyre_damage_fl, self.tyre_damage_fr, self.tyre_damage_bl, self.tyre_damage_br]
        self.wing_damage_list = [self.wing_damage_fl, self.wing_damage_fr, self.wing_damage_rear]
    def __repr__(self):
        return '\n{:>3.1f}% 0-0 {:<3.1f}%\n      |\n{:>3.1f}% 0-0 {:<3.1f}%\n'.format(
            self.tyre_wear_fl, self.tyre_wear_fr, self.tyre_wear_bl, self.tyre_wear_br
        )
class _car_damage_:
    def __init__(self, bytes):
        self.cars = []
        for i in range(22):
            car_bytes = bytes[i*39:(i+1)*39]
            if len(car_bytes) == 39:
                self.cars.append(_car_damage_data_(car_bytes))
class _penalty_:
    def __init__(self, bytes):
        [
            self._type_,
            self._infringement_,
            self.car,
            self.other_car,
            self.time,
            self.lap,
            self.places_gained,
            self.grid_penalty
        ] = unpack('<BBBbbBbB', bytes)
        try:
            self.type = [
                'Drive Through Penalty',
                'Stop Go Penalty',
                'Grid Penalty',
                'Reminder',
                'Time Penalty',
                'Warning',
                'Disqualified',
                'Removed from Formation Lap',
                'Parked too Long Timer',
                'Tyre regulations',
                'Invalidated Lap',
                'Invalidated Lap',
                'Invalidated Lap',
                'Invalidated Lap',
                'Invalidated Lap',
                'Invalidated Lap',
                'Retired',
                'Black Flag Timer'
            ][self._type_]
        except:
            self.type = self._type_
        try:
            self.infringement = [
                'Blocking by slow driving',
                'Blocking by wrong way driving',
                'Reversing off the start line',
                'Big Collision',
                'Small Collision',
                'Failed to hand back position',
                'Failed to hand back positions',
                'Corner cutting gained time',
                'Corner cutting overtaking',
                'Corner cutting overtaking',
                'Crossed pit exit lane',
                'Ignoring blue flags',
                'Ignoring yellow flags',
                'Ignoring drive through',
                'Too many drive throughs',
                'Drive through reminder serve within n laps',
                'Drive through reminder serve this lap',
                'Pit lane speeding',
                'Parked for too long',
                'Ignoring tyre regulations',
                'Too many penalties',
                'Multiple warnings',
                'Approaching disqualification',
                'Tyre regulations select single',
                'Tyre regulations select multiple',
                'Lap invalidated corner cutting',
                'Lap invalidated running wide',
                'Corner cutting ran wide gained time minor',
                'Corner cutting ran wide gained time significant',
                'Corner cutting ran wide gained time extreme',
                'Lap invalidated wall riding',
                'Lap invalidated flashback used',
                'Lap invalidated reset to track',
                'Blocking the pitlane',
                'Jump start',
                'Safety car to car collision',
                'Safety car illegal overtake',
                'Safety car exceeding allowed pace',
                'Virtual safety car exceeding allowed pace',
                'Formation lap below allowed speed',
                'Retired mechanical failure',
                'Retired terminally damaged',
                'Safety car falling too far back',
                'Black flag timer',
                'Unserved stop go penalty',
                'Unserved drive through penalty',
                'Engine component change',
                'Gearbox change',
                'League grid penalty',
                'Retry penalty',
                'Illegal time gain',
                'Mandatory pitstop'
            ][self._infringement_]
        except:
            self.infringement = self._infringement_
    def __repr__(self):
        return 'Car {} - {} ({}) {}\nLap {} - {} - Gained {} places\n extra byte? {}'.format(
            self.car,self.type,self.infringement,('on car {}'.format(self.other_car) if self.other_car>0 else ''),self.lap,
            ('{}s Penalty'.format(self.time) if self.time>0 else 'Warning')
            , self.places_gained, self.grid_penalty
        )
class _speed_trap_:
    def __init__(self, bytes):
        [
            self.car,
            self.speed,
            self.session_fastest,
            self.fastest_driver
        ] = unpack('<BfBB', bytes[:7])
    def __repr__(self):
        return 'Speed Trap\nCar {} - {:.0f}kph{}'.format(
            self.car,self.speed,(' Fastest Speed in Session' if self.session_fastest else '')
        )
class _event_:
    def __init__(self, bytes):
        self.type = str(bytes[:4], 'UTF-8')
        if self.type == 'PENA':
            self.penalty = _penalty_(bytes[4:])
        if self.type == 'SPTP':
            self.speed_trap = _speed_trap_(bytes[4:])
    def __repr__(self):
        return '{}'.format(self.type)
class _participant_:
    def __init__(self, bytes):
        [
            self.ai,
            self.driver_id,
            self.network_id,
            self.team_id,
            self.my_team,
            self.race_number,
            self.nationality
        ] = unpack('<BBBBBBB', bytes[:7])
        self.driver_name = str(bytes[7:56], 'UTF-8').split('\0', 1)[0]
    def __repr__(self):
        return '{} - {}'.format(self.race_number, self.driver_name)
class _participants_:
    def __init__(self, bytes):
        self.cars = []
        for i in range(22):
            car_bytes = bytes[1+i*56:(i+1)*56]
            if len(car_bytes) >= 7:
                self.cars.append(_participant_(car_bytes))
class _car_telemetry_:
    def __init__(self, bytes):
        [
            self.speed,
            self.throttle,
            self.steering,
            self.brake,
            self.clutch,
            self.gear,
            self.rpm,
            self.drs,
            self.rev_light_percent,
            self.rev_light_index,
            self.brake_temp_bl,
            self.brake_temp_br,
            self.brake_temp_fl,
            self.brake_temp_fr,
            self.tyre_surface_temp_bl,
            self.tyre_surface_temp_br,
            self.tyre_surface_temp_fl,
            self.tyre_surface_temp_fr,
            self.tyre_core_temp_bl,
            self.tyre_core_temp_br,
            self.tyre_core_temp_fl,
            self.tyre_core_temp_fr,
            self.engine_temp,
            self.tyre_pressure_bl,
            self.tyre_pressure_br,
            self.tyre_pressure_fl,
            self.tyre_pressure_fr,
            self.track_surface_bl,
            self.track_surface_br,
            self.track_surface_fl,
            self.track_surface_fr
        ] = unpack('<HfffBbHBBH4H4B4BH4f4B', bytes)
        self.brake_temp_list = [self.brake_temp_fl, self.brake_temp_fr, self.brake_temp_bl, self.brake_temp_br]
        self.tyre_surface_temp_list = [self.tyre_surface_temp_fl, self.tyre_surface_temp_fr, self.tyre_surface_temp_bl, self.tyre_surface_temp_br]
        self.tyre_core_temp_list = [self.tyre_core_temp_fl, self.tyre_core_temp_fr, self.tyre_core_temp_bl, self.tyre_core_temp_br]
        self.tyre_pressure_list = [self.tyre_pressure_fl, self.tyre_pressure_fr, self.tyre_pressure_bl, self.tyre_pressure_br]
        self.track_surface_list = [self.track_surface_fl, self.track_surface_fr, self.track_surface_bl, self.track_surface_br]
    def __repr__(self):
        return '{}kph'.format(self.speed)
class _telemetry_:
    def __init__(self, bytes):
        self.cars = []
        for i in range(22):
            car_bytes = bytes[i*60:(i+1)*60]
            if len(car_bytes) == 60:
                self.cars.append(_car_telemetry_(car_bytes))
class packet:
    def __init__(self, bytes):
        self.header = _header_(bytes[:24])
        if self.header.packet_type == 0:
            self.type = 'Motion'
            self.body = 'Motion'
        if self.header.packet_type == 1:
            self.type = 'Session'
            self.body = _session_(bytes[24:])
        if self.header.packet_type == 2:
            self.type = 'Lap Data'
            self.body = 'Lap Data'
        if self.header.packet_type == 3:
            self.type = 'Event'
            self.body = _event_(bytes[24:])
        if self.header.packet_type == 4:
            self.type = 'Participants'
            self.body = _participants_(bytes[24:])
        if self.header.packet_type == 5:
            self.type = 'Car Setup'
            self.body = 'Car Setup'
        if self.header.packet_type == 6:
            self.type = 'Car Telemetry'
            self.body = _telemetry_(bytes[24:])
        if self.header.packet_type == 7:
            self.type = 'Car Status'
            self.body = _car_status_(bytes[24:])
        if self.header.packet_type == 8:
            self.type = 'Final'
            self.body = 'Final'
        if self.header.packet_type == 9:
            self.type = 'Lobby'
            self.body = 'Lobby'
        if self.header.packet_type == 10:
            self.type = 'Car Damage'
            self.body = _car_damage_(bytes[24:])
        if self.header.packet_type == 11:
            self.type = 'History'
            self.body = 'History'
    def __repr__(self):
        return '{}'.format(self.header)