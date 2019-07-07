import canvasapi
import sys

url: str = 'https://canvas.ucdavis.edu'
password: str = sys.argv[1]  # password to be passed as first command line argument
canvas = canvasapi.Canvas(url, password)
course = canvas.get_course(1599)
print(course.name)
for user in course.get_users():
    print(user)
