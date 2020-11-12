"""
Нужно реализовать два метода:
    - get_all_playlists() - возвращает все плейлисты в промежуточном формате
    - synchronize() который принимает плейлисты в промежуточном формате и их синхронизирует
        (добавляет недостающие песни, создаёт плейлист если нет и т. д. и т. п.)
        В общем конечная цель этого метода, чтобы в принимающем сервисе были все такие же плейлисты как в исходном
"""

from yandex_music import Client, Playlist


def __get_tracks_from_playlist__(_client: Client, _playlist: Playlist) -> list:
    """ Для клиента и плейлиста возвращает список треков в формате "Название - Исполнитель" """

    kind = _playlist['kind']
    uid = _playlist['uid']

    # информация по каждому треку
    tracks_info = _client.users_playlists(kind=kind, user_id=uid)[0]['tracks']

    # нужная информация по каждому треку
    tracks_ids = [(track['id'], track['album_id']) for track in tracks_info]

    tracks = list()
    for tracks_id in tracks_ids:
        # достаём трек по id и album_id
        info = client.tracks(['{}:{}'.format(tracks_id[0], tracks_id[1])])

        # добавляем в результирующий список название трека и исполнителя
        tracks.append('{} - {}'.format(info[0]['title'], info[0]['artists'][0]['name']))
    return tracks


def get_all_playlists(client: Client) -> list:
    """ Возвращает все плейлисты в промежуточном формате """

    info_about_playlists = list()
    client_playlists = client.users_playlists_list()
    for i, playlist in enumerate(client_playlists):

        tracks = __get_tracks_from_playlist__(_client=client, _playlist=playlist)

        info_about_playlists.append(
            {
                'index': i,                     # порядковый номер
                'uid': playlist['uid'],         # id владельца
                'kind': playlist['kind'],       # id плейлиста
                'title': playlist['title'],     # название
                'track_count': playlist['track_count'],  # количество треков
                'tracks': tracks                # список треков "название - исполнитель"
            }
        )
    return info_about_playlists


def synchronize(playlist1: list, playlist2: list) -> list:
    """ Синхронизирует плейлисты """

    return list(set(playlist1).union(set(playlist2)))


if __name__ == '__main__':
    file = open('kek.txt').readline()
    mail, password = file.split(' ')
    client = Client.from_credentials("oner161@yandex.ru", "rostov161rusrnd")

    playlists = get_all_playlists(client=client)

    # Инфа по каждому плейлисту
    for play in playlists:
        print(play)

    print(synchronize(playlists[0]['tracks'], playlists[1]['tracks']))
