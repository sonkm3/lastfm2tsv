# lastfm2tsv
Extract lastfm scrobble history into tab separated text file.

# requirement
* last.fm API key (you can acquire API key from here http://www.lastfm.jp/api/account/create )
* httplib2
 
# usage
`python lastfm2tsv -k <apikey> -u <username> [-p <(int)startpage>] [-i <(int)item per page>] [-m <(int) max page>]`

#tsv format
<table>
<tr><td>timestamp</td><td>datetime</td><td>artist name</td><td>artist mbid</td><td>album name</td><td>album mbid</td><td>track name</td><td>track mbid</td><td>hash(artist_name+album_name+track_name)</td></tr>
<tr><td>1374854779</td><td>2013-07-27 01:06:19</td><td>9nine</td><td>60bf8a76-dbf2-41c2-9328-aff14db120f7</td><td>9nine</td><td>51c54dd7-6e1f-48d9-b204-61a2577c1915</td><td>SHINING☆STAR</td><td>557161eb-9f12-4315-9551-0d048f28b1c3</td><td>e9ff9a618e9d5a6853f2aee9e29ba12b7f4b0d0e</td></tr>
</table>
