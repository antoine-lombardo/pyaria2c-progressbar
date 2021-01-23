# Implementation of a progress evaluator for aria2c batch download process

## Notes

Since this code use the number of completed downloads to evaluate the progress, it may only be useful when processing a large amount of file (more than 20-30) with approximatively the same weight. 

## Usage example

    import sys
    from pyaria2c import Pyaria2c
    
    def on_progress(percent: int):
        print('{}%'.format(str(percent)))
    
    def on_finish(status_code: int):
        print('aria2c ended with status code: {}'.format(str(status_code)))
    
    if __name__ == '__main__':
        aria2c_exec = 'aria2c.exe'
        urls = []
        filenames = []
        for i in range(0, 100):
            urls.append('http://ipv4.download.thinkbroadband.com/5MB.zip')
            filenames.append('file{}.zip'.format(i))
    
        downloader = Pyaria2c(aria2c_exec,
                            on_progress=on_progress,
                            on_finish=on_finish)
        downloader.download(urls, filenames, 'downloads')
        sys.exit(0)
The on_progress() function could call an update function of a progressbar for example.
