import aiohttp
import asyncio
import pycountry
from bs4 import BeautifulSoup


async def parse_from_mmsi(mmsi_number: str) -> dict:
    """Basic function for initial parsing of ship information.
     Used only when this information is not available in the database.
     params:
     mmsi_number = str, number of ship mmsi.

     Return data in dict."""

    url = f"https://www.vesselfinder.com/vessels/details/{mmsi_number}"

    result_dct={"Name": None, "MMSI": None, "IMO": None, "Country-ISO": None,
            "Country": None, "Type": None, "Type-specific": None,
            "Navigational-status": None, "Callsign": None, "Gross-tonnage": None,
            "TEU": None, "Length": None, "Beam": None, "Year-of-built": None, "Current-draught": None,
            "ENI": None, "Image": None}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=20) as resp:
                if resp.status == 200:
                    response = await resp.text()
                    soup = BeautifulSoup(response, 'html.parser')
                    try:
                        image = soup.find('a', class_='img-holder s0')
                        if image:
                            img = image.find('img').get('src')
                            result_dct.update({"Image": img})
                    except Exception:
                        pass
                    country_name = soup.find('div', class_='title-flag-icon').get('title')
                    result_dct.update({"Country": country_name})
                    ship_name = soup.find('h1', class_='title').text
                    result_dct.update({"Name": ship_name})
                    type_and_imo = soup.find('h2', class_='vst').text
                    ship_type = type_and_imo.split(',')[0].strip()
                    result_dct.update({"Type-specific": ship_type})
                    first_table_data = soup.find('table', class_='aparams')
                    trs = first_table_data.find_all('tr')
                    for tds in trs:
                        if "Current draught" in tds.find('td', class_='n3').text:
                            result_dct.update({"Current-draught": tds.find('td', class_='v3').text})
                        if "IMO / MMSI" in tds.find('td', class_='n3').text:
                            result_dct.update({"IMO": tds.find('td', class_='v3').text.split('/')[0].strip()})
                            result_dct.update({"MMSI": tds.find('td', class_='v3').text.split('/')[1].strip()})
                        if "ENI / MMSI" in tds.find('td', class_='n3').text:
                            result_dct.update({"ENI": tds.find('td', class_='v3').text.split('/')[0].strip()})
                            result_dct.update({"MMSI": tds.find('td', class_='v3').text.split('/')[1].strip()})
                        if "Callsign" in tds.find('td', class_='n3').text:
                            result_dct.update({"Callsign": tds.find('td', class_='v3').text})
                        if "Length / Beam" in tds.find('td', class_='n3').text:
                            result_dct.update({"Length": f"{tds.find('td', class_='v3').text.split('/')[0].strip()} m"})
                            result_dct.update({"Beam": tds.find('td', class_='v3').text.split('/')[1].strip()})
                        if "Navigation Status" in tds.find('td', class_='n3').text:
                            result_dct.update({"Navigational-status": tds.find('td', class_='v3').text.strip()})
                    tables_tpt1 = soup.find_all('table', class_='tpt1')
                    if tables_tpt1:
                        for table in tables_tpt1:
                                for tr in table.find_all('tr'):
                                    t_tr = tr.find('td', class_="tpc1")
                                    if t_tr:
                                        try:
                                            if "Year of Build" in t_tr.text:
                                                result_dct.update({"Year-of-built": tr.find('td', class_='tpc2').text.strip()})
                                        except Exception:
                                            pass
                                        try:
                                            if "Gross Tonnage" in t_tr.text:
                                                result_dct.update({"Gross-tonnage": tr.find('td', class_='tpc2').text.strip()})
                                        except Exception:
                                            pass
                                        try:
                                            if "TEU" in t_tr.text:
                                                result_dct.update({"TEU": tr.find('td', class_='tpc2').text.strip()})
                                        except Exception:
                                            pass
                    type_ship = soup.find_all('span', {"itemprop": "name"})
                    if len(type_ship)>=3:
                        type_ship = type_ship[2].text.strip()
                        result_dct.update({"Type":type_ship})
                    try:
                        iso_format = pycountry.countries.get(name=result_dct.get("Country"))
                        result_dct.update({"Country-ISO": iso_format.alpha_2})
                    except:
                        pass
                    return {"status code": 200, "detail": result_dct}
                else:
                    return {"status code": 404, "detail": "Can not find information about ship."}
    except asyncio.TimeoutError:
        return {"Status":resp.status, "detail": resp.json()}



