from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos en memoria para canciones
songs = []
song_id_counter = 1

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK"}), 200

@app.route('/song', methods=['GET'])
def get_all_songs():
    return jsonify(songs), 200

@app.route('/song/<int:id>', methods=['GET'])
def get_song(id):
    song = next((s for s in songs if s['id'] == id), None)
    if song:
        return jsonify(song), 200
    return jsonify({"error": "Song not found"}), 404

@app.route('/song', methods=['POST'])
def create_song():
    global song_id_counter
    data = request.get_json()
    new_song = {
        'id': song_id_counter,
        'title': data.get('title'),
        'artist': data.get('artist'),
        'album': data.get('album'),
        'year': data.get('year')
    }
    songs.append(new_song)
    song_id_counter += 1
    return jsonify(new_song), 201

@app.route('/song/<int:id>', methods=['PUT'])
def update_song(id):
    song = next((s for s in songs if s['id'] == id), None)
    if song:
        data = request.get_json()
        song['title'] = data.get('title', song['title'])
        song['artist'] = data.get('artist', song['artist'])
        song['album'] = data.get('album', song['album'])
        song['year'] = data.get('year', song['year'])
        return jsonify(song), 200
    return jsonify({"error": "Song not found"}), 404

@app.route('/song/<int:id>', methods=['DELETE'])
def delete_song(id):
    global songs
    song = next((s for s in songs if s['id'] == id), None)
    if song:
        songs = [s for s in songs if s['id'] != id]
        return jsonify({"message": "Song deleted successfully"}), 200
    return jsonify({"error": "Song not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5002)
