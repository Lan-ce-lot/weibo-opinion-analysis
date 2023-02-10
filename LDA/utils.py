# python3
import re
# import rich bar
import sys
sys.path.append('..')
from logger.config import StreamLogger
import logging
from rich.progress import track
def infile(fliepath):
    train = []
    with open(fliepath,'r',encoding='utf-8') as f:
        # f to string
        for i in track(f.readlines()):
            n = re.findall(r"\[.*\]", i)[0]
            new_line = eval(n)
            train.append(new_line)
    return train


if __name__ == "__main__":
    # StreamLogger.info("StreamLogger111")
    logging.info("logging111")
    t = infile("./气候变化.txt")
    print(t[:10])
    # ans = re.findall(r"\[.*\]", s)
    # st = "[111]222222222222222"
    # no = re.search(r"\[.*\]", st)
    # print(no)
    # n = re.findall(r"\[.*\]", st)
    # print(n)
    # eval(n[0])
