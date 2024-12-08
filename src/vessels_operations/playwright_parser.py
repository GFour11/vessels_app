import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def parse_map_async(type,imo):
    """Function to intercept current coordinates and travel data"""
    url = f"https://www.vesselfinder.com/?{type}={imo}"
    result_dct = {"ETA_UTC": None, "Draught": None, "Deadweight": None, "Speed": None, "ATD_UTC": None,
                  "Latitude": None, "Longitude": None, "Course": None, "Destination": None, "Last-Port": None}

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
                locale="en-US"
            )
            page = await context.new_page()
            await page.goto(url)
    
            full_html = await page.content()
            await browser.close()
            soup = BeautifulSoup( full_html, 'html.parser')
            shipinfo_inner = soup.find('div', class_='shipinfo-inner')
            divs = [div for div in shipinfo_inner.find_all('div')][0]
            divs = [div for div in divs]
            try:
                destination = divs[0].find('div', class_='TaBtS enMy-').text
                eta_utc = divs[0].find_all('span')
                result_dct.update({"ETA_UTC": " ".join([i.text for i in eta_utc]), "Destination": destination})
            except:
                pass
            keeys = divs[1].find_all('div', class_='Hs6Sr')
            vals = divs[1].find_all('div', class_='TaBtS')
            try:
                dct = dict(zip([i.text for i in keeys], [i.text for i in vals]))
                last_port = divs[2].find('div', class_='TaBtS enMy-').text
                atd = divs[2].find_all('span')
                result_dct.update(
                    {"Draught": dct['Draught:'], "Speed": dct["Speed:"], "Course": dct["Course:"], "Last-Port":
                        last_port, "ATD_UTC": ' '.join([i.text for i in atd])})
            except:
                pass
            try:
                lat = soup.find_all('div', class_='coordinate lat')
                lon = soup.find_all('div', class_='coordinate lon')
                result_dct.update({"Latitude": "/".join([i.text for i in lat]),
                                   "Longitude": "/".join([i.text for i in lon])})
            except:
                pass
            try:
                divs2 = [div for div in shipinfo_inner.find_all('div')]
                position = 0
                for div in divs2:
                    if "Deadweight:" in div.text:
                        break
                    else:
                        position+=1
                dct2 = dict(zip([el.text for el in divs2[position].find_all('div', class_='Hs6Sr')],
                                [el.text for el in divs2[position].find_all('div', class_='TaBtS')]))
                result_dct.update({"Deadweight": dct2.get("Deadweight:")})
            except:
                pass
            return {"Status": 200, "detail": result_dct}
        except Exception as e:
            return {"Status": 400, "detail": e}


