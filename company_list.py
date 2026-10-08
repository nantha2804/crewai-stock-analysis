from pathlib import Path


COMPANY_FILE = Path(__file__).resolve().parent / "Companies _short names.txt"


def load_companies():
    companies = {}

    with COMPANY_FILE.open("r", encoding="utf-8") as file:
        next(file, None)  # Skip header

        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split()

            if len(parts) < 3:
                continue

            # Sector can contain spaces, so company/symbol are
            # extracted based on the known three-column structure.
            sector_start = None

            sectors = {
                "Energy", "Telecom", "IT", "Banking", "Engineering",
                "Automobile", "Steel", "Finance", "Conglomerate",
                "Infrastructure", "Pharma", "FMCG", "Paints",
                "Consumer", "Power", "Mining"
            }

            for index, value in enumerate(parts):
                if value in sectors:
                    sector_start = index
                    break

            if sector_start is None or sector_start < 2:
                continue

            symbol = parts[sector_start - 1]
            company_name = " ".join(parts[:sector_start - 1])

            companies[company_name] = {
                "symbol": symbol,
                "yahoo_symbol": f"{symbol}.NS",
                "sector": " ".join(parts[sector_start:]),
            }

    return companies


COMPANIES = load_companies()