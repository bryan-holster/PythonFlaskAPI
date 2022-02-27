from flask import Flask, request, jsonify
import maxminddb
import json
import logging

# Initialize Flask
app = Flask(__name__)

logging.basicConfig(filename='record.log', level=logging.ERROR, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.route('/', methods=['GET'])
def check():
    app.logger.info(request)
    greenlight = False

    ip = request.args.get('ip')
    #If not a valid ip format return False
    if ip.count('.') != 3:
        return jsonify({'response': greenlight, 'message': 'Invalid IPv4 address.'}), 500

    try:
        #Parse whitelist into useable list
        whitelist = json.loads(request.args.get('whitelist'))
        #If whitelist is empty we can return False immediately
        if len(whitelist) < 1:
            return jsonify({'response': greenlight}), 200
    except Exception as e:
        app.logger.error(str(e), exc_info=True)
        return jsonify({'response': greenlight, 'message': 'Failed to properly format whitelist.'}), 500

    try:
        #Reading in MaxMind binary database from file
        #This db can be kept up to date by using GeoIP Update from MaxMind
        #https://dev.maxmind.com/geoip/updating-databases?lang=en
        with maxminddb.open_database('GeoLite2-Country.mmdb') as reader:
            #The whitelist could theoretically contain the geoname_id, iso_code, or country name
            #Country name isn't advised since it is language dependent. iso_code is likely best, because 
            #I don't know that geoname_id is agnostic to data provider

            #Returns the Alpha-2 version of the ISO code
            country = reader.get(ip)['country']['iso_code']
            greenlight = True if country in whitelist else False
    except Exception as e:
        app.logger.error(str(e), exc_info=True)
        return jsonify({'response': greenlight, 'message': 'Query failed for specified IPv4 address.'}), 500

    return jsonify({'response': greenlight}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)