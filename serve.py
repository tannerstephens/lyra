#!/usr/bin/python3

from lyra import create_app
from subprocess import Popen

def main():
  app = create_app()
  app.run(debug=True, threaded=True, host="127.0.0.1", port=3000)

if __name__ == "__main__":
  webpack_watch = Popen('yarn watch', shell=True)
  main()
