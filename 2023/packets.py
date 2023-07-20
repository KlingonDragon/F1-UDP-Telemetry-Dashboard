from struct import unpack
class PacketData():
    def __init__(self, bytes):
        self.header = self.PacketHeader(bytes[:29])
        match self.header.packet_id:
            case 1:
                self.body = self.PacketSessionData(bytes[29:])
            case 2:
                self.body = self.PacketLapData(bytes[29:])
            case 3:
                pass
            case 4:
                pass
            case 6:
                pass
            case 7:
                pass
            case 10:
                pass
            case 11:
                pass
            case 12:
                pass
            case _:
                # 0 motion
                # 2 Lap data
                # 5 Setup Data
                # 8 Final Classification
                # 9 Lobby Info
                # 13 Extended Motion Data
                pass
    class PacketHeader():
        def __init__(self, bytes):
            [
                self.packet_format,
                self.game_year,
                self.game_major_version,
                self.game_minor_version,
                self.packet_version,
                self.packet_id,
                self.session_uid,
                self.session_time,
                self.frame_identifier,
                self.overall_frame_identifier,
                self.player_car_index,
                self.secondary_player_car_index
            ] = unpack('<HBBBBBQfIIBB', bytes)
    class PacketSessionData():
        def __init__(self, bytes):
            [
                self.weather,
                self.track_temperature,
                self.air_temperature,
                self.total_laps,
                self.track_length,
                self.session_type,
                self.track_id,
                self.formula,
                self.session_time_left,
                self.session_duration,
                self.pit_speed_limit,
                self.game_paused,
                self.is_spectating,
                self.spectator_car_index,
                self.sli_pro_native_support,
                self.num_marshal_zones
            ] = unpack('<BbbBHBbBHHBBBBBB', bytes[:19])
            start = 19
            self.marshal_zones = [self.MarshalZone(x, bytes[start+(5*x):start+(5*x)+5]) for x in range(self.num_marshal_zones)]
            start += (5*self.num_marshal_zones)+5
            [
                self.safety_car_status,
                self.network_game,
                self.num_weather_forcast_samples
            ] = unpack('<BBB', bytes[start:start+3])
            start += 3
            self.weather_forcast_samples = [self.WeatherForcastSample(bytes[start+(8*x):start+(8*x)+8]) for x in range(self.num_weather_forcast_samples)]
            start += (8*self.num_weather_forcast_samples)+8
            [
                self.forecast_accuracy,
                self.ai_difficulty,
                self.season_link_identifier,
                self.weekend_link_identifier,
                self.session_link_identifier,
                self.pit_stop_window_ideal_lap,
                self.pit_stop_window_latest_lap,
                self.pit_stop_rejoin_position,
                self.steering_assist,
                self.braking_assist,
                self.gearbox_assist,
                self.pit_assist,
                self.pit_release_assist,
                self.ers_assist,
                self.drs_assist,
                self.dynamic_racing_line,
                self.dynamic_racing_line_type,
                self.game_mode,
                self.ruleset,
                self.time_of_day,
                self.session_length,
                self.speed_units_lead_player,
                self.temperature_units_lead_player,
                self.speed_units_secondary_player,
                self.temperature_units_secondary_player,
                self.num_safety_car_periods,
                self.num_virtual_safety_car_periods,
                self.num_red_flag_periods
            ] = unpack('<BBIIIBBBBBBBBBBBBBBIBBBBBBBB', bytes[start:start+40])
            
        class MarshalZone():
            def __init__(self, x, bytes):
                self.zone_number = x
                [
                    self.zone_start,
                    self.zone_flag
                ] = unpack('<fb', bytes)
            def __repr__(self) -> str:
                return  '<MarshalZone {}: {}>'.format(self.zone_number,
                    self.zone_flag)
        class WeatherForcastSample():
            def __init__(self, bytes):
                [
                    self.session_type,
                    self.time_offset,
                    self.weather,
                    self.track_temperature,
                    self.track_temperature_change,
                    self.air_temperature,
                    self.air_temperature_change,
                    self.rain_percentage
                ] = unpack('<BBBbbbbB', bytes)
    class PacketLapData():
        def __init__(self, bytes):
            [] = unpack('<', bytes)
        class LapData():
            def __init__(self, bytes):
                [] = unpack('<', bytes)
