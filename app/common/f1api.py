from lxml import html
import requests
import logging

logger = logging.getLogger(__name__)


class F1Scraper:
    def __init__(self):
        self._driver_stat_url = (
            "https://www.formula1.com/en/results.html/2025/drivers.html"
        )
        self._team_stat_url = "https://www.formula1.com/en/results/2025/team"

    @staticmethod
    def _scrape_f1(url: str, key: str) -> dict:
        page = requests.get(url)
        tree = html.fromstring(page.content)

        tables = tree.cssselect("table")

        for table in tables:
            headers = [
                header.text_content().strip().lower()
                for header in table.cssselect("th")
            ]
            if key in headers and "pos" in headers and "pts" in headers:
                table_rows = table.cssselect("tr")
                break
        else:
            logger.error(
                "No matching table found. The structure of the website might have changed."
            )
            return {"data": []}

        column_headers = [
            column.text_content().strip() for column in table_rows[0].cssselect("th")
        ]

        data_rows = []
        for row in table_rows[1:]:
            data = [column.text_content().strip() for column in row.cssselect("td")]
            data_dict = dict(zip(column_headers, data))
            if key.capitalize() in data_dict:
                data_dict[key.capitalize()] = data_dict[key.capitalize()].replace(
                    "\xa0", " "
                )
            data_rows.append(data_dict)

        return {"data": data_rows}

    def get_driver_data(self) -> dict:
        return self._scrape_f1(self._driver_stat_url, "driver")

    def get_team_data(self) -> dict:
        return self._scrape_f1(self._team_stat_url, "team")
