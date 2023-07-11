from flask import Flask, redirect, request, jsonify
app = Flask(__name__)

url_mappings = {}
visit_counts = {}

@app.route('/redirect/<short_code>', methods=['GET'])
def redirect_url(short_code):
    if short_code in url_mappings:
        original_url = url_mappings[short_code]
        visit_counts[short_code] = visit_counts.get(short_code, 0) + 1
        unique_visitors = len(set(request.remote_addr for _ in range(visit_counts[short_code])))
        return redirect(original_url, code=302)
    else:
        return "Short code not found", 404

@app.route('/create/<short_code>/<path:destination_url>', methods=['POST'])
def create_short_url(short_code, destination_url):
    if short_code in url_mappings:
        return "Short code already exists", 409
    else:
        url_mappings[short_code] = destination_url
        visit_counts[short_code] = 0
        return "Short URL created", 201

@app.route('/update/<short_code>', methods=['PATCH'])
def update_destination_url(short_code):
    if short_code not in url_mappings:
        return "Short code not found", 404
    else:
       
        new_destination_url = request.json.get('destination_url')
        if new_destination_url:
            url_mappings[short_code] = new_destination_url
            return "Destination URL updated", 200
        else:
            return "Missing destination URL in request body", 400

@app.route('/stats/<short_code>', methods=['GET'])
def get_stats(short_code):
    if short_code in url_mappings:
        visit_count = visit_counts.get(short_code, 0)
        unique_visitors = len(set(request.remote_addr for _ in range(visit_count)))
        return jsonify({
            'visit_count': visit_count,
            'unique_visitors': unique_visitors
        })
    else:
        return "Short code not found", 404

if __name__ == '__main__':
    app.run()
