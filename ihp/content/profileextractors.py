"""Profile extractor utilities for social account providers"""

import pycountry

from geonode.people.profileextractors import BaseExtractor


class LinkedInExtractor(BaseExtractor):

    def extract_city(self, data):
        return data.get("location", {}).get("name", "")

    def extract_country(self, data):
        code = data.get("location", {}).get("country", {}).get("code")
        try:
            country = pycountry.countries.get(alpha_2=code.upper())
            result = country.alpha_3
        except KeyError:
            result = ""
        return result

    def extract_email(self, data):
        return data.get("emailAddress", "")

    def extract_first_name(self, data):
        return data.get("firstName", "")

    def extract_last_name(self, data):
        return data.get("lastName", "")

    def extract_position(self, data):
        latest = _get_latest_position(data)
        return latest.get("title", "") if latest is not None else ""

    def extract_organization(self, data):
        organization = _get_latest_company(data)
        return organization.get("name", "") if organization is not None else ""

    def extract_profile(self, data):
        headline = data.get("headline", "")
        summary = data.get("summary", "")
        profile = "\n".join((headline, summary))
        return profile.strip()


def _get_latest_company(data):
    latest = _get_latest_position(data)
    return latest.get("company", {}) if latest is not None else {}


def _get_latest_position(data):
    all_positions = data.get(
        "positions",
        {"values": []}
    )["values"]
    return all_positions[0] if any(all_positions) else None
