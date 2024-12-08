from src.vessels_operations.parsers import parse_from_mmsi
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.models import  Vessel
from src.vessels_operations.playwright_parser import parse_map_async


async def get_or_create_vessel(imo_or_mmsi: str, db: AsyncSession) -> Vessel:

    result = await db.execute(select(Vessel).where(Vessel.imo == imo_or_mmsi))
    vessel = result.scalars().first()
    result2 = await db.execute(select(Vessel).where(Vessel.mmsi == imo_or_mmsi))
    vessel2 = result2.scalars().first()

    if vessel:
        if vessel.update_time and vessel.update_time >= datetime.utcnow() - timedelta(hours=5):
            return vessel
    elif vessel2:
        if vessel2.update_time and vessel2.update_time >= datetime.utcnow() - timedelta(hours=5):
            return vessel2
    else:
        parse_global_ship_info = await parse_from_mmsi(imo_or_mmsi)
        if type(parse_global_ship_info.get('detail')) is dict:
            detail = parse_global_ship_info.get('detail').get("IMO")
            if detail:
                data_global = parse_global_ship_info.get('detail')
                dynamic_data = await parse_map_async('imo',detail)
                if type(dynamic_data.get('detail')) is dict:
                    dyn_data = dynamic_data.get('detail')
                    new_vessel = Vessel(name=data_global.get('Name'),
                                        mmsi=data_global.get('MMSI'),
                                        imo=data_global.get('IMO'),
                                        country_iso=data_global.get('Country-ISO'),
                                        country_name=data_global.get('Country-name'),
                                        ship_type=data_global.get('Type'),
                                        type_specific=data_global.get('Type-specific'),
                                        navigational_status=data_global.get('Navigational-status'),
                                        callsign=data_global.get('Callsign'),
                                        gross_tonnage=data_global.get('Gross-tonnage'),
                                        teu=data_global.get('TEU'),
                                        length= data_global.get('Length'),
                                        beam = data_global.get('Beam'),
                                        year_of_built = data_global.get('Year-of-built'),
                                        current_draught = data_global.get('Current-draught'),
                                        gas_m3=data_global.get('Current-draught'),
                                        eni=data_global.get('Current-draught'),
                                        image=data_global.get('Current-draught'),
                                        eta_utc=dyn_data.get('ETA_UTC'),
                                        draught = dyn_data.get('Draught'),
                                        deadweight = dyn_data.get('Deadweight'),
                                        speed = dyn_data.get('Speed'),
                                        atd_utc = dyn_data.get('ATD_UTC'),
                                        latitude = dyn_data.get('Latitude'),
                                        longitude = dyn_data.get('Longitude'),
                                        course = dyn_data.get('Course'),
                                        destination = dyn_data.get('Destination'),
                                        last_port=dyn_data.get('Last-Port'),
                                        update_time=datetime.utcnow()
                                   )
                    db.add(new_vessel)
                    await db.commit()
                    await db.refresh(new_vessel)

                    return new_vessel
            else:
                detail = parse_global_ship_info.get('detail').get("MMSI")
                data_global = parse_global_ship_info.get('detail')
                dynamic_data = await parse_map_async('mmsi', detail)
                if type(dynamic_data.get('detail')) is dict:
                    dyn_data = dynamic_data.get('detail')
                    new_vessel = Vessel(name=data_global.get('Name'),
                                        mmsi=data_global.get('MMSI'),
                                        imo=data_global.get('IMO'),
                                        country_iso=data_global.get('Country-ISO'),
                                        country_name=data_global.get('Country-name'),
                                        ship_type=data_global.get('Type'),
                                        type_specific=data_global.get('Type-specific'),
                                        navigational_status=data_global.get('Navigational-status'),
                                        callsign=data_global.get('Callsign'),
                                        gross_tonnage=data_global.get('Gross-tonnage'),
                                        teu=data_global.get('TEU'),
                                        length= data_global.get('Length'),
                                        beam = data_global.get('Beam'),
                                        year_of_built = data_global.get('Year-of-built'),
                                        current_draught = data_global.get('Current-draught'),
                                        gas_m3=data_global.get('Current-draught'),
                                        eni=data_global.get('Current-draught'),
                                        image=data_global.get('Current-draught'),
                                        eta_utc=dyn_data.get('ETA_UTC'),
                                        draught = dyn_data.get('Draught'),
                                        deadweight = dyn_data.get('Deadweight'),
                                        speed = dyn_data.get('Speed'),
                                        atd_utc = dyn_data.get('ATD_UTC'),
                                        latitude = dyn_data.get('Latitude'),
                                        longitude = dyn_data.get('Longitude'),
                                        course = dyn_data.get('Course'),
                                        destination = dyn_data.get('Destination'),
                                        last_port=dyn_data.get('Last-Port'),
                                        update_time=datetime.utcnow()
                                   )

                    db.add(new_vessel)
                    await db.commit()
                    await db.refresh(new_vessel)

                    return new_vessel