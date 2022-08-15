import socket, app, packets as f1
from awake import awake as alive
from sys import argv as cli_options, exit as close
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 0))
    ip = s.getsockname()[0]
    s.close()
    return ip
def main(port):
    this_ip = get_ip()
    print('Initialising\n--------------------------')
    print('Launching graphical interface')
    win = app.window()
    win.host(this_ip, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    sock.settimeout(0.5)
    awake = alive()
    win.terminal('Keeping screen awake')
    win.terminal('UDP Listening on {}:{}'.format(this_ip, port))
    while win.active:
        win.update()
        try:b_data, addr = sock.recvfrom(1347)
        except:continue
        if not win.active:
            break
        win.host(this_ip,port,addr)
        p = f1.packet(b_data)
        data = p.body
        win.version_info(p.header.version, p.header.major_version, p.header.minor_version)
        my_car = p.header.player_car
        co_car = p.header.coop_car
        if co_car > 0:
            print(co_car)
        if p.type == 'Participants':
            win.driver_list(data.cars)
        if p.type == 'Session':
            win.session(data.session)
            win.safety_car(data.sc)
            win.pit_info(data.ideal_pit_lap, data.late_pit_lap, data.pit_rejoin)
            win.weather_info(data.weather, data.forecast)
        if p.type == 'Car Status':
            win.flag(data.cars[my_car].flags)
            win.extra_fuel(data.cars[my_car].fuel_laps)
            win.tyre_compound(data.cars[my_car].tyre_compound)
        if p.type == 'Car Damage':
            win.damage(data.cars[my_car].tyre_damage_list, data.cars[my_car].wing_damage_list)
        if p.type == 'Car Telemetry':
            win.tyre_temp(data.cars[my_car].tyre_core_temp_list)
        if p.type == 'Final':
            win.reset()
        if p.type == 'Event':
            if data.type == 'PENA':
                win.penalty(data.penalty)
                if data.penalty.car == my_car and data.penalty.type == 'Disqualified':
                    win.flag('DSQ')
            elif data.type == 'SPTP':
                if data.speed_trap.session_fastest:
                    win.speed_trap(data.speed_trap)
            elif data.type == 'SSTA':#'SEND':
                win.reset()
            elif data.type == 'CHQF':
                win.flag('CHQF')
            elif data.type != 'BUTN':
                win.terminal(data.type)
    print('Graphical interface closed')
    awake.stop()
    print('No longer keeping screen awake')
    sock.close()
    print('No longer listening on UDP')
    close()

if __name__ == "__main__":
    main(cli_options[1] if len(cli_options) >=2 else 20777)