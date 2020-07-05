import json
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import requests
from dotenv import load_dotenv, find_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
LAST_FM_URL = os.environ["LAST_FM_URL"]
REQUEST_PARAMS = {
    "api_key": os.environ["LAST_FM_KEY"],
    "format": "json",
}


def get_collection(name: str):
    with (Path(__file__).parent / f"{name}.json").open("r") as file:
        collection = json.load(file)
    return collection


def request_last_fm(**kwargs) -> Dict:
    result = requests.get(LAST_FM_URL, params={**kwargs, **REQUEST_PARAMS})
    return result.json()


performers_cache = get_collection("performers_cache")


def get_corrected_performer(name: str) -> Optional[Dict]:
    result = performers_cache.get(name)
    if result is None:
        result = request_last_fm(method="artist.getcorrection", artist=name)
        print(name, result)
    corrections = result["corrections"]
    if isinstance(corrections, str):
        return None
    artist = corrections["correction"]["artist"]
    return {"name": artist["name"], "mbid": artist.get("mbid")}


def get_performers_indexes(performers: Dict[int, Dict]) -> Dict[int, List]:
    groups_by_mbid = defaultdict(list)
    for performer in performers.values():
        groups_by_mbid[performer["mbid"]].append(performer)
    return dict(((i, v) for i, v in enumerate(groups_by_mbid.values(), start=1)))


def get_performer_fixture(index: int, performer: Dict, user: int) -> Dict:
    return {
        "model": "reviews.performer",
        "pk": index,
        "fields": {
            "name": performer["name"],
            "mbid": performer["mbid"],
            "user": user,
            "created": str(datetime.now()),
            "last_updated": str(datetime.now()),
        },
    }


def build_performers(user: int) -> Tuple:
    performers = get_collection("performer")
    print("performers:", len(performers))
    corrected_performers = {
        performer["performer_id"]: {**performer, **corrected}
        for performer in performers
        for corrected in [get_corrected_performer(performer["name"])]
        if corrected is not None
    }
    performers_indexes = get_performers_indexes(corrected_performers)
    performers_fixture = [
        get_performer_fixture(index, grouped_performers[0], user)
        for index, grouped_performers in performers_indexes.items()
    ]
    performers_mapping = {
        performer["performer_id"]: (index, grouped_performers[0])
        for index, grouped_performers in performers_indexes.items()
        for performer in grouped_performers
    }
    return performers_fixture, performers_mapping


def get_corrected_album(title: str, name: str):
    result = request_last_fm(method="album.search", album=f"{name} {title}")
    albums = result["results"]["albummatches"]["album"]
    print(f'"{name}, {title}": {{{len(albums)}}},')
    if len(albums) == 0:
        print(f"|{name}, {title}|")
        return None
    album = albums[0]
    return {"name": album["name"], "mbid": album["mbid"]}


def get_corrected_albums(performers_mapping: Dict) -> Dict:
    albums = get_collection("album")
    print("albums:", len(albums))
    albums_performers = {
        album["album_id"]: (
            album,
            performers_mapping.get(album["performer_performer_id"]),
        )
        for album in albums
    }
    filtered_albums = {
        album_id: ap for album_id, ap in albums_performers.items() if ap[1] is not None
    }

    corrected_albums = {}
    for album_id, ap in filtered_albums.items():
        album, performer_tuple = ap
        if performer_tuple is not None:
            performer_index, performer = performer_tuple
            corrected = get_corrected_album(album["title"], performer["name"])
            if corrected is not None:
                corrected_albums[album_id] = {
                    **album,
                    "performer": performer_index,
                    **corrected,
                }
    return corrected_albums
    # return {
    #     album_id: {**album, "performer": performer_index, **corrected}
    #     for album_id, (album, (performer_index, performer)) in filtered_albums.items()
    #     for corrected in [get_corrected_album(album["title"], performer["name"])]
    #     if corrected is not None
    # }


def get_album_indexes(corrected_albums: Dict[int, Dict]):
    groups_by_mbid = defaultdict(list)
    for album in corrected_albums.values():
        groups_by_mbid[album["mbid"]].append(album)
    return dict(((i, v) for i, v in enumerate(groups_by_mbid.values(), start=1)))


def get_album_fixture(index: int, album: Dict, user: int) -> Dict:
    return {
        "model": "reviews.album",
        "pk": index,
        "fields": {
            "mbid": album["mbid"],
            "performer": album["performer"],
            "name": album["title"],
            "year": album["year"],
            "user": user,
            "created": str(datetime.now()),
            "last_updated": str(datetime.now()),
        },
    }


def build_albums(user: int, performers_mapping: Dict):
    corrected_albums = get_corrected_albums(performers_mapping)
    album_indexes = get_album_indexes(corrected_albums)
    albums_fixture = [
        get_album_fixture(index, grouped_albums[0], user)
        for index, grouped_albums in album_indexes.items()
    ]
    albums_mapping = {
        album["album_id"]: index
        for index, grouped_albums in album_indexes.items()
        for album in grouped_albums
    }
    return albums_fixture, albums_mapping


def get_review_fixture(index: int, review: Dict, user: int) -> Dict:
    return {
        "model": "reviews.review",
        "pk": index,
        "fields": {
            "album": review["album"],
            "user": user,
            "review": review["description"],
            "rating": review["rate"],
            "created": review["date"],
            "last_updated": review["date"],
        },
    }


def build_reviews(user: int, album_mapping: Dict) -> List:
    reviews = get_collection("rating")
    print("reviews:", len(reviews))
    reviews_album = (
        {**review, "album": album_mapping.get(review["album_album_id"])}
        for review in reviews
    )
    filtered_reviews = (
        review for review in reviews_album if review["album"] is not None
    )
    return [
        get_review_fixture(index, review, user)
        for index, review in enumerate(filtered_reviews, start=1)
    ]


def main():
    user = 1

    performers_fixture, performers_mapping = build_performers(user)
    albums_fixture, albums_mapping = build_albums(user, performers_mapping)
    reviews_fixture = build_reviews(user, albums_mapping)

    fixtures = performers_fixture + albums_fixture + reviews_fixture
    print(len(performers_fixture), len(albums_fixture), len(reviews_fixture))

    with (Path(__file__).parent / "fixture.json").open("w") as file:
        json.dump(fixtures, file, indent=4)


if __name__ == "__main__":
    main()
