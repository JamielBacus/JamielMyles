# src/scraper.py
from bs4 import BeautifulSoup
import pandas as pd

def run_scraper():
    """
    Simulates or performs web scraping of the Steam Market price table.
    Returns a pandas DataFrame of the raw data.
    """
    # Simulated HTML structure based on the market snapshot
    html_content = """
    <table>
        <caption>Counter Strike 2 | AWP - Atheris Skin prices via Steam Market</caption>
        <tr>
            <th></th><th>2019</th><th>2020</th><th>2021</th><th>2022</th><th>2023</th><th>2024</th><th>2025</th><th>2026</th>
        </tr>
        <tr>
            <td>Factory New</td><td>1033.2</td><td>778.46</td><td>750.84</td><td>757.54</td><td>846.13</td><td>1015.79</td><td>1120.55</td><td>4339.02</td>
        </tr>
        <tr>
            <td>Minimal Wear</td><td>521.17</td><td>378.46</td><td>340.58</td><td>350.59</td><td>370.3</td><td>446.96</td><td>498.06</td><td>697.55</td>
        </tr>
        <tr>
            <td>Field-Tested</td><td>293.2</td><td>226.31</td><td>189.41</td><td>175.48</td><td>203.43</td><td>235</td><td>284.79</td><td>414.11</td>
        </tr>
        <tr>
            <td>Well-Worn</td><td>239.51</td><td>182.13</td><td>159.32</td><td>132.45</td><td>154.14</td><td>169.51</td><td>238.39</td><td>360.52</td>
        </tr>
        <tr>
            <td>Battle-Scarred</td><td>200.39</td><td>152.97</td><td>138.37</td><td>124.01</td><td>137.6</td><td>153.33</td><td>228.26</td><td>332.67</td>
        </tr>
    </table>
    """
    
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    
    # Extract headers and handle the empty structural corner cell
    headers = [th.text.strip() for th in table.find_all('th')]
    headers[0] = "Condition"
    
    rows = []
    for tr in table.find_all('tr')[1:]:
        cells = [td.text.strip() for td in tr.find_all('td')]
        if cells:
            rows.append(cells)
            
    raw_df = pd.DataFrame(rows, columns=headers)
    return raw_df
