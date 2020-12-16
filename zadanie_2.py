import requests
import json
from bs4 import BeautifulSoup as Soup
from urllib import request
import create_database
import argparse
import cv2
import numpy as np


def get_soup_images(keyword, number):
    """
    based on given parameters gets images from flick and saves to database

    :param keyword:
    :param number:
    :return:
    """
    api_key = u'your_key'
    api_secret = u'your_key'

    # download json
    url = f"https://www.flickr.com/services/rest?method=flickr.photos.search&api_key={api_key}&format=json&nojsoncallback=1&text={keyword}"
    html = request.urlopen(url).read()
    soup_data = Soup(html, 'html.parser')
    site_json = json.loads(soup_data.text)

    # get list of photos
    all_photos = site_json['photos']
    photo_list = all_photos['photo']

    # saves images based on input params
    for id, item in enumerate(photo_list):
        if id == number: break
        server = item['server']
        photo_id = item['id']
        secret = item['secret']
        title = item['title']
        save_images(server, photo_id, secret, title)


def save_images(server, photo_id, secret, title):
    """
    downloads actual binary of an image and inserts into database
    :param server:
    :param photo_id:
    :param secret:
    :param title:
    :return:
    """
    url = f"https://live.staticflickr.com/{server}/{photo_id}_{secret}.jpg"
    response = requests.get(url)
    create_database.insertBLOB(photo_id, title, response.content)


def bgr_evaluator(img):
    """
    quick evaluator that considers colors oponency property and substracts sum all of red values and green values

    :param img:
    :return:
    """
    b, g, r = cv2.split(img)
    sum_r = np.sum(r)
    sum_g = np.sum(g)
    return sum_r - sum_g

def hsv_evalutor(img):
    """
    evaluates hue channel by thresholding red color by sum of all pixels that fit red color range

    :param img:
    :return:
    """

    # normalize size for comparison
    img = cv2.resize(img, (512, 512), img)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV);

    lower_red = np.array([170, 165, 0])
    upper_red = np.array([179, 255, 255])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)

    # cv2.imshow('mask', mask0)
    value = np.sum(mask0,dtype=int)

    return value



def get_most_red():
    """
    shows most red image from the database
    :return:
    """

    # get all data from database
    all_rows = create_database.select_images()
    values_of_desc = []

    # iterate and analyze images
    for row in all_rows:
        nparr = np.frombuffer(row[2], np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR in OpenCV 3.1
        # descriptor = bgr_evaluator(img_np)
        descriptor = hsv_evalutor(img_np)
        values_of_desc.append((descriptor, img_np))

    # show most reddish image
    # print(values_of_desc)
    most_red = sorted(values_of_desc, key=lambda x: x[0],reverse=True)
    print("most red", most_red[0][0])
    cv2.imshow('most red img', most_red[0][1])
    cv2.waitKey()


if __name__ == '__main__':
    # create database
    create_database.main()

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', required=True, type=str, help='keyword to look')
    parser.add_argument('-n', required=False, default=100, type=int, help='number of photos')
    args = parser.parse_args()

    # download images
    get_soup_images(args.k, args.n)

    # get most red images from all images
    get_most_red()
