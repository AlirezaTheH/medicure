from typing import Any, Dict

from tests.parameterize import movie_imdb_id, tvshow_imdb_id


class FindMock:
    def __init__(self, id: str) -> None:
        self.id = id

    def info(self, external_source: str) -> Dict[str, Any]:
        result = {
            movie_imdb_id: {
                'movie_results': [
                    {'title': 'The Batman', 'release_date': '2022-03-01'}
                ],
                'tv_results': [],
            },
            tvshow_imdb_id: {
                'movie_results': [],
                'tv_results': [{'name': 'Peaky Blinders', 'id': 60574}],
            },
        }
        return result[self.id]


class TVSeasonsMock:
    def __init__(self, tv_id, season_number):
        self.tv_id = tv_id
        self.season_number = season_number

    def info(self) -> Dict[str, Any]:
        result = {
            60574: {
                season_number: {
                    'name': f'Series {season_number}',
                    'episodes': [
                        {'episode_number': i + 1, 'name': name}
                        for i, name in enumerate(episode_names)
                    ],
                }
                for season_number, episode_names in {
                    4: [
                        'The Noose',
                        'Heathens',
                        'Blackbird',
                        'Dangerous',
                        'The Duel',
                        'The Company',
                    ],
                    5: [
                        'Black Tuesday',
                        'Black Cats',
                        'Strategy',
                        'The Loop',
                        'The Shock',
                        'Mr Jones',
                    ],
                    6: [
                        'Black Day',
                        'Black Shirt',
                        'Gold',
                        'Sapphire',
                        'The Road to Hell',
                        'Lock and Key',
                    ],
                }.items()
            }
        }
        return result[self.tv_id][self.season_number]
