# ![WebToon Icon](https://webtoons-static.pstatic.net/image/favicon/favicon.ico?dt=2017082301) WebToon Downloader

## About
This is a simple script that allows you to search and download webtoons published at [webtoons.com](https://webtoons.com).

## Usage
To run the script just type `python downloader.py --help` (`python3 downloader.py --help` if you have multiple installations of python) and you'll get the usage information:

```
usage: downloader.py [-h] [--url URL] [--name NAME] [--id ID] [--chapters CHAPTERS] option [output]

Download webtoons

positional arguments:
  option               search / download
  output               Output directory

optional arguments:
  -h, --help           show this help message and exit
  --url URL            Specify the download url
  --name NAME          Specify the webtoon's name
  --id ID              Specify the webtoon's id
  --chapters CHAPTERS  Chapters to download
```

As you can see, there are 2 basic modes of execution: download and search. To search for a work, simply use `downloader.py search --name="name"`

```
web@toon:~$ python3 downloader.py search --name="tower of god"
ORIGINALS:
        1. Tower of God - SIU - Fantasy (37.6M) [o95]

CANVAS:
        2. The Voice - Allow God - School [c369730]
        3. God & Ann - God & Ann - Slice of life [c575706]
        4. Moos - Lu of Moos - Comedy [c529303]
        5. Cup of Kitty  - Cup of Kitty - Slice of life [c369392]
        6. StarStruck - 8 Of Diamonds - Fantasy [c454673]
        7. Furr of Urros - Furr of Urros - Comedy [c489517]
        8. Crutchie Series!!! - pan of frying - Short story [c545353]
        9. The diary of me aka qings(not my real name) - Diary Of Qings - Slice of life [c415373]
        10. Plague Spreader - Boys Of Bummer - Sci-fi [c420766]
        11. Lullaby (H) - King of Ashes  - Short story [c462558]
        12. Stardust - God King Fitzy - Sci-fi [c478101]
        13. Bridge Duels. - Child of Death - Comedy [c566350]

To download one of these works, use the option 'download' with --id equal to the webtoon's id (for example, c4324)
```

To then download a work, just use the download mode:

```
web@toon:~$ python3 downloader.py download downloads/ --id=o95 --chapters=1-3,5
Downloading chapter 1...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:01<00:00,  6.90it/s]
Downloading chapter 2...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 51/51 [00:07<00:00,  6.46it/s] 
Downloading chapter 3...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 76/76 [00:11<00:00,  6.37it/s]
Downloading chapter 5...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 66/66 [00:37<00:00,  1.78it/s]
```

And now we can see all images that have been dowloaded:

```
web@toon:~$ ls downloads/
total 16436
-rwxrwxrwx 1 web web  64275 Jan 29 15:26 tower-of-god-ch1-1.jpg
-rwxrwxrwx 1 web web  98637 Jan 29 15:26 tower-of-god-ch1-2.jpg
-rwxrwxrwx 1 web web  79308 Jan 29 15:26 tower-of-god-ch1-3.jpg
...
```

You can also use an URL to download a webtoon:

```
web@toon:~$ python downloader.py download downloads/ --url="https://www.webtoons.com/en/action/the-god-of-high-school/list?title_no=66" --chapters=1
```