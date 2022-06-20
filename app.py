# from lib2to3.pytree import Base
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Musician, Song
from auth import AuthError, requires_auth


# ------------------------------------------------------------------------------#
# Pagination
# ------------------------------------------------------------------------------#

MUSICIANS_PER_PAGE = 2

def paginate_musicians(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * MUSICIANS_PER_PAGE
    end = start + MUSICIANS_PER_PAGE

    musicians = [musician.format() for musician in selection]
    current_musicians = musicians[start:end]

    return current_musicians

SONGS_PER_PAGE = 1

def paginate_songs(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * SONGS_PER_PAGE
    end = start + SONGS_PER_PAGE

    songs = [song.format() for song in selection]
    current_songs = songs[start:end]

    return current_songs

# ------------------------------------------------------------------------------#
# Create and configure the app
# ------------------------------------------------------------------------------#

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    # ------------------------------------------------------------
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,PATCH')
        return response

    # ------------------------------------------------------------------------------#
    # Controllers
    # ------------------------------------------------------------------------------#

    #  Musicians
    # ------------------------------------------------------------
    @app.route('/musicians')
    @requires_auth('get:musicians')
    def retrieve_musicians(payload):
        selection = Musician.query.order_by(Musician.id).all()
        current_musicians = paginate_musicians(request, selection)

        if len(current_musicians) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'musicians': current_musicians,
            'total_musicians': len(Musician.query.all())
        })

    @app.route('/musicians/<int:musician_id>')
    @requires_auth('get:musicians')
    def specific_musician_info(payload, musician_id):

        musician = Musician.query.filter(Musician.id == musician_id).one_or_none()

        if musician is None:
            abort(
                404,
                'Musician with id: ' +
                str(musician_id) +
                ' could not be found.'
            )

        musician = musician.format()
        return jsonify({
            'success': True,
            'musicians': musician,
        })



    @app.route('/musicians/<int:musician_id>', methods=['PATCH'])
    @requires_auth('patch:musicians')
    def update_musician(payload, musician_id):
        body = request.get_json()

        try:
            musician = Musician.query.filter(Musician.id == musician_id).one_or_none()
            # this error rose when the id exits but doesn't have any data in the row. Ex: sometime we create a new row but soon delete it, then the id given by sql will remain while data has been eliminated.
            if musician is None:
                abort(
                    404,
                    'Musician with id: ' +
                    str(musician_id) +
                    ' could not be found.'
                )
            
            if 'name' in body:
                musician.name = str(body.get('name'))
            if 'e_mail' in body:
                musician.e_mail = str(body.get('e_mail'))
            if 'phone' in body:
                musician.phone = str(body.get('phone'))
            if 'website' in body:
                musician.website = str(body.get('website'))
            if 'introduction' in body:
                musician.introduction = str(body.get('introduction'))
            if 'avatar_link' in body:
                musician.avatar_link = str(body.get('avatar_link'))
            if 'genres' in body:
                musician.genres = str(body.get('genres'))
            
            musician.update()

            return jsonify({
                'success': True,
                'updated': musician.format()
            })

        except BaseException:
            abort(400)
            
    
    @app.route('/musicians/<int:musician_id>', methods=['DELETE'])
    @requires_auth('delete:musicians')
    def delete_musician(payload, musician_id):
        try:
            musician = Musician.query.filter(Musician.id == musician_id).one_or_none()

            if musician is None:
                abort(
                    404,
                    'Musician with id: ' +
                    str(musician_id) +
                    ' could not be found.'
                )
            musician.delete()
            selection = Musician.query.order_by(Musician.id).all()
            current_musicians = paginate_musicians(request, selection)

            return jsonify({
                'success': True,
                'deleted': musician_id,
                'musicians': current_musicians,
                'total_musicians': len(Musician.query.all())
            })
        
        except BaseException:
            abort(422)


    @app.route('/musicians', methods=['POST'])
    @requires_auth('post:musicians')
    def create_musician(payload):
        body = request.get_json()

        if body is None:
            abort(
                400,
                'Sorry there is something wrong and your request cannot be fulfilled...' +
                'Please check your input and try again.' 
            )

        new_name = body.get('name', None)
        new_e_mail = body.get('e_mail', None)
        new_phone = body.get('phone', None)
        new_website = body.get('website', None)
        new_introduction = body.get('introduction', None)
        new_avatar_link = body.get('avatar_link', None)
        new_genres = body.get('genres', None)

        if new_name is None:
            abort(
                400,
                "Sorry you need to input the musician's name"
            )

        try:
            musician = Musician(name=new_name, e_mail=new_e_mail, phone=new_phone, website=new_website, introduction=new_introduction, avatar_link=new_avatar_link, genres=new_genres)
            musician.add()

            selection = Musician.query.order_by(Musician.id).all()
            current_musicians = paginate_musicians(request, selection)

            return jsonify({
                'success': True,
                'created': musician.id,
                'musicians': current_musicians,
                'total_musicians': len(Musician.query.all())
            })
        
        except BaseException:
            abort(422)


    #  Songs
    # ------------------------------------------------------------
    @app.route('/songs')
    @requires_auth('get:songs')
    def retrieve_songs(payload):
        selection = Song.query.order_by(Song.id).all()
        current_songs = paginate_songs(request, selection)

        if len(current_songs) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'songs': current_songs,
            'total_songs': len(Song.query.all())
        })

    @app.route('/songs/<int:song_id>')
    @requires_auth('get:songs')
    def specific_song_info(payload, song_id):

        song = Song.query.filter(Song.id == song_id).one_or_none()

        if song is None:
            abort(
                404,
                'Song with id: ' +
                str(song_id) +
                ' could not be found.'
            )

        song = song.format()
        return jsonify({
            'success': True,
            'songs': song,
        })


    @app.route('/songs/<int:song_id>', methods = ['PATCH'])
    @requires_auth('patch:songs')
    def update_song(payload, song_id):
        body = request.get_json()

        try:
            song = Song.query.filter(Song.id == song_id).one_or_none()
            
            if song is None:
                abort(
                    404,
                    'Song with id: ' +
                    str(song_id) +
                    ' could not be found.'
                )
            
            if 'name' in body:
                song.name = str(body.get('name'))
            if 'introduction' in body:
                song.introduction = str(body.get('introduction'))
            if 'cover_link' in body:
                song.cover_link = str(body.get('cover_link'))
            if 'song_link' in body:
                song.song_link = str(body.get('song_link'))
            if 'genre' in body:
                song.genre = str(body.get('genre'))
            if 'musician_id' in body:
                song.musician_id = str(body.get('musician_id'))
            
            song.update()

            return jsonify({
                'success': True,
                'updated': song.format()
            })

        except BaseException:
            abort(400)
    
    @app.route('/songs/<int:song_id>', methods=['DELETE'])
    @requires_auth('delete:songs')
    def delete_song(payload, song_id):
        try:
            song = Song.query.filter(Song.id == song_id).one_or_none()

            if song is None:
                abort(
                    404,
                    'Song with id: ' +
                    str(song_id) +
                    ' could not be found.'
                )
            song.delete()
            selection = Song.query.order_by(Song.id).all()
            current_songs = paginate_songs(request, selection)

            return jsonify({
                'success': True,
                'deleted': song_id,
                'songs': current_songs,
                'total_songs': len(Song.query.all())
            })
        
        except:
            abort(
                422,
                'Opps, it seems there is something wrong and we can not complete what you have requested'
            )

    @app.route('/songs', methods=['POST'])
    @requires_auth('post:songs')
    def create_song(payload):
        body = request.get_json()

        if body is None:
            abort(
                400,
                'Sorry there is something wrong and your request cannot be fulfilled...' +
                'Please check your input and try again.' 
            )

        new_name = body.get('name', None)
        new_introduction = body.get('introduction', None)
        new_cover_link = body.get('cover_link', None)
        new_song_link = body.get('song_link', None)
        new_genre = body.get('genre', None)
        new_musician_id = body.get('musician_id', None)

        if new_name is None or new_song_link is None:
            abort(
                400,
                "Sorry you need to input the song's name and link."
            )

        try:
            song = Song(name=new_name, introduction=new_introduction, cover_link=new_cover_link, song_link=new_song_link, genre=new_genre, musician_id = new_musician_id)
            song.add()

            selection = Song.query.order_by(Song.id).all()
            current_songs = paginate_songs(request, selection)

            return jsonify({
                'success': True,
                'created': song.id,
                'songs': current_songs,
                'total_songs': len(Song.query.all())
            })
        
        except BaseException:
            abort(422)

    # ------------------------------------------------------------------------------#
    # Error Handling
    # ------------------------------------------------------------------------------#

    # def get_error_message(error, default_message):
    #     try:
    #         return error.description
    #     except BaseException:
    #         return default_message

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(auth_error):
        return jsonify({
            "success": False,
            "error": auth_error.status_code,
            "message": auth_error.error['description']
        }), auth_error.status_code
    # @app.errorhandler(405)
    # def not_allowed(error):
    #     return jsonify({
    #         'success': False,
    #         'error': 405,
    #         'message': 'method not allowed'
    #     }), 405

    # @app.errorhandler(500)
    # def server_error(error):
    #     return jsonify({
    #         'success': False,
    #         'error': 500,
    #         'message': 'Internal server error',
    #     }), 500    

    # @app.errorhandler(AuthError)
        
    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)