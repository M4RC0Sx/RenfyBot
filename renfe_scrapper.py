import requests
import datetime


# RENFE URL to get information.
SERVICE_URL = 'https://horarios.renfe.com/cer/HorariosServlet'

# Arrival final hour, use 26 for every hour.
ALL_HOUR = 26


def get_renfe_data(origin, target, date=datetime.datetime.now(), hour=datetime.datetime.now()):

    try:
        date_str = date.strftime("%Y%m%d")
        hour_str = hour.strftime("%H")
        hour__min_str = hour.strftime("%H:%M")

        # Populate params dictionary.
        params = {
            "nucleo": 10,
            "origen": origin,
            "destino": target,
            "fchaViaje": date_str,
            "validaReglaNegocio": True,
            "tiempoReal": True,
            "servicioHorarios": "VTI",
            "horaViajeOrigen": hour_str,
            "horaViajeLlegada": ALL_HOUR,
            "accesibilidadTrenes": True
        }

        # Post request and collect JSON response content.
        r = requests.post(SERVICE_URL, json=params)
        renfe_data = r.json()["horario"]
        if len(renfe_data) <= 0:
            return {} 

        # Only get next trains.
        for i in range(0, len(renfe_data)):
            if datetime.datetime.strptime(renfe_data[i]['horaSalida'], '%H:%M').time() < datetime.datetime.strptime(hour__min_str, '%H:%M').time():
                del(renfe_data[i])
    except Exception:
        # Empty dictionary on exception.
        renfe_data = {}

    # Return timetable data.
    return renfe_data
