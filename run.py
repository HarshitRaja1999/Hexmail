from multiprocessing import Process,Pipe
from bot.bot import run
from pub_sub.pub_sub import PubSub


if __name__=="__main__":
    discord_conn, pubsub_conn = Pipe()
    process1 = Process(target=run,args=(discord_conn,))
    process2 = Process(target=PubSub,args=(pubsub_conn,))
    process1.start()
    process2.start()
    process1.join()
    process2.join()