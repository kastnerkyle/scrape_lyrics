import spynner
import os
import zipfile
import zlib
compression = zipfile.ZIP_DEFLATED
import threading
import Queue

out_dir = "results"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)


class WriteThread(threading.Thread):
    def __init__(self, queue, out_queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue

    def run(self):
        while True:
            n, site = self.queue.get()
            url = site.strip()
            result_path = url
            result_path = result_path.split("/")[-1]
            zip_path = result_path + ".zip"
            zip_file = os.path.join(out_dir, zip_path)
            result_path = result_path + ".html"
            result_file = os.path.join(out_dir, result_path)
            if os.path.exists(zip_file):
                self.out_queue.put((zip_file, 0))
                self.queue.task_done()
                continue

            # creating and closing browser is wasteful but guarantees no
            # memory issues
            browser = spynner.Browser()
            browser.create_webview(True)
            try:
                browser.load(url, load_timeout=20)
            except spynner.browser.SpynnerTimeout:
                print("Load timeout reading %i, %s" % (n, url))

            print("Scraping %i, %s" % (n, url))
            try:
                f = open(result_file, mode="w")
                read = browser._get_html()
                f.writelines(read)
                f.close()

                zf = zipfile.ZipFile(zip_file, mode='w')
                zf.write(result_file, compress_type=compression)
                os.remove(result_file)
                zf.close()
                self.out_queue.put((zip_file, 0))

            except TypeError:
                print("Error reading %i, %s" % (n, url))
                self.out_queue.put((zip_file, 2))
            except spynner.browser.SpynnerTimeout:
                print("Timeout reading %i, %s" % (n, url))
                self.out_queue.put((zip_file, 3))
            except:
                print("Unknown error reading %i, %s" % (n, url))
                self.out_queue.put((zip_file, 4))
            browser.close()
            del browser
            self.queue.task_done()


if __name__ == '__main__':
    def main():
        f = open("all_sites.txt")
        import random
        sites = f.readlines()
        # Randomly shuffle sites so multiple python threads aren't running
        # on top of one another
        random.shuffle(sites)
        # Use spynner timeout and qsize to avoid flooding the site
        # Ideally a rate of ~1 per second... 12 days total to get all 2M
        input_qsize = 20
        queue = Queue.Queue(maxsize=input_qsize)
        out_queue = Queue.Queue()
        for i in range(1):
            # Would love to use > 1 thread, but QApplication and xvfb are
            # segfaulting
            # Gonna have to add some bash hacks to make this work
            t = WriteThread(queue, out_queue)
            t.setDaemon(True)
            t.start()

        for n, site in enumerate(sites):
            queue.put((n, site))
        queue.join()

    main()
