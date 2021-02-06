import source.monitor_display as md
import source.client_socket as s
import pyglet
import multiprocessing

def runpachinko(queue_dict):
    pach = md.Pachinko(queue_dict)
    pyglet.clock.schedule_interval(pach.update, 0.001)
    pyglet.app.run()

    # pass
if __name__ == '__main__':
    # runpachinko(None)
    queue_dict = {
        'queueue': multiprocessing.Queue(),
        'request_import': multiprocessing.Queue(),
        'request_export': multiprocessing.Queue()
    }
    client_socket_process = multiprocessing.Process(target=s.run_client_socket, args=(queue_dict,))
    game_process = multiprocessing.Process(target=runpachinko, args=(queue_dict,))
    game_process.start()
    client_socket_process.start()


    game_process.join()
    # client_socket_process.join()