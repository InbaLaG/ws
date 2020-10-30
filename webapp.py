import opengraph
from flask import Flask, request, jsonify
import urlcanon

app = Flask(__name__)
app.config["DEBUG"] = True


url_db = {}


def get_canonized_url(url):
    return urlcanon.parse_url(url)


def scrape_page(og_obg):
    return {}


def get_url_record_by_url(db, url):
    for k, v in db.items():
        if v["url"] == url:
            return [k, v]
    return None


def get_ogp_info(msg_id=None, url=None):
    if msg_id == None or url == None:
        return None
    rec = {}
    rec['url'] = url
    data = {}
    og = OpenGraph(
        url, ["og:title", "article:published_time", "og:price:amount"])

    # print(og.metadata)
    # print(og.metadata['title'])

    rec['og_obg'] = og
    # rec['valid'] = og.is_valid()
    return rec


class MyWebService:
    @app.route('/stories', methods=['GET'])
    def get_stories(msg_id=None):
        if msg_id == None:
            return ('no URL')
        elif msg_id in url_db:
            url_record = url_db[msg_id]
            return ('found')
        else:
            return ('No url %s ' % url)

    @app.route('/stories', methods=['POST'])
    def set_stories():
        url = request.args.get('url')
        print('url %s' % url)
        if url == None:
            return "error"
        else:
            c_url = get_canonized_url(url)
            exist_rec = get_url_record_by_url(url_db, c_url)
            if exist_rec:
                print("exist?")
                return exist_rec[0]
            else:
                if len(url_db) == 0:
                    print("no db")
                    msg_id = 1
                else:
                    msg_id = max([int(_) for _ in url_db.keys()]) + 1
                print(msg_id)
                mdi = get_ogp_info(msg_id, c_url)
                url_db[msg_id] = mdi

                return mdi


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
